import sys, os, re
import signal
import random
from twisted.internet import reactor, protocol
import numpy as np
import gradientDescent as gd
import gradientDescentII as gdII
from sklearn import preprocessing
import argparse
# from sklearn.decomposition import PCA
# import matplotlib.pyplot as plt


class Client(protocol.Protocol):
  """Random Client"""
  def __init__(self, N):
    self.N = int(N)
    self.X = None
    self.y = None
    self.w = None
    self.vw = None
    self.bw = None
    self.bestAccuracy = None
    self.isvwbest = None
    self.iter = 0
    self.itaV = None
    self.itaB = None
    self.candidates = []
    self.maxiterV = 2500
    self.maxiterB = 500

  def dataReceived(self, data):
    if data != "gameover":
      self.parseAndGD(data)
      candidate = self.makeCandidate();
      candidateString = ' '.join(str(x) for x in candidate)
      # print "sending candidate", candidateString, "\ncandidate length:", len(candidate)
      self.transport.write(candidateString)
      self.iter += 1
    else:
      print "GAMEOVER"

  def makeCandidate(self):
    # if self.isvwbest:
    #   X = np.copy(self.vw)
    #   min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 1), copy=True)
    #   score_norm = min_max_scaler.fit_transform([X])
    #   print "self.vw\n", X, "\nscore_norm:\n", score_norm
    #   candidate = score_norm
    # else:
    #   candidate = [(round(0, 4) if w<0 else round(1, 4)) for w in (self.vw if self.isvwbest else self.bw)]
    # candidate = []
    # if self.isvwbest:
    #   iteratable = zip(self.vw,self.bw)
    # else:
    #   iteratable = zip(self.bw,self.vw)

    # for w in iteratable:
    #   if w[0]<0 and w[0]*w[1]>=0:
    #     candidate.append(0)
    #   elif w[0]>0 and w[0]*w[1]>=0:
    #     candidate.append(1)
    #   else:
    #     candidate.append(0.5)

    # candidate = [(round(0, 4) if w[0]<0 and w[0]*w[1]>=0 elif w[0]>0 and w[0]*w[1]>=0 round(1, 4) else round(0.5, 4) ) for w in (zip(self.vw,self.bw) if self.isvwbest else (self.bw,self.vw))]
    candidate = [(round(0, 4) if w<0 else round(1, 4)) for w in (self.vw if self.isvwbest else self.bw)]

    if candidate in self.candidates:
      randlist = np.random.permutation(len(candidate))
      print "before rand change:", candidate
      for idx in randlist[:5]:
        candidate[idx] = (0 if candidate[idx] >0 else 1)
      print "after rand change:", candidate
      self.maxiterV = (self.maxiterV*1.0001 if self.maxiterV<1.5*self.maxiterV else self.maxiterV)
      # self.maxiterB = (self.maxiterB*1.01 if self.maxiterB<1.5*self.maxiterB else self.maxiterB)
    self.candidates.append(candidate)
    # candidate = [(round(-1*self.bestAccuracy, 4) if w<0 else round(1*self.bestAccuracy, 4)) for w in (self.vw if self.isvwbest else self.bw)]
    # candidate = [(round(-1*self.bestAccuracy, 4) if w<0 else round(1*self.bestAccuracy, 4)) for w in (self.vw if self.isvwbest else self.bw)]
    return candidate

  def parseAndGD(self, data):
    print "data\n", data
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
    self.vw = self.thinkValueGD(x, y)
    self.bw = self.vw
    # self.bw = self.thinkBinaryGD(x, y)
    # print "self.bw\n", ",".join(str(x) for x in self.bw), "\nself.vw:\n", ",".join(str(x) for x in self.vw)
    # print "len(self.bw)", len(self.bw), "len(self.vw)",len(self.vw)
    accu_v = self.getAccuracy(self.vw, self.y)
    accu_b = accu_v
    print "Binary Sign Accuracy:", accu_b, "Value Sign Accuracy:", accu_v
    # print "len(self.bw)", len(self.bw), "len(self.vw)",len(self.vw)
    self.bestAccuracy = (accu_b if accu_b > accu_v else accu_v)
    self.isvwbest = (False if accu_b > accu_v else True)
    # self.makePlot(vw)

  def compute_obj(self, w):
    n = self.X.shape[0]
    wx = np.apply_along_axis(lambda x: np.dot(w, x), 1, self.X)
    return (1/float(2*n)) * np.sum(np.apply_along_axis(lambda x: (x[0]-x[1])**2, 1, zip(wx,self.y)))

  def getAccuracy(self, inputx, target):
    diff = np.apply_along_axis(lambda x:x[0]*x[1], 1, zip(target, inputx))
    return len(np.where(diff>0)[0])/float(len(diff))

  def thinkValueGD(self, X, y):
    #TODO: grid search for minimize loss function
    X_new = np.apply_along_axis(lambda x:np.append(x,0),1,X)
    n, dim = X_new.shape
    w = np.zeros(dim)
    # w = np.random.random_sample((dim,))
    # w = (self.w if self.w!= None else np.zeros(dim))
    mygd = gd.gradientDescent(X_new, y)
    if self.iter >= 0:
      bestIta = -1
      bestw = None
      bestAccuracy = -100
      for ita in [0.2, 0.15, 0.13, 0.12, 0.11, 0.09, 0.07, 0.05, 0.03, 0.01]:
        # averagedwIter, allw, w, iterCount = mygd.my_sgd(w, maxiter=50, ita=ita, c=1, Step_backtrack=False, stopMethod="performance")
        wIter, w, iterCount = mygd.my_gradient_decent(w, maxiter=10, ita=ita, c=1, Step_backtrack=False)
        accu_b = self.getAccuracy(w, self.y)
        # accu_b = self.compute_obj(np.delete(w, -1, 0))
        if bestAccuracy < accu_b:
          bestAccuracy = accu_b
          bestw = w
          bestIta = ita
      print "thinkValueGD ita update:", self.itaV, "-->", bestIta, "bestAccuracy", bestAccuracy
      self.itaV = bestIta
      w = bestw

    # averagedwIter, allw, w, iterCount = mygd.my_sgd(w, maxiter=self.maxiterV, ita=self.itaV, c=1, Step_backtrack=False, stopMethod="performance")
    # print "Done iterCount:", iterCount

    wIter, w, iterCount = mygd.my_gradient_decent(w, maxiter=self.maxiterV, ita=self.itaV, c=1, Step_backtrack=False, stopMethod="optimize")
    # self.w = w
    # accuracy = gd.getAccuracyOverIteration(wIter, X_new, y)
    print "iterCount:", iterCount
    # print "thinkValueGD accuracy", accuracy, "\niterCount:", iterCount
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
    if self.iter >= 0:
      bestIta = -1
      bestw = None
      bestAccuracy = sys.float_info.max
      for ita in [0.2, 0.18, 0.17, 0.16, 0.15, 0.13, 0.11, 0.1, 0.07, 0.05, 0.03]: #good for dim 38
        wIter, w, iterCount = mygd.my_gradient_decent(w, maxiter=50, ita=ita, c=1, Step_backtrack=False)
        # accu_b = self.getAccuracy(w, self.y)
        accu_b = self.compute_obj(w)
        if bestAccuracy < accu_b:
          bestAccuracy = accu_b
          bestw = w
          bestIta = ita
      print "thinkBinaryGD ita update:", self.itaB, "-->", bestIta, "bestAccuracy", bestAccuracy
      self.itaB = bestIta
      resultw = bestw
    wIter, resultw, iterCount = mygd.my_gradient_decent(w, maxiter=self.maxiterB, ita=self.itaB, c=1, Step_backtrack=False)
    # print "len(resultw)", len(resultw)
    # accuracy = gdII.getAccuracyOverIteration(wIter, X_norm, y_norm)
    # print "thinkBinaryGD accuracy", accuracy
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
