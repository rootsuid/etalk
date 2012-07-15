#!/usr/bin/env python
#
#
# ,/etalk host port
# ./etalk host
# ./etalk (listen)
import sys
import curses
from etalk import *
try:
  if len(sys.argv) == 3:
    client=EtalkClient()
    client.start()
    client.connect_etalk(sys.argv[1],sys.argv[2])
  if len(sys.argv) == 2:
    client=EtalkClient()
    client.start()
    client.connect_etalk(sys.argv[1])
  if len(sys.argv) == 1:
    server=EtalkServer()
    server.start()

except KeyboardInterrupt:
  curses.endwin()
  sys.exit()
  print "Keyboard Interupt - Exiting cleanly"

except:
#  if not(curses.isendwin()): curses.endwin()
  raise




