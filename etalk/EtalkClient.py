import socket, ssl, pprint,select
import asyncore
import collections
import threading
from EtalkScreen import *
from EtalkDispatcher import *
class EtalkClient(EtalkScreen,EtalkDispatcher,asyncore.dispatcher,threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.setDaemon(True)

    EtalkScreen.__init__(self)
    EtalkDispatcher.__init__(self)
    asyncore.dispatcher.__init__(self)
    self.outbox = collections.deque()
    self.host=None
    self.port=1776
    self.socket=None
    self.test=True
  def start(self):
    EtalkScreen.start(self)
    return
  def handle_close(self):
    self.socket=self._socket
  def handle_connect(self):
    self._socket = self.socket
    self.set_socket(ssl.wrap_socket(self._socket, do_handshake_on_connect=False))
    self.server_window=self.make_window("server")
    self.refresh()
#    self.println(repr(self.socket.getpeername()))
#    self.println(self.socket.cipher())
#    self.println(pprint.pformat(self.socket.getpeercert()))

#    self.socket.close()

  def handle_read(self):
    if not self.established: self._handshake(); return
    self.server_window.addstr(self.socket.recv(1024))
#    print self.socket.recv(1024)
#    self.print_window("server",self.socket.recv(1024))
  def run(self):
    asyncore.loop()
  def handle_write(self):
    if not self.established: self._handshake(); return
    if self.test:
      self.send("Connected\n\n")
      self.test=False
    if not self.outbox:
      return
    message = self.outbox.popleft()
    self.socket.send(message)

  def connect_etalk(self,host=None,port=None):
    if host!=None: self.host=host
    if port!=None: self.port=int(port)
    self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
    self.println("Connecting... : "+self.host + ":" +str(self.port))
    self.connect((self.host,self.port))

    threading.Thread.start(self)
    self.input_loop()
  def write(self,c):
    self.outbox.append(c)

  def input_loop(self):
    while 1:
      if not self.established: continue
      c = self.stdscr.getch()
      self.process_key(c)
      if c<0: continue
      if c<256:
        self.my_window.addstr(chr(c))
        self.write(chr(c))
