
import curses
import curses.textpad
import string

from widget import Widget
from cjc import common


class EditLine(Widget):
	def __init__(self):
		Widget.__init__(self)
		self.win=None
		self.capture_rest=0
		self.content=u""
		self.pos=0
		self.offset=0
		
	def set_parent(self,parent):
		Widget.set_parent(self,parent)
		self.screen.lock.acquire()
		try:
			self.win=curses.newwin(self.h,self.w,self.y,self.x)
			self.win.keypad(1)
			self.screen.set_default_key_handler(self)
		finally:
			self.screen.lock.release()
		self.printable=string.digits+string.letters+string.punctuation+" "

	def get_height(self):
		return 1

	def keypressed(self,c,escape):
		self.screen.lock.acquire()
		try:
			return self._keypressed(c,escape)
		finally:
			self.screen.lock.release()
		
	def _keypressed(self,c,escape):
		if escape:
			common.debug("Key: 27 %i" % (c,))
			return
		common.debug("Key: %i" % (c,))
		if c==curses.KEY_ENTER:
			return self.key_enter()
		elif c==curses.KEY_LEFT:
			return self.key_left()
		elif c==curses.KEY_RIGHT:
			return self.key_right()
		elif c==curses.KEY_BACKSPACE:
			return self.key_bs()
		elif c==curses.KEY_DC:
			return self.key_del()
		elif c>255 or c<0:
			curses.beep()
			return
		c=chr(c)
		if c in ("\n\r"):
			self.key_enter()
		elif c=="\b":
			self.key_bs()
		elif c=="\x7f":
			self.key_del()
		if c in self.printable:
			self.key_char(c)
		else:
			curses.beep()
		
	def key_enter(self):
		self.screen.user_input(self.content)
		self.content=u""
		self.pos=0
		self.offset=0
		self.win.clear()
		self.win.refresh()

	def key_left(self):
		if self.pos<=0:
			curses.beep()
			return
		self.pos-=1
		self.win.move(0,self.pos-self.offset)
		self.win.refresh()

	def key_right(self):
		if self.pos>=len(self.content):
			curses.beep()
			return
		self.pos+=1
		self.win.move(0,self.pos-self.offset)
		self.win.refresh()

	def key_bs(self):
		if self.pos<=0:
			curses.beep()
			return
		self.content=self.content[:self.pos-1]+self.content[self.pos:]
		self.pos-=1
		self.win.move(0,self.pos-self.offset)
		self.win.delch()
		self.win.refresh()

	def key_del(self):
		if self.pos>=len(self.content):
			curses.beep()
			return
		self.content=self.content[:self.pos]+self.content[self.pos+1:]
		self.win.delch()
		self.win.refresh()

	def key_char(self,c):
		c=unicode(c,self.screen.encoding,"replace")
		if self.pos==len(self.content):
			self.content+=c
			self.win.addstr(c.encode(self.screen.encoding))
		else:
			self.content=self.content[:self.pos]+c+self.content[self.pos:]
			self.win.insstr(c.encode(self.screen.encoding))
			self.win.move(0,self.pos-self.offset+1)
		self.pos+=1
		self.win.refresh()

	def update(self,now=1):
		self.screen.lock.acquire()
		try:
			self.win.cursyncup()
			if now:
				self.win.refresh()
			else:
				self.win.noutrefresh()
		finally:
			self.screen.lock.release()

	def cursync(self):
		self.screen.lock.acquire()
		try:
			self.win.cursyncup()
			self.win.refresh()
		finally:
			self.screen.lock.release()
