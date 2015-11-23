import sys, os, re
import signal
import random
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
  def __init__(self, N):
    self.N = int(N)

  def dataReceived(self, data):
    print "data\n", data, "\n------------------------\n"
    data = re.split('\n+', data)
    if len(data) > 10:
      data = map(lambda x:re.split('\s+|\|', x), data)
      del data[-1]
      m = np.array([elm[:self.N] for elm in data])
      y = np.array([elm[self.N+2] for elm in data])
      print "y.shape", y.shape
      print y

  def connectionMade(self):
    # self.transport.write('REGISTER: {0}\n'.format(self.name))
    pass

  def connectionLost(self, reason):
    reactor.stop()

class ClientFactory(protocol.ClientFactory):
  """ClientFactory"""
  def __init__(self, N):
    self.N = N

  def buildProtocol(self, addr):
    c = Client(self.N)
    c.addr = addr
    return c

  def clientConnectionFailed(self, connector, reason):
    print "Connection failed - goodbye!"
    reactor.stop()

  def clientConnectionLost(self, connector, reason):
    print "Connection lost - goodbye!"

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("N", help="N elements")
  parser.add_argument("-p", "--port", type=int, default="9696", help="Server port to connect to.")
  args = parser.parse_args()
  N = args.N
  port = args.port
  factory = ClientFactory(N)
  reactor.connectTCP("localhost", port, factory)
  reactor.run()

if __name__ == '__main__':
    main()
