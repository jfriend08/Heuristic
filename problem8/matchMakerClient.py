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
    self.bw = None
    self.bestAccuracy = None
    self.isvwbest = None

  def dataReceived(self, data):
    if data != "gameover":
      self.parseAndGD(data)
      candidate = self.makeCandidate();
      candidateString = ' '.join(str(x) for x in candidate)
      print "sending candidate", candidateString, "\ncandidate length:", len(candidate)
      self.transport.write(candidateString)
    else:
      print "GAMEOVER"

  def makeCandidate(self):
    candidate = [(round(-1, 4) if w<0 else round(1, 4)) for w in (self.vw if self.isvwbest else self.bw)]
    # candidate = [(round(-1*self.bestAccuracy, 4) if w<0 else round(1*self.bestAccuracy, 4)) for w in (self.vw if self.isvwbest else self.bw)]
    # candidate = [(round(-1*self.bestAccuracy, 4) if w<0 else round(1*self.bestAccuracy, 4)) for w in (self.vw if self.isvwbest else self.bw)]
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
    else:
      data = map(lambda x:re.split('\s+|\|', x), data)
      del data[-1]
      newx = np.array([elm[:self.N] for elm in data], dtype=float)
      newy = np.array([elm[self.N+2] for elm in data], dtype=float)
      self.X = np.concatenate((self.X, newx))
      self.y = np.append(self.y, newy)

    x = np.copy(self.X)
    y = np.copy(self.y)
    self.bw = self.thinkBinaryGD(x, y)
    self.vw = self.thinkValueGD(x, y)
    # print "self.bw\n", ",".join(str(x) for x in self.bw), "\nself.vw:\n", ",".join(str(x) for x in self.vw)
    # print "len(self.bw)", len(self.bw), "len(self.vw)",len(self.vw)
    accu_b = self.getAccuracy(self.bw, self.y)
    accu_v = self.getAccuracy(self.vw, self.y)
    print "Binary Sign Accuracy:", accu_b, "Value Sign Accuracy:", accu_v
    # print "len(self.bw)", len(self.bw), "len(self.vw)",len(self.vw)
    self.bestAccuracy = (accu_b if accu_b > accu_v else accu_v)
    self.isvwbest = (False if accu_b > accu_v else True)
    # self.makePlot(vw)

  def getAccuracy(self, inputx, target):
    diff = np.apply_along_axis(lambda x:x[0]*x[1], 1, zip(target, inputx))
    return len(np.where(diff>0)[0])/float(len(diff))

  def thinkValueGD(self, X, y):
    #TODO: grid search for minimize loss function
    X_new = np.apply_along_axis(lambda x:np.append(x,0),1,X)
    n, dim = X_new.shape
    w = np.zeros(dim)
    mygd = gd.gradientDescent(X_new, y)
    wIter, w, iterCount = mygd.my_gradient_decent(w, maxiter=3000, ita=0.05, c=1, Step_backtrack=False)
    return np.delete(w, -1, 0)
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
    # print "thinkBinaryGD X.shape", X.shape, "w.shape", w.shape
    mygd = gdII.gradientDescent(X_norm, y_norm)
    wIter, resultw, iterCount = mygd.my_gradient_decent(w, maxiter=10000, ita=0.3, c=1, Step_backtrack=False)
    # print "len(resultw)", len(resultw)
    return resultw

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
