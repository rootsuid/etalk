import curses
import curses.textpad
import time
class EtalkWindow:
  def __init__(self,window,name):
    self.window=window
    self.content=window.subwin(1,1)
    self.content.immedok(True)
    self.content.scrollok(True)
    self.name=name
  def addstr(self,s):
    self.content.addstr(str(s))
    
class EtalkScreen:
  def __init__(self):
    self.windows=[]
  def start(self):
    self.stdscr=curses.initscr()
    curses.noecho()
    curses.cbreak()
    self.stdscr.keypad(1)
    self.stdscr.nodelay(1)
    self.stdscr.clear()
    self.stdscr.refresh()
    self.stdscr.immedok(True)
    w=self.make_window("self")
    self.my_window=w
  def find_window(self,name):
    ew=None
    for w in self.windows:
      if w.name == name:
        ew=w
    return ew
  def remove_window(self,name):
    w=self.find_window(name)
    if w != None:
      self.window.remove(w)
      self.resize_children()

  
  def make_window(self,name):
    win=self.stdscr.subwin(0,0)
    win.clear()
    win.immedok(True)
    win.scrollok(True)
    w=EtalkWindow(win,name)
    self.windows.append(w)
    self.resize_children()
    return w
  def println(self,s):
      self.my_window.content.addstr(str(s)+"\n")
  def resize_children(self):
    n=len(self.windows)
    yx=self.stdscr.getmaxyx()
    h= int(yx[0]/n)
    x=yx[1]
    y=0
    if h < 4: return
    if x < 4: return
    for w in self.windows:
      try:
        w.window.resize(h,x)
        w.window.mvderwin(y,0)
        w.content.mvderwin(1,1)
        w.content.resize(h-2,x-2)
        y += h
      except:
        #momentarily, it was bigger than the window
#        time.sleep(1)
        raise
        self.resize_children()
        return
      
    self.refresh()
    for w in self.windows:
      xy=w.window.getmaxyx()
      w.window.clear()
      w.window.box()
      w.content.clear()
    self.refresh()
  def process_key(self,c):
    if c == curses.KEY_F1: self.make_window("x")
    elif c == curses.KEY_RESIZE: self.resize_children()
    elif c == curses.KEY_REFRESH: self.refresh()
    elif c == curses.KEY_F5: self.refresh()

  def refresh(self):
    self.stdscr.touchwin()
    self.stdscr.refresh()
    for w in self.windows:
      w.window.touchwin()
      w.content.touchwin()
      w.window.refresh()
      w.content.refresh()
 

  def exit(self):
    curses.endwin()
    exit()
  def resize(self):
    self.exit()
    
  def test(self):
    self.start()

