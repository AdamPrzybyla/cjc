#!/usr/bin/python -u

import libxml2
import time
import traceback
import sys,os
import select
import string
from types import StringType,UnicodeType,IntType,ListType,TupleType
import locale
import curses
import threading
import socket

import pyxmpp

import ui
import ui.buffer
import version
import commands
import themes
import common

logfile=open("cjc.log","a")

class Exit(Exception):
	pass

global_commands={
	# command: alias
	#    or
	# command: (handler, usage, description)
	#
	# handler may be method name or any callable
	"exit": ("cmd_quit",
		"/exit [reason]",
		"Exit from CJC"),
	"quit": "exit",
	"set": ("cmd_set",
		"/set [setting] [value]",
		"Changes one of the settings."
		" Without any arguments shows all current settings."
		" With only one argument shows description and current value of given settings."),
	"unset": ("cmd_unset",
		"/unset [setting]",
		"Unsets one of settings."),
	"connect": ("cmd_connect",
		"/connect",
		"Connect to a Jabber server"),
	"disconnect": ("cmd_disconnect",
		"/disconnect [reason]",
		"Disconnect from a Jabber server"),
	"save": ("cmd_save",
		"/save [filename]",
		"Save current settings to a file (default: .cjcrc)"),
	"load": ("cmd_load",
		"/load [filename]",
		"Load settings from a file (default: .cjcrc)"),
	"redraw": ("cmd_redraw",
		"/redraw",
		"Redraw screen"),
	"info": ("cmd_info",
		"/info jid",
		"Show information known about given jid"),
	"help": ("cmd_help",
		"/help [command]",
		"Show simple help"),
	"theme": ("cmd_theme",
		("/theme load [filename]","/theme save [filename]"),
		"Theme management. Default theme filename is \".cjc-theme\"")
}

global_settings={
	"jid": ("Jabber ID to use.",pyxmpp.JID),
	"password": ("Jabber ID to use.",unicode),
	"port": ("Port number to connect to",int),
	"server": ("Server address to connect to",str),
	"auth_methods": ("Authentication methods to use (e.g. 'sasl:DIGEST-MD5 digest')",list),
	"layout": ("Screen layout - one of: plain,icr,irc,vertical,horizontal",str,"set_layout"),
	"disconnect_timeout": ("Time (in seconds) to wait until the connection is closed before exit",float),
	"disconnect_delay": ("Delay (in seconds) before stream is disconnected after final packets are written - needed for some servers to accept disconnect reason.",float),
}

global_theme_attrs=(
	("default", curses.COLOR_WHITE,curses.COLOR_BLACK,curses.A_NORMAL, curses.A_NORMAL),
	("error", curses.COLOR_RED,curses.COLOR_BLACK,curses.A_BOLD, curses.A_STANDOUT),
	("warning", curses.COLOR_YELLOW,curses.COLOR_BLACK,curses.A_BOLD, curses.A_UNDERLINE),
	("info", curses.COLOR_WHITE,curses.COLOR_BLACK,curses.A_NORMAL, curses.A_NORMAL),
	("debug", curses.COLOR_WHITE,curses.COLOR_BLACK,curses.A_NORMAL, curses.A_DIM),
	("bar", curses.COLOR_WHITE,curses.COLOR_BLACK,curses.A_STANDOUT, curses.A_STANDOUT),
	("scroll_mark", curses.COLOR_YELLOW,curses.COLOR_BLACK,curses.A_BOLD, curses.A_BOLD),
)

global_theme_formats=(
	("window_status",u"%[bar] %(active)s %(winname)s:%(locked)s%(bufname)s(%(bufnum)s) [%(bufcol)s,%(bufrow)s]"),
	("title_bar",u"%[bar]%(name)s ver. %(version)s by %(author)s"),
	("status_bar",u"%[bar]%(name)-40s Active buffers: [%{buffers}]"),
	("error",u"%[error][%(T:now)s] %(msg)s\n"),
	("warning",u"%[warning][%(T:now)s] %(msg)s\n"),
	("info",u"%[info][%(T:now)s] %(msg)s\n"),
	("debug",u"%[debug][%(T:now)s] %(msg)s\n"),
	("buffer_visible",""),
	("buffer_inactive",""),
	("buffer_active1","%[default]%(num)i"),
	("buffer_active2","%[warning]%(num)i"),
	("buffer_active3","%[error]%(num)i"),
)

class Application(pyxmpp.Client,commands.CommandHandler):
	def __init__(self):
		pyxmpp.Client.__init__(self)
		commands.CommandHandler.__init__(self,global_commands)
		self.settings={
			"jid":self.jid,
			"password":self.password,
			"auth_methods":self.auth_methods,
			"layout":"plain",
			"disconnect_timeout":10.0,
			"disconnect_delay":0.25}
		self.available_settings=global_settings
		self.plugin_dirs=["cjc/plugins"]
		self.plugins={}
		self.event_handlers={}
		self.user_info={}
		self.info_handlers={}
		self.exiting=0
		self.ui_thread=None
		self.stream_thread=None
		self.roster_window=None
		self.status_window=None
		self.main_window=None

	def load_plugin(self,name):
		self.info("  %s" % (name,))
		try:
			mod=__import__(name)
			plugin=mod.Plugin(self)
			self.plugins[name]=plugin
		except:
			self.print_exception()
			self.info("Plugin load failed")

	def load_plugins(self):
		sys_path=sys.path
		for path in self.plugin_dirs:
			self.info("Loading plugins from %s:" % (path,))
			sys.path=[path]+sys_path
			try:
				d=os.listdir(path)
			except (OSError,IOError),e:
				self.error("Couldn't get plugin list: %s" % (e,))
				continue
			for f in d:
				if f[0]=="." or not f.endswith(".py"):
					continue
				self.load_plugin(os.path.join(f[:-3]))
		sys.path=sys_path

	def add_event_handler(self,event,handler):
		if not self.event_handlers.has_key(event):
			self.event_handlers[event]=[]
		self.event_handlers[event].append(handler)

	def send_event(self,event,arg=None):
		if not self.event_handlers.has_key(event):
			return
		for h in self.event_handlers[event]:
			try:
				h(event,arg)
			except:
				self.print_exception()
				self.info("Event handler failed")

	def add_info_handler(self,var,handler):
		self.info_handlers[var]=handler

	def command(self,cmd,args):
		if not commands.CommandHandler.command(self,cmd,args):
			self.error(u"Unknown command: %s" % (cmd,))

	def layout_plain(self):
		status_bar_params={
			"name": "CJC",
			"version": version.version,
			"author": "Jacek Konieczny <jajcus@bnet.pl>",
			}
		ui.buffer.activity_handlers=[]
		top_bar=ui.StatusBar(self.theme_manager,"title_bar",status_bar_params)
		ui.buffer.activity_handlers.append(top_bar.update)
		self.main_window=ui.Window(self.theme_manager,"Main")
		command_line=ui.EditLine(self.theme_manager)
		bottom_bar=ui.StatusBar(self.theme_manager,"status_bar",status_bar_params)
		ui.buffer.activity_handlers.append(bottom_bar.update)
		sp=ui.HorizontalSplit(top_bar,self.main_window,bottom_bar,command_line)
		self.screen.set_content(sp)
		self.screen.focus_window(self.main_window)
		self.status_window=None
		self.roster_window=None

	def layout_icr(self):
		status_bar_params={
			"name": "CJC",
			"version": version.version,
			"author": "Jacek Konieczny <jajcus@bnet.pl>",
			}
		ui.buffer.activity_handlers=[]
		top_bar=ui.StatusBar(self.theme_manager,"title_bar",status_bar_params)
		ui.buffer.activity_handlers.append(top_bar.update)
		self.status_window=ui.Window(self.theme_manager,"Status",1)
		self.main_window=ui.Window(self.theme_manager,"Main")
		command_line=ui.EditLine(self.theme_manager)
		bottom_bar=ui.StatusBar(self.theme_manager,"status_bar",status_bar_params)
		ui.buffer.activity_handlers.append(bottom_bar.update)
		self.roster_window=ui.Window(self.theme_manager,"Roster",1)

		sp=ui.VerticalSplit(self.main_window,self.roster_window)
		sp=ui.HorizontalSplit(top_bar,self.status_window,sp,bottom_bar,command_line)
		self.screen.set_content(sp)
		self.screen.focus_window(self.main_window)
	
	def layout_irc(self):
		status_bar_params={
			"name": "CJC",
			"version": version.version,
			"author": "Jacek Konieczny <jajcus@bnet.pl>",
			}
		ui.buffer.activity_handlers=[]
		top_bar=ui.StatusBar(self.theme_manager,"title_bar",status_bar_params)
		ui.buffer.activity_handlers.append(top_bar.update)
		self.status_window=ui.Window(self.theme_manager,"Status",1)
		self.main_window=ui.Window(self.theme_manager,"Main")
		command_line=ui.EditLine(self.theme_manager)
		bottom_bar=ui.StatusBar(self.theme_manager,"status_bar",status_bar_params)
		ui.buffer.activity_handlers.append(bottom_bar.update)
		self.roster_window=ui.Window(self.theme_manager,"Roster",1)

		sp=ui.VerticalSplit(self.status_window,self.roster_window)
		sp=ui.HorizontalSplit(top_bar,sp,self.main_window,bottom_bar,command_line)
		self.screen.set_content(sp)
		self.screen.focus_window(self.main_window)

	def layout_vertical(self):
		status_bar_params={
			"name": "CJC",
			"version": version.version,
			"author": "Jacek Konieczny <jajcus@bnet.pl>",
			}
		ui.buffer.activity_handlers=[]
		top_bar=ui.StatusBar(self.theme_manager,"title_bar",status_bar_params)
		ui.buffer.activity_handlers.append(top_bar.update)
		self.main_window=ui.Window(self.theme_manager,"Main")
		command_line=ui.EditLine(self.theme_manager)
		bottom_bar=ui.StatusBar(self.theme_manager,"status_bar",status_bar_params)
		ui.buffer.activity_handlers.append(bottom_bar.update)
		self.roster_window=ui.Window(self.theme_manager,"Roster",1)

		sp=ui.VerticalSplit(self.main_window,self.roster_window)
		sp=ui.HorizontalSplit(top_bar,sp,bottom_bar,command_line)
		self.screen.set_content(sp)
		self.screen.focus_window(self.main_window)
		self.status_window=None

	def layout_horizontal(self):
		status_bar_params={
			"name": "CJC",
			"version": version.version,
			"author": "Jacek Konieczny <jajcus@bnet.pl>",
			}
		ui.buffer.activity_handlers=[]
		top_bar=ui.StatusBar(self.theme_manager,"title_bar",status_bar_params)
		ui.buffer.activity_handlers.append(top_bar.update)
		self.main_window=ui.Window(self.theme_manager,"Main")
		command_line=ui.EditLine(self.theme_manager)
		bottom_bar=ui.StatusBar(self.theme_manager,"status_bar",status_bar_params)
		ui.buffer.activity_handlers.append(bottom_bar.update)
		self.roster_window=ui.Window(self.theme_manager,"Roster",1)
		sp=ui.HorizontalSplit(top_bar,self.roster_window,self.main_window,bottom_bar,command_line)
		self.screen.set_content(sp)
		self.screen.focus_window(self.main_window)
		self.status_window=None

	def run(self,screen):
		self.screen=screen
		self.theme_manager=themes.ThemeManager(self)
		try:
			self.theme_manager.load(".cjc-theme")
		except (IOError,OSError):
			pass
		self.theme_manager.set_default_attrs(global_theme_attrs)
		self.theme_manager.set_default_formats(global_theme_formats)
		screen.set_default_command_handler(self)
		
		self.status_buf=ui.TextBuffer(self.theme_manager,"Status")
		self.message_buf=ui.TextBuffer(self.theme_manager,"Messages")

		self.set_layout(self.settings["layout"],"plain")
		
		self.screen.update()
		
		common.error=self.error
		common.debug=self.debug
		common.print_exception=self.print_exception
		
		self.load_plugins()

		self.load()
		if not self.settings["jid"]:
			self.info("")
			self.info("Quickstart:")
			self.info("/set jid your_username@your.domain/your_resource")
			self.info("/set password your_password")
			self.info("/save")
			self.info("/connect")
			self.info("/chat jajcus@jabber.bnet.pl CJC Rulez!")
			self.info("")
			self.info("press Alt-Tab (or Escape Tab) to change active window")
			self.info("PgUp/PgDown to scroll window content")

		self.ui_thread=threading.Thread(None,self.ui_loop,"UI")
		self.stream_thread=threading.Thread(None,self.stream_loop,"Stream")

		self.ui_thread.start()
		self.stream_thread.start()
		self.main_loop()

		for th in threading.enumerate():
			if th is threading.currentThread():
				continue
			th.join(1)
		for th in threading.enumerate():
			if th is threading.currentThread():
				continue
			th.join(0)

	def session_started(self):
		for p in self.plugins.values():
			try:
				p.session_started(self.stream)
			except:
				self.print_exception()
				self.info("Plugin call failed")
		self.stream.set_message_handler("error",self.message_error)
		self.stream.set_message_handler("normal",self.message_normal)

	def disconnected(self):
		self.warning("Disconnected")

	def message_error(self,stanza):
		self.warning(u"Message error from: "+stanza.get_from().as_unicode())
		
	def message_normal(self,stanza):
		self.info(u"Message from: "+stanza.get_from().as_unicode())
		self.message_buf.append_line(u"Message from: "+stanza.get_from().as_unicode())
		self.message_buf.append_line("Subject: "+stanza.get_subject())
		self.message_buf.append_line(stanza.get_body())
		self.message_buf.update(1)
	
	def cmd_quit(self,args):
		reason=args.all()
		args.finish()
		self.exit_request(reason)

	def cmd_connect(self,args):
		if self.stream:
			self.error(u"Already connected")
			return
		jid=self.settings.get("jid")
		if not jid:
			self.error(u"Can't connect - jid not given")
			return
		if None in (jid.node,jid.resource):
			self.error(u"Can't connect - jid is not full")
			return
		password=self.settings.get("password")
		if not password:
			self.error(u"Can't connect - password not given")
			return
		self.jid=jid
		self.password=password
		self.port=self.settings.get("port")
		if not self.port:
			self.port=5222
		self.server=self.settings.get("server")
		self.auth_methodsr=self.settings.get("auth_methods")
		self.info(u"Connecting...")
		try:
			self.connect()
		except pyxmpp.StreamError,e:
			self.error("Connection failed: "+str(e))
		except (socket.error),e:
			self.error("Connection failed: "+e.args[1])
	
	def cmd_disconnect(self,args):
		if not self.stream:
			self.error(u"Not connected")
			return
		reason=args.all()
		args.finish()
		if reason:
			self.info(u"Disconnecting (%s)..." % (reason,))
		else:
			self.info(u"Disconnecting...")
		self.send_event("disconnect request",reason)
		time.sleep(self.settings["disconnect_delay"])
		self.disconnect()
	
	def cmd_set(self,args):
		fvar=args.shift()
		if not fvar:
			for plugin in [None]+self.plugins.keys():
				if plugin is None:
					obj=self
				else:
					obj=self.plugins[plugin]
				for var in obj.available_settings:
					sdef=obj.available_settings[var]
					if len(sdef)<3:
						nsdef=[None,str,None]
						nsdef[:len(sdef)]=list(sdef)
						sdef=nsdef
					descr,typ,handler=sdef
					val=obj.settings.get(var)
					if var=="password":
						val=len(val) * '*'
					if plugin is not None:
						var="%s.%s" % (plugin,var)
					if val is None:
						self.info("%s is not set" % (var,))
						continue
					if type(typ) is tuple:
						typ=typ[0]
					if typ is list:
						self.info(u"%s = %s" % (var,string.join(val,",")))
					elif typ is pyxmpp.JID:
						self.info(u"%s = %s" % (var,val.as_unicode()))
					else:
						self.info(u"%s = %s" % (var,val))
			return

		val=args.shift()
		args.finish()

		if fvar.find(".")>0:
			plugin,var=fvar.split(".",1)
			try:
				obj=self.plugins[plugin]
			except KeyError:
				self.error("Unknown category: "+plugin)
				return
		else:
			obj=self
			var=fvar

		try:
			sdef=obj.available_settings[var]
			if len(sdef)<3:
				nsdef=[None,str,None]
				nsdef[:len(sdef)]=list(sdef)
				sdef=nsdef
			descr,typ,handler=sdef
		except KeyError:
			self.error("Unknown setting: "+fvar)
			return

		if val is None:
			self.info(u"%s - %s" % (fvar,descr))
			val=obj.settings.get(var)
			if val is None:
				self.info("%s is not set" % (fvar,))
				return
			if type(typ) is tuple:
				typ=typ[0]
			if typ is list:
				self.info(u"%s = %s" % (fvar,string.join(val,",")))
			elif typ is pyxmpp.JID:
				self.info(u"%s = %s" % (fvar,val.as_unicode()))
			else:
				self.info(u"%s = %s" % (fvar,val))
			return
	
		if type(typ) is not tuple:
			typ=(typ,)

		valid=0
		for t in typ:
			if t is None:
				continue
			if t is unicode:
				valid=1
				break
			try:
				if t is list:
					val=val.split(",")
				else:
					val=t(val)
				valid=1
				break
			except Exception,e:
				continue

		if not valid:
			self.error("Bad value: "+str(e))
			return

		if handler:
			if not callable(handler):
				handler=getattr(obj,handler)
		
		oldval=obj.settings.get(var)
		obj.settings[var]=val
		if handler:
			handler(oldval,val)

	def cmd_unset(self,args):
		fvar=args.shift()
		
		if not fvar:
			return self.cmd_set(args)

		if fvar.find(".")>0:
			plugin,var=fvar.split(".",1)
			try:
				obj=self.plugins[plugin]
			except KeyError:
				self.error("Unknown category: "+plugin)
				return
		else:
			obj=self
			var=fvar

		try:
			descr,typ=obj.available_settings[var][:2]
		except KeyError:
			self.error("Unknown setting: "+fvar)
			return

		if typ is None:
			pass
		elif type(typ) is tuple and None in typ:
			pass
		else:
			self.error("%s cannot be unset %r" % (fvar,typ))
			return
		del obj.settings[var]

	def set_layout(self,oldval,newval):
		if newval not in ("plain","icr","irc","vertical","horizontal"):
			self.settings["layout"]=oldval
			return
		getattr(self,"layout_"+newval)()
		if self.status_window:
			self.status_window.set_buffer(self.status_buf)
		elif self.main_window:
			self.main_window.set_buffer(self.status_buf)
		self.send_event("layout changed",newval)
		self.screen.redraw()
			
	def cmd_save(self,args):
		filename=args.shift()
		args.finish()
		self.save(filename)
		
	def save(self,filename=None):
		if filename is None:
			filename=".cjcrc"
		self.info(u"Saving settings to "+filename)
		try:
			f=file(filename,"w")
		except IOError,e:
			self.error(u"Couldn't open config file: "+str(e))
			return

		for plugin in [None]+self.plugins.keys():
			if plugin is None:
				obj=self
			else:
				obj=self.plugins[plugin]
			for var in obj.available_settings:
				descr,typ=obj.available_settings[var][:2]
				val=obj.settings.get(var)
				if val is None:
					continue
				if plugin is not None:
					var="%s.%s" % (plugin,var)
				args=commands.CommandArgs(var)
				if type(typ) is tuple:
					typ=typ[0]
				if typ is list:
					val=string.join(val,",")
				elif typ is pyxmpp.JID:
					val=val.as_string()
				elif typ is unicode:
					val=val.encode("utf-8")
				args.add_quoted(str(val))
				print >>f,args.all()

	def cmd_load(self,args):
		filename=args.shift()
		args.finish()
		self.load(filename)
		
	def load(self,filename=None):
		if filename is None:
			filename=".cjcrc"
		try:
			f=file(".cjcrc","r")
		except IOError,e:
			self.warning("Couldn't open config file: "+str(e))
			return
		
		for l in f.readlines():
			if not l:
				continue
			l=l.split("#",1)[0].strip()
			if not l:
				continue
			try:
				args=commands.CommandArgs(unicode(l,"utf-8"))
				self.cmd_set(args)
			except (ValueError,UnicodeError):
				self.warning(
					"Invalid config directive %r ignored" % (l,))
		f.close()

	def cmd_redraw(self,args):
		self.screen.redraw()
	
	def cmd_info(self,args):
		jid=args.shift()
		if not jid:
			self.error("JID missing")
			return
		args.finish()
		try:
			jid=pyxmpp.JID(jid)
		except pyxmpp.JIDError:
			self.error("Invalid jabber id")
		uinf=self.get_user_info(jid)
		if uinf is None:
			self.info(u"I know nothing about "+jid.as_unicode())
			return
		self.info(u"Information known about %s:" % (jid.as_unicode(),))
		for k,v in uinf.items():
			if not self.info_handlers.has_key(k):
				continue
			r=self.info_handlers[k](k,v)
			if not r:
				continue
			self.info(u"  %s: %s" % r)

	def cmd_help(self,args):
		cmd=args.shift()
		if not cmd:
			self.info("Available commands:")
			commands=self.commands()
			if commands:
				self.info("  Global commands:")
				for cmd in commands:
					self.info(u"    /"+cmd)
			commands=self.screen.commands()
			if commands:
				self.info("  Screen commands:")
				for cmd in commands:
					self.info(u"    /"+cmd)
			win=self.screen.active_window
			if not win:
				return
			commands=win.commands()
			if commands:
				self.info(u"  commands for window '%s':" % (win.description(),))
				for cmd in commands:
					self.info(u"    /"+cmd)
			return

		if cmd[0]=="/":
			cmd=cmd[1:]
		try:
			handler,usage,descr=self.get_command_info(cmd)
		except KeyError:
			try:
				handler,usage,descr=self.screen.get_command_info(cmd)
			except KeyError:
				if self.screen.active_window:
					win=self.screen.active_window
					try:
						handler,usage,descr=win.get_command_info(cmd)
					except KeyError:
						self.error(u"Unknown command: "+`cmd`)
						return
				else:
					self.error(u"Unknown command: "+`cmd`)
					return
		
		self.info("Usage:")
		if type(usage) in (ListType,TupleType):
			for u in usage:
				self.info(u"   "+u)
		else:
			self.info(u"   "+usage)
		self.info(u"  "+descr)

	def cmd_theme(self,args):
		self.theme_manager.command(args)

	def exit_request(self,reason):
		if self.stream:
			if reason:
				self.info(u"Disconnecting (%s)..." % (reason,))
			else:
				self.info(u"Disconnecting...")
			self.send_event("disconnect request",reason)
			time.sleep(self.settings["disconnect_delay"])
			self.disconnect()
		self.state_changed.acquire()
		self.exiting=time.time()
		self.state_changed.notify()
		self.state_changed.release()

	def exit_time(self):
		if not self.exiting:
			return 0
		if not self.stream:
			return 1
		if self.exiting>time.time()+self.settings["disconnect_timeout"]:
			return 1
		return 0

	def ui_loop(self):
		while not self.exit_time():
			try:
				self.screen.keypressed()
			except (KeyboardInterrupt,SystemExit),e:
				self.exit_request(str(e))
				self.print_exception()
		print >>logfile,"UI loop exiting"

	def stream_loop(self):
		while not self.exit_time():
			self.state_changed.acquire()
			stream=self.stream
			if not stream:
				self.state_changed.wait(1)
				stream=self.stream
			self.state_changed.release()
			if not stream:
				continue
			try:
				self.stream.loop_iter(1)
			except (KeyboardInterrupt,SystemExit),e:
				self.exit_request(unicode(str(e)))
				self.print_exception()
		print >>logfile,"Stream loop exiting"

	def main_loop(self):
		while not self.exit_time():
			try:
				self.state_changed.acquire()
				self.state_changed.wait(1)
				self.state_changed.release()
			except (KeyboardInterrupt,SystemExit),e:
				self.exit_request(unicode(str(e)))
				self.print_exception()
		print >>logfile,"Main loop exiting"
		
	def get_user(self,name):
		if name.find("@")>=0:
			if self.roster:
				try:
					ritems=self.roster.items_by_name(name)
				except KeyError:
					ritems=None
				if ritems:
					if len(ritems)==1:
						return ritems[0].jid()
			try:
				return pyxmpp.JID(name)
			except pyxmpp.JIDError:
				self.error(u"Invalid JID: %s" % (name,))
				return None

		if not self.roster:
			self.error(u"%s not found in roster" % (name,))
			return None

		try:
			ritems=self.roster.items_by_name(name)
		except KeyError:
			self.error(u"%s not found in roster" % (name,))
			return None
		
		if ritems:
			if len(ritems)>1:
				self.error("ambiguous user name")
				return None
			else:
				return ritems[0].jid()
		return None

	def get_bare_user_info(self,jid,var=None):
		if jid.resource:
			jid=jid.bare()
		ujid=jid.as_unicode()
		if not self.user_info.has_key(ujid):
			return None
		if var is None:
			return self.user_info[ujid]
		return self.user_info[ujid].get(var)

	def get_user_info(self,jid,var=None):
		uinf=self.get_bare_user_info(jid).copy()
		if uinf is None:
			return None
		if uinf.has_key("resources") and uinf["resources"].has_key(jid.resource):
			uinf.update(uinf["resources"][jid.resource])
		if var is None:
			return uinf
		return uinf.get(var)

	def set_user_info(self,jid,var,val):
		bare=jid.bare()
		ubare=bare.as_unicode()
		if self.user_info.has_key(ubare):
			uinf=self.user_info[ubare]
			if not uinf.has_key("resources"):
				uinf["resources"]={}
		else:
			uinf={"resources":{},"jid":bare}
			self.user_info[ubare]=uinf

		if uinf["resources"].has_key(jid.resource):
			fuinf=uinf["resources"][jid.resource]
		else:
			fuinf={"jid":jid}
			uinf["resources"][jid.resource]=fuinf
		fuinf[var]=val
	
	def set_bare_user_info(self,jid,var,val):
		bare=jid.bare()
		ubare=bare.as_unicode()
		if self.user_info.has_key(ubare):
			uinf=self.user_info[ubare]
		else:
			uinf={"jid":bare}
			self.user_info[ubare]=uinf
		uinf[var]=val

	def roster_updated(self,jid=None):
		if jid is None:
			self.info("Got roster")
		else:
			self.debug("Roster updated")
		self.send_event("roster updated",jid)

	def idle(self):
		pyxmpp.Client.idle(self)
		self.send_event("idle")
			
	def print_exception(self):
		if logfile:
			traceback.print_exc(file=logfile)
		traceback.print_exc(file=self.status_buf)
			
	def error(self,s):
		if logfile:
			print >>logfile,time.asctime(),"ERROR",s.encode("utf-8","replace")
		self.status_buf.append_themed("error",s)
		self.status_buf.update(1)
		
	def warning(self,s):
		if logfile:
			print >>logfile,time.asctime(),"WARNING",s.encode("utf-8","replace")
		self.status_buf.append_themed("warning",s)
		self.status_buf.update(1)
		
	def info(self,s):
		if logfile:
			print >>logfile,time.asctime(),"INFO",s.encode("utf-8","replace")
		self.status_buf.append_themed("info",s)
		self.status_buf.update(1)

	def debug(self,s):
		if logfile:
			print >>logfile,time.asctime(),"DEBUG",s.encode("utf-8","replace")
		#self.status_buf.append_themed("debug",s)
		#self.status_buf.update(1)


def main():
	locale.setlocale(locale.LC_ALL,"")
	app=Application()
	try:
		screen=ui.init()
		app.run(screen)
	finally:
		print >>logfile,"Cleaning up"
		ui.deinit()
		print >>logfile,"Cleaned up"
