import sys, os, re
import signal
import random
import argparse
from twisted.internet import reactor, protocol
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA

class Client(protocol.Protocol):
  """Random Client"""
  def __init__(self, N):
    self.N = int(N)

  def dataReceived(self, data):
    print "data\n", data, "\n------------------------\n"
    

  def connectionMade(self):
    self.W = self.getDenseInitW()
    strs = ' '.join(map(lambda x: str(round(x, 2)), self.W))
    print 'Init:\n{0}'.format(','.join(map(lambda x: str(round(x, 2)), self.W)))
    self.transport.write(strs)

  def getInitW(self):
    random.seed()
    numbers = [0] * self.N
    negative = self.N / 2
    acm = -1.0

    for i in xrange(negative-1):
      now = round(float(random.randint(0, 100) % 100) / 100, 2)
      numbers[i] = -now if now < abs(acm) else 0
      acm -= numbers[i]

    numbers[negative-1] = acm

    acm = 1.0
    for i in xrange(negative, self.N-1):
      now = round(float(random.randint(0, 100) % 100) / 100, 2)
      numbers[i] = now if now < acm else 0
      acm -= numbers[i]
    numbers[-1] = acm

    numbers = np.asarray(numbers)
    rng = np.random.RandomState()

    for i in xrange(self.N):
      permutation = rng.permutation(self.N)
      numbers = numbers[permutation]

    return numbers

  def getDenseInitW(self):
    random.seed(10)
    numbers = [0] * self.N
    negative = self.N / 2
    acm = -1.0

    for i in xrange(negative-1):
      now = round(float(random.randint(0, 100) % 100) / 100, 2)
      while now > abs(acm) / float(self.N / 4) or now == 0:
        now = round(float(random.randint(0, 100) % 100) / 100, 2)
      numbers[i] = -now
      acm -= numbers[i]
    numbers[negative-1] = acm

    acm = 1.0
    for i in xrange(negative, self.N-1):
      now = round(float(random.randint(0, 100) % 100) / 100, 2)
      while now > acm / (self.N / 4.0):
        now = round(float(random.randint(0, 100) % 100) / 100, 2)
      numbers[i] = now
      acm -= numbers[i]
    numbers[-1] = acm

    numbers = np.asarray(numbers)
    rng = np.random.RandomState()

    for i in xrange(self.N):
      permutation = rng.permutation(self.N)
      numbers = numbers[permutation]

    return numbers

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
  parser.add_argument("-p", "--port", type=int, default="6969", help="Server port to connect to.")
  args = parser.parse_args()
  N = args.N
  port = args.port
  factory = ClientFactory(N)
  reactor.connectTCP("localhost", port, factory)
  reactor.run()

if __name__ == '__main__':
    main()