import sys, os, re
import signal
import random
import argparse
from twisted.internet import reactor, protocol
import numpy as np
import gradientDescent as gd
from sklearn import preprocessing

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
      X = np.array([elm[:self.N] for elm in data], dtype=float)
      y = np.array([elm[self.N+2] for elm in data], dtype=float)
      print "X.shape", X.shape
      print "Before norm", X
      min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1), copy=True)
      X = min_max_scaler.fit_transform(X)
      print "After norm", X
      n, dim = X.shape
      w = np.zeros(dim)
      mygd = gd.gradientDescent(X, y)
      wIter, w, iterCount = mygd.my_gradient_decent(w, maxiter=50000, ita=0.1, c=1, Step_backtrack=True)
      print "w", w, "iterCount", iterCount
      for predict, target in zip(map(lambda x:np.dot(w,x), X), y):
        print predict, target


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
