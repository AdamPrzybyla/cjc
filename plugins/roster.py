import string
import curses

import pyxmpp
import pyxmpp.roster

from cjc.plugin import PluginBase
from cjc.ui import ListBuffer

theme_attrs=(
	("roster.available_online", curses.COLOR_YELLOW,curses.COLOR_BLACK,curses.A_BOLD, curses.A_BOLD),
	("roster.available_dnd", curses.COLOR_RED,curses.COLOR_BLACK,curses.A_NORMAL, curses.A_BOLD),
	("roster.available_away", curses.COLOR_YELLOW,curses.COLOR_BLACK,curses.A_NORMAL, curses.A_BOLD),
	("roster.available_xa", curses.COLOR_BLUE,curses.COLOR_BLACK,curses.A_NORMAL, curses.A_BOLD),
	("roster.available_chat", curses.COLOR_GREEN,curses.COLOR_BLACK,curses.A_BOLD, curses.A_BOLD),
	("roster.unavailable", curses.COLOR_WHITE,curses.COLOR_BLACK,curses.A_NORMAL|curses.A_DIM, curses.A_DIM),
)

theme_formats=(
	("roster.group", "%(group)s:"),
	("roster.group_none", "unfiled:"),
	("roster.group_me", "me:"),
	("roster.group_unknown", "not in roster:"),
	("roster.unavailable", "%[roster.unavailable] %(aflag)s%(sflag)s%(name)-20s [%(J:jid:show)s] %(J:jid:status)s"),
	("roster.available", "%[roster.available_%(J:jid:show)s] %(aflag)s%(sflag)s%(name)-20s [%(J:jid:show)s] %(J:jid:status)s"),
)

# virtual groups
VG_ME=1
VG_UNKNOWN=2

class Plugin(PluginBase):
	def __init__(self,app):
		PluginBase.__init__(self,app)
		self.available_settings={
			"show": ("Which items show - list of 'available','unavailable','chat',"
					"'online','away','xa' or 'all'",list,self.set_show),
			}
		self.settings={"show":["all"]}
		app.add_info_handler("rostername",self.info_rostername)
		app.add_info_handler("rostergroups",self.info_rostergroups)
		app.add_event_handler("roster updated",self.ev_roster_updated)
		app.add_event_handler("presence changed",self.ev_presence_changed)
		app.add_event_handler("layout changed",self.ev_layout_changed)
		app.theme_manager.set_default_attrs(theme_attrs)
		app.theme_manager.set_default_formats(theme_formats)
		self.buffer=ListBuffer(app.theme_manager,"Roster")
		self.extra_items=[]

	def info_rostername(self,k,v):
		if not v:
			return None
		return "Roster name",v

	def info_rostergroups(self,k,v):
		if not v:
			return None
		return "Roster groups",string.join(v,",")

	def set_show(self,oldval,newval):
		self.write_all()

	def ev_roster_updated(self,event,arg):
		if not arg:
			for item in self.cjc.roster.items():
				for group,it in self.extra_items:
					if not isinstance(it,pyxmpp.JID) or group!=VG_UNKNOWN:
						continue
					jid=item.jid()
					if group==VG_UNKNOWN and it==jid or it.bare()==jid:
						self.extra_items.remove((VG_UNKNOWN,it))
						if self.buffer.has_key((VG_UNKNOWN,it)):
							self.buffer.remove_item((VG_UNKNOWN,it))
			self.write_all()
			return
		self.update_item(arg)

	def ev_presence_changed(self,event,arg):
		if arg:
			self.update_item(arg)

	def ev_layout_changed(self,event,arg):
		if self.cjc.roster_window:
			self.cjc.roster_window.set_buffer(self.buffer)

	def update_item(self,item):
		if isinstance(item,pyxmpp.JID):
			if self.cjc.roster:
				try:
					item=self.cjc.roster.item_by_jid(item)
				except KeyError:
					try:
						item=self.cjc.roster.item_by_jid(item.bare())
					except KeyError:
						pass
		if isinstance(item,pyxmpp.roster.RosterItem):
			for group in item.groups():
				self.write_item(group,item)
		elif isinstance(item,pyxmpp.JID):
			if item.bare()==self.cjc.jid.bare():
				group=VG_ME
				if not self.buffer.has_key((group,None)):
					self.buffer.insert_themed((group,None),"roster.group_me",{})
			else:
				group=VG_UNKNOWN
				if not self.buffer.has_key((group,None)):
					self.buffer.insert_themed((group,None),"roster.group_unknown",{})
			self.write_item(group,item)
			self.extra_items.append((group,item))
		self.buffer.update()
	
	def write_item(self,group,item):
		if isinstance(item,pyxmpp.JID):
			jid=item
			name=None
			ask=None
			if group==VG_ME:
				subs="both"
			else:
				subs="none"
		else:
			subs=item.subscription()
			jid=item.jid()
			name=item.name()
			ask=item.ask()
			if jid.resource:
				self.cjc.set_user_info(jid,"rostername",name)
			else:
				self.cjc.set_bare_user_info(jid,"rostername",name)
				
		if not name:
			name=jid.as_unicode()
		p={"name":name,"jid":jid}
		pr=self.cjc.get_user_info(jid,"presence")
		if not pr or pr.get_type() and pr.get_type()!="available":
			available=0
			show=None
		else:
			available=1
			show=pr.get_show()
			if not show:
				show="online"

		show_list=self.settings["show"]
		if subs=="remove":
			show_it=0
		elif "all" in show_list:
			show_it=1
		elif "available" in show_list and available:
			show_it=1
		elif "unavailable" in show_list and not available:
			show_it=1
		elif show in show_list and available:
			show_it=1
		else:
			show_it=0

		if not show_it:
			if self.buffer.has_key((group,jid)):
				self.buffer.remove_item((group,jid))
			return
			
		p["ask"]=ask
		if not ask:
			p["aflag"]=" "
		elif ask=="unsubscribe":
			p["aflag"]="-"
		else:
			p["aflag"]="?"
		p["subscription"]=subs
		if subs=="both":
			p["sflag"]=" "
		elif subs=="from":
			p["sflag"]="<"
		elif subs=="to":
			p["sflag"]=">"
		else:
			p["sflag"]="-"
			
		if available:
			self.buffer.insert_themed((group,jid),"roster.available",p)
		else:
			self.buffer.insert_themed((group,jid),"roster.unavailable",p)

	def write_all(self):
		self.buffer.clear()
		groups_added=[]
		for group,item in self.extra_items:
			if group==VG_ME and group not in groups_added:
				self.buffer.insert_themed((group,None),"roster.group_me",{})
			elif group==VG_UNKNOWN and group not in groups_added:
				self.buffer.insert_themed((group,None),"roster.group_unknown",{})
			self.write_item(group,item)
			
		if not self.cjc.roster:
			self.buffer.update()
			return
		groups=self.cjc.roster.groups()
		groups.sort()
		for group in groups:
			if group:
				p={"group":group}
				self.buffer.insert_themed((group,None),"roster.group",p)
			else:
				self.buffer.insert_themed((group,None),"roster.group_none",{})
			for item in self.cjc.roster.items_by_group(group):
				self.write_item(group,item)
		self.buffer.update()

	def session_started(self,stream):
		self.cjc.request_roster()
