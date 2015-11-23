import sys, os, re
import signal
import random
import argparse
from twisted.internet import reactor, protocol
import numpy as np
import gradientDescent as gd
import gradientDescentII as gdII
from sklearn import preprocessing
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

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
      print "X.shape", X.shape, "y.shape", y.shape
      solution = np.linalg.solve(X, y)
      print "w solution:", solution
      '''Get the sign w, but seems vw performed better'''
      # wBinary = self.thinkBinaryGD(X, y)
      # diff = np.apply_along_axis(lambda x:x[0]*x[1], 1, zip(solution, wBinary))
      # print "Accuracy:", len(np.where(diff>0)[0])/float(len(diff))
      # print "wBinary:\n", wBinary

      vw = self.thinkValueGD(X, y)
      print "vw.shape", vw.shape
      diff = np.apply_along_axis(lambda x:x[0]*x[1], 1, zip(solution, vw))
      print "Accuracy:", len(np.where(diff>0)[0])/float(len(diff))
      print "vw:\n", vw
      plt.figure(1)
      plt.subplot(211)
      plt.plot(vw, 'r--')
      plt.title('Loss function')
      plt.ylabel('Value')
      plt.xlabel('yt')
      plt.subplot(212)
      plt.plot(solution, 'b--')
      plt.show()


  def thinkValueGD(self, X, y):
    X_new = np.apply_along_axis(lambda x:np.append(x,0),1,X)
    # X_new = np.copy(X)
    print "X_new.shape", X_new.shape
    n, dim = X_new.shape
    w = np.zeros(dim)
    mygd = gd.gradientDescent(X_new, y)
    wIter, w, iterCount = mygd.my_gradient_decent(w, maxiter=50000, ita=0.11, c=1, Step_backtrack=False)
    print "result w:", w
    return w
    # for i in xrange(5):
    #   w = np.random.rand(1, dim).flatten()
    #   print "Testing w", w
    #   print i, "th checking: error sum\n", mygd.grad_checker(w)
    #   print "----------------------"
  def thinkBinaryGD(self, X, y):
    min_max_scaler = preprocessing.MinMaxScaler(feature_range=(-1, 1), copy=True)
    X_norm = min_max_scaler.fit_transform(X)
    y_norm = np.array([ (1 if each>=0 else -1) for each in y])
    n, dim = X.shape
    w = np.zeros(dim)
    mygd = gdII.gradientDescent(X_norm, y_norm)
    wIter, w, iterCount = mygd.my_gradient_decent(w, maxiter=50000, ita=0.1, c=1, Step_backtrack=False)
    product = np.apply_along_axis(lambda x: np.dot(w,x[0])*x[1], 1, zip(X_norm,y_norm) )
    print "Accuracy1:", len(np.where(product>0)[0])/float(len(product))
    return w

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
