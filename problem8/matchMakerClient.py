import sys, os
import signal
import random
import time
import argparse
from twisted.internet import reactor, protocol
import numpy as np

board_size = 1000

def signal_handler(signum, frame):
    raise Exception("Timed out!")

class TimedOutExc(Exception):
  pass


class Client(protocol.Protocol):
  """Random Client"""
  def __init__(self, name):
    pass

  def dataReceived(self, data):
    pass


  def connectionMade(self):
    # self.transport.write('REGISTER: {0}\n'.format(self.name))
    pass

  def connectionLost(self, reason):
    reactor.stop()

class ClientFactory(protocol.ClientFactory):
  """ClientFactory"""
  def __init__(self, name):
    self.name = name

  def buildProtocol(self, addr):
    c = Client(self.name)
    c.addr = addr
    return c

  def clientConnectionFailed(self, connector, reason):
    print "Connection failed - goodbye!"
    reactor.stop()

  def clientConnectionLost(self, connector, reason):
    print "Connection lost - goodbye!"

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("name", help="Your name")
  parser.add_argument("-p", "--port", type=int, default="9696", help="Server port to connect to.")
  args = parser.parse_args()
  client_name = args.name
  port = args.port
  factory = ClientFactory(client_name)
  reactor.connectTCP("localhost", port, factory)
  reactor.run()

if __name__ == '__main__':
    main()




# from websocket import create_connection
# import json, socket

# port = 9696
# s = socket.socket()
# s.connect(('127.0.0.1', port))

# # mainSocket = create_connection('ws://localhost:127.0.0.1');
# # socketM = create_connection('ws://localhost:9696');

# class MatchMaker(object):
#   def __init__(self):
#     pass


# def main():
#   # hunter = Hunter(3, 5)
#   # socketH.send(json.dumps({'command': 'M'}))

#   gameover = False
#   while gameover is False:
#     cmd = json.loads(s.recv(1024))
#     print "cmd", cmd
#     # gameover = cmd['gameover']
#     # if gameover is False:
#     #   newMove = hunter.make_move(cmd)
#     #   socketH.send(json.dumps(newMove))
#     # else:
#     #   print 'DONE: ' + str(cmd['time'])


# if __name__ == '__main__':
#   main()
