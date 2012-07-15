import socket, ssl
import asyncore
import collections
import threading
from EtalkScreen import *
from EtalkDispatcher import *

class EtalkUser(EtalkDispatcher,asyncore.dispatcher):
  def println(self,s): print str(s)
  def __init__(self, server, conn, address,w):
    self.window=w
    EtalkDispatcher.__init__(self)
    self.server=server
    asyncore.dispatcher.__init__(self, conn)
    self.socket = ssl.wrap_socket(conn,
                                 server_side=True,
                                 do_handshake_on_connect=False,
                                 certfile="cert",
                                 keyfile="key",
                                 ssl_version=ssl.PROTOCOL_TLSv1)

    self.host = address
    self.outbox = collections.deque()
  def write(self, message):
    self.outbox.append(message)

  def handle_read(self):
    if not self.established: self._handshake(); return
    self.window.addstr(self.recv(1024))
  def handle_write(self):
    if not self.established: self._handshake(); return
    if not self.outbox: return
    message = self.outbox.popleft()
    self.send(message)
  def handle_close(self):
    asyncore.dispatcher.close(self)
    self.server.remove_client(self)


class EtalkServer(asyncore.dispatcher,EtalkScreen,threading.Thread):
  def __init__(self,port=1776):
    threading.Thread.__init__(self)
    self.setDaemon(True)
    EtalkScreen.__init__(self)
    asyncore.dispatcher.__init__(self)
    self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
    self.bind(('0.0.0.0', port))
    self.listen(1)
    self.remote_clients = []
  def remove_client(self,client):
    try:
      self.remote_clients.remove(client)
      self.remove_window(client.host)
    except:
      return
  def handle_accept(self):
    conn, fromaddr = self.accept()
    w=self.make_window(str(fromaddr))
    self.refresh()
    self.remote_clients.append(EtalkUser(self,conn,fromaddr,w))
  def handle_read(self):
    
    return
  def broadcast(self, message):
    for remote_client in self.remote_clients:
        remote_client.write(message)

  def client_recv(self,connstream):
      data=True
      while data:
          data = connstream.read()
          print data
  def run(self):
    asyncore.loop()
    
  def start(self):
    EtalkScreen.start(self)
    threading.Thread.start(self)
    self.input_loop()
  def input_loop(self):
    while 1:
      c = self.stdscr.getch()
      self.process_key(c)
      if c<0: continue
      if c<256:
        self.my_window.addstr(chr(c))
        self.broadcast(chr(c))
