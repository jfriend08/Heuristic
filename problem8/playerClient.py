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
    self.W = np.zeros(self.N)

  def flip(self, arr, compFunc):
    idx = []
    for i in xrange(len(arr)):
      if compFunc(arr[i]):
        idx.append(i)

    if len(idx) >= 2:
      idx1, idx2 = random.sample(idx, 2)
      minNum = min(abs(arr[idx1]), abs(arr[idx2]))
      res = minNum * 0.2
      print '{0} and {1} flip for {2}'.format(arr[idx1], arr[idx2], res)
      arr[idx1] += res
      arr[idx2] -= res

  def dataReceived(self, data):
    print "data\n", data, "\n------------------------\n"
    if data.find('continue') == -1:
      reactor.stop()

    now = np.copy(self.W)
    numSet = int(self.N * 0.05) / 2
    if numSet == 1:
      flipNegative = random.randint(0, 1) == 0
      if flipNegative:
        self.flip(now, lambda a: a < 0)
      else:
        self.flip(now, lambda a: a > 0)

    elif numSet == 2:
      self.flip(now, lambda a: a < 0)
      self.flip(now, lambda a: a > 0)

    strs = ' '.join(map(lambda x: str(round(x, 2)), now))
    print 'Now Preference:\n{0}'.format(strs)
    self.transport.write(strs)

  def connectionMade(self):
    self.W = self.getDenseInitW()
    strs = ' '.join(map(lambda x: str(round(x, 2)), self.W))
    print 'Init:\n{0}'.format(strs)
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
    random.seed()
    numbers = [0] * self.N
    negative = self.N / 2
    acm = -1.0

    for i in xrange(negative-1):
      now = round(float(random.randint(1, 100) % 100) / 100, 2)
      while now > abs(acm) / 8.0:
        now = round(float(random.randint(1, 100) % 100) / 100, 2)
      numbers[i] = -now
      acm -= numbers[i]
    numbers[negative-1] = acm

    acm = 1.0
    for i in xrange(negative, self.N-1):
      now = round(float(random.randint(0, 100) % 100) / 100, 2)
      while now > acm / 8.0:
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
