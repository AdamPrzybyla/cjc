import string
import curses

import pyxmpp
from cjc import ui
from cjc.plugin import PluginBase
from cjc import common

theme_attrs=(
	("message.subject", curses.COLOR_YELLOW,curses.COLOR_BLACK,curses.A_BOLD, curses.A_UNDERLINE),
	("message.sender", curses.COLOR_YELLOW,curses.COLOR_BLACK,curses.A_BOLD, curses.A_UNDERLINE),
	("message.body", curses.COLOR_WHITE,curses.COLOR_BLACK,curses.A_NORMAL, curses.A_NORMAL),
)

theme_formats=(
	("message.received",
"""------------------
%[message.subject]From:    %(from)s
%[message.sender]Subject: %(subject)s

%[message.body]%(body)s
------------------
"""),
	("message.sent",
"""------------------
%[message.subject]To:      %(to)s
%[message.sender]Subject: %(subject)s

%[message.body]%(body)s
------------------
"""),
	("message.composing",
"""------------------
%[message.subject]To:      %(from)s
%[message.sender]Subject: %(subject)s

%[message.body]%(body)s
------------------
"""),
	("message.descr-per-user","Messages from %(J:peer:full)s [%(J:peer:show)s] %(J:peer:status)s"),
	("message.descr","Messages"),
)

class MessageBuffer:
	def __init__(self,plugin,peer,thread):
		self.plugin=plugin
		self.peer=peer
		self.thread=thread
		if peer:
			self.buffer=ui.TextBuffer(plugin.cjc.theme_manager,{"peer":self.peer},
									"message.descr-per-user")
		else:
			self.buffer=ui.TextBuffer(plugin.cjc.theme_manager,{},"message.descr")
		self.buffer.update()
		self.buffer.register_commands({"close": (self.cmd_close,
							"/close",
							"Closes current chat buffer"),
						"reply": (self.cmd_reply,
							"/reply [-subject subject] [text]",
							"Reply to the last message in window"),
						})
		self.last_sender=None
		self.last_subject=None
		self.last_body=None
		self.last_thread=None

	def add_received(self,sender,subject,body,thread):
		self.buffer.append_themed("message.received",{
				"from": sender,
				"subject": subject,
				"thread": thread,
				"body": body,
				})
		self.buffer.update()
		self.last_sender=sender
		self.last_subject=subject
		self.last_body=body
		self.last_thread=thread
		
	def add_sent(self,recipient,subject,body,thread):
		self.buffer.append_themed("message.sent",{
				"to": recipient,
				"subject": subject,
				"thread": thread,
				"body": body,
				})
		self.buffer.update()
		
	def error(self,stanza):
		err=stanza.get_error()
		emsg=err.get_message()
		msg="Error"
		if emsg:
			msg+=": %s" % emsg
		etxt=err.get_text()
		if etxt:
			msg+=" ('%s')" % etxt
		self.buffer.append_themed("error",msg)
		self.buffer.update()

	def cmd_close(self,args):
		args.finish()
		key=self.peer.bare().as_unicode()
		if self.plugin.buffers.has_key(key):
			l=self.plugin.buffers[key]
			if self in l:
				l.remove(self)
		self.buffer.close()

	def cmd_reply(self,args):
		if not self.last_sender:
			self.buffer.append_themed("error","No message to reply to")
			return
		arg1=args.get()
		if arg1=="-subject":
			args.shift()
			subject=args.shift()
			if not subject:
				self.buffer.append_themed("error","subject argument missing")
				return
		else:
			if self.last_subject:
				if self.last_subject.startswith(u"Re:"):
					subject=self.last_subject
				else:
					subject=u"Re: "+self.last_subject
			else:
				subject=None
			
		if not self.plugin.cjc.stream:
			self.buffer.append_themed("error","Not connected!")
			return
			
		body=args.all()
		if not body:
			self.buffer.append_themed("error","Message composition not supported yet"
				" - you mast include message body on the command line")
			return

		self.plugin.send_message(self.last_sender,subject,body,self.last_thread)

class Plugin(PluginBase):
	def __init__(self,app):
		PluginBase.__init__(self,app)
		self.buffers={}
		self.last_thread=0
		app.theme_manager.set_default_attrs(theme_attrs)
		app.theme_manager.set_default_formats(theme_formats)
		self.available_settings={
			"buffer": ("How received messages should be put in buffers"
					" (single|separate|per-user|per-thread)",
					("single","separate","per-user","per-thread"))}
		self.settings={"buffer":"per-user"}
		app.register_commands({"message": (self.cmd_message,
					"/message [-subject subject] nick|jid [text]",
					"Compose or send message to given user"),
					"msg": "message",})
		app.add_event_handler("presence changed",self.ev_presence_changed)

	def cmd_message(self,args):
		arg1=args.shift()
		if arg1=="-subject":
			subject=args.shift()
			if not subject:
				self.error("subject argument missing")
				return
			recipient=args.shift()
		else:
			subject=None
			recipient=arg1
		if not recipient:
			self.error("/message without arguments")
			return
			
		if not self.cjc.stream:
			self.error("Connect first!")
			return
			
		recipient=self.cjc.get_user(recipient)
		if recipient is None:
			return

		body=args.all()
		if not body:
			self.error("Message composition not supported yet"
				" - you mast include message body on the command line")
			return

		self.send_message(recipient,subject,body)

	def send_message(self,recipient,subject,body,thread=0,buff=None):
		if thread==0:
			self.last_thread+=1
			thread="message-thread-%i" % (self.last_thread,)
		m=pyxmpp.Message(to=recipient,type="normal",subject=subject,body=body,thread=thread)
		self.cjc.stream.send(m)
		if buff is None:
			buff=self.find_or_make(recipient,thread)
		buff.add_sent(recipient,subject,body,thread)

	def ev_presence_changed(self,event,arg):
		key=arg.bare().as_unicode()
		if not self.buffers.has_key(key):
			return
		for buff in self.buffers[key]:
			if buff.peer==arg or buff.peer==arg.bare():
				buff.buffer.update()

	def session_started(self,stream):
		self.cjc.stream.set_message_handler("normal",self.message_normal)
		self.cjc.stream.set_message_handler("error",self.message_error,None,90)

	def find_buffer(self,user,thread):
		buff=None
		if user:
			key=user.bare().as_unicode()
		else:
			key=user
		if self.buffers.has_key(key):
			buffs=self.buffers[key]
			for b in buffs:
				if thread==b.thread:
					buff=b
					break
		return buff

	def find_or_make(self,user,thread):
		bset=self.settings["buffer"]
		if bset=="separate":
			pass
		elif bset=="per-thread":
			buff=self.find_buffer(user,thread)
			if buff:
				return buff
		elif bset=="per-user":
			buff=self.find_buffer(user,None)
			if buff:
				return buff
			thread=None
		else:
			buff=self.find_buffer(None,None)
			if buff:
				return buff
			thread=None
			user=None
		buff=MessageBuffer(self,user,thread)
		if user:
			key=user.bare().as_unicode()
		else:
			key=user
		if not self.buffers.has_key(key):
			self.buffers[key]=[buff]
		else:
			self.buffers[key].append(buff)
		return buff

	def message_error(self,stanza):
		if self.settings["buffer"]=="separate":
			return 0
		fr=stanza.get_from()
		thread=stanza.get_thread()
	
		buff=self.find_buffer(fr,thread)
		bset=self.settings["buffer"]
		if not buff and bset in ("per-thread","per-user","single"):
			buff=self.find_buffer(fr,thread)
		if not buff and bset in ("per-user","single"):
			buff=self.find_buffer(fr,None)
		if not buff and bset=="single":
			buff=self.find_buffer(None,None)
		if not buff:
			return 0
		buff.error(stanza)
		return 1
	
	def message_normal(self,stanza):
		fr=stanza.get_from()
		thread=stanza.get_thread()
		subject=stanza.get_subject()
		body=stanza.get_body()
		if body is None:
			body=u""

		buff=self.find_or_make(fr,thread)
		buff.add_received(fr,subject,body,thread)
		return 1