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
    self.X = None
    self.y = None
    self.vw = None

  def dataReceived(self, data):
    if data != "gameover":
      self.parseAndGD(data)
      candidate = self.makeCandidate();
      del candidate[-1]
      candidateString = ' '.join(str(x) for x in candidate)
      print "sending candidate", candidateString
      self.transport.write(candidateString)
    else:
      print "GAMEOVER"

  def makeCandidate(self):
    candidate = [(0 if w<0 else round(w/2, 4)) for w in self.vw]
    return candidate

  def parseAndGD(self, data):
    print "data\n", data, "\n------------------------\n"
    data = re.split('\n+', data)
    if len(data) > 10:
      data = map(lambda x:re.split('\s+|\|', x), data)
      del data[-1]
      X = np.array([elm[:self.N] for elm in data], dtype=float)
      y = np.array([elm[self.N+2] for elm in data], dtype=float)
      self.X = X
      self.y = y
      print "X.shape", X.shape, "y.shape", y.shape
      '''Get the sign w, but seems vw performed better'''
      # bw = self.thinkBinaryGD(X, y)

      vw = self.thinkValueGD(X, y)
      self.vw = vw
      print "vw.shape", vw.shape, "vw:\n", vw
      # solution = np.linalg.solve(X, y)
      # print "w solution:", solution
      diff = np.apply_along_axis(lambda x:x[0]*x[1], 1, zip(self.y, vw))
      print "Sign Accuracy:", len(np.where(diff>0)[0])/float(len(diff))
      self.makePlot(vw)
      print "self.X.shape", self.X.shape
    else:
      data = map(lambda x:re.split('\s+|\|', x), data)
      del data[-1]
      newx = np.array([elm[:self.N] for elm in data], dtype=float)
      newy = np.array([elm[self.N+2] for elm in data], dtype=float)
      self.X = np.concatenate((self.X, newx))
      self.y = np.append(self.y, newy)
      # solution = np.linalg.solve(self.X, self.y)
      vw = self.thinkValueGD(self.X, self.y)
      print "vw.shape", vw.shape, "vw:\n", vw
      diff = np.apply_along_axis(lambda x:x[0]*x[1], 1, zip(self.y, vw))
      print "Sign Accuracy:", len(np.where(diff>0)[0])/float(len(diff))
      self.makePlot(vw)

  def thinkValueGD(self, X, y):
    #TODO: grid search for minimize loss function
    X_new = np.apply_along_axis(lambda x:np.append(x,0),1,X)
    print "X_new.shape", X_new.shape
    n, dim = X_new.shape
    w = np.zeros(dim)
    mygd = gd.gradientDescent(X_new, y)
    wIter, w, iterCount = mygd.my_gradient_decent(w, maxiter=50000, ita=0.05, c=1, Step_backtrack=False)
    return w
    # for i in xrange(5):
    #   w = np.random.rand(1, dim).flatten()
    #   print "Testing w", w
    #   print i, "th checking: error sum\n", mygd.grad_checker(w)
    #   print "----------------------"
  def makePlot(self, vw, target=None):
    if target==None:
      plt.plot(vw, 'r--')
      plt.title('w function')
      plt.ylabel('Value')
    else:
      plt.figure(1)
      plt.subplot(211)
      plt.plot(vw, 'r--')
      plt.title('w function')
      plt.ylabel('Value')
      plt.xlabel('each attribute')
      plt.subplot(212)
      plt.plot(solution, 'b--')
    plt.show()
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
