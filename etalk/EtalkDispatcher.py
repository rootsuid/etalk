import ssl
import asyncore
import socket
class EtalkDispatcher(asyncore.dispatcher):
  def __init__(self):
    self.established = False
    self.want_read = self.want_write = True
  def _handshake(self):
    try:
        self.socket.do_handshake()
    except ssl.SSLError as err:
        self.want_read = self.want_write = False
        if err.args[0] == ssl.SSL_ERROR_WANT_READ:
            self.want_read = True
            return
        elif err.args[0] == ssl.SSL_ERROR_WANT_WRITE:
            self.want_write= True
            return
        else:
            raise
    else:
        self.established = True
        self.want_read = self.want_write = True
  def readable(self):
      return self.want_read and asyncore.dispatcher.readable(self)
  def writable(self):
      return self.want_write and asyncore.dispatcher.writable(self)
