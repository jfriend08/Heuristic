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

def deadline(timeout, *args):
  def decorate(f):
    def handler(signum, frame):
      raise TimedOutExc()

    def new_f(*args):
      signal.signal(signal.SIGALRM, handler)
      signal.alarm(timeout)
      return f(*args)
      signal.alarm(0)

    new_f.__name__ = f.__name__
    return new_f
  return decorate

class Client(protocol.Protocol):
  """Random Client"""
  def __init__(self, name):
    self.name = name
    self.prev_moves = []
    self.nodeStates = {}
    self.nodeConCount = []
    self.playerStates = {}
    self.Paths = []
    self.receiveCount = 0
    self.totalNanos = None

  def reset(self):
    print "Reset called"
    self.prev_moves = []

  def make_random_move(self):
    move = None
    while not move:
      x = random.randint(0, board_size-1)
      y = random.randint(0, board_size-1)
      if (x, y) not in self.prev_moves:
        move = (x, y)
    return move

  def parseStates(self, data):
    stateList = data.split("\n")
    startToSavePlayer=False
    # first pass: get states
    for elm in stateList:
      if elm.find("nodeid") != -1:
        continue
      if elm != "START" and elm != "END" and elm != "WAITING" and elm != "":
        if elm.find("PlayerID") == -1:
          states = elm.split(",")
          if not startToSavePlayer:
            self.nodeStates[states[0]] = {'loc':[states[1], states[2]], 'state':states[3], 'linkage':states[4:len(states)]}
          else:
            if self.totalNanos == None:
              self.totalNanos = states[2]
            self.playerStates[states[1]] = {'id':states[0], 'remain':states[2], 'used':states[3] , 'inPlay':states[4] , 'score':states[5]}
        else:
          startToSavePlayer = True

    # second pass: get counts
    self.nodeConCount = [0 for i in xrange(len(self.nodeStates.keys()))]
    for key in self.nodeStates.keys():
      self.nodeConCount[int(key)] =  4 - "".join(self.nodeStates[key]['linkage']).count('null')
    print "PARSE DONE"


  def bfsFindPath(self, visitedIdx, startIdx, directions):
    if self.nodeStates[startIdx]['state']!="FREE":
      pass

    linkList = self.nodeStates[startIdx]['linkage']
    if "".join(linkList).count('null') == 3:
      print "visitedIdx", visitedIdx, "startIdx", startIdx
      visitedIdx.append(startIdx)
      print "visitedIdx", visitedIdx, "startIdx", startIdx
      self.Paths.append(visitedIdx)
      print "self.Paths", self.Paths

    for nodeid in linkList:
      if nodeid != "null" and self.nodeStates[nodeid]['state']=="FREE" and nodeid not in visitedIdx:
        vCopy = visitedIdx[:]
        vCopy.append(startIdx)
        self.bfsFindPath(vCopy, nodeid)

  @deadline(1)
  def bfsHandler(self, visitedIdx, startIdx):
    self.bfsFindPath(visitedIdx, startIdx)

  def bfsFindPath2(self, visitedIdx, startIdx, directions, depth):
    if startIdx == "null":
      return
    if self.nodeStates[startIdx]['state']!="FREE":
      return

    noMoveCount = 0
    noValidCount = 0
    linkList = self.nodeStates[startIdx]['linkage']
    result = []
    for idx in xrange(len(linkList)):
      nodeid = linkList[idx]
      if nodeid =="null" or nodeid in visitedIdx:
        noValidCount+=1
      if nodeid =="null" or nodeid in visitedIdx or idx in directions:
        noMoveCount+=1
        continue
      if self.nodeStates[nodeid]['state']!="FREE":
        continue
      cpV = visitedIdx[:]
      cpDir = directions[:]
      cpV.append(startIdx)
      cpDir.append(idx)
      result.extend(self.bfsFindPath2(cpV, nodeid, cpDir, depth+1))
    if noMoveCount==4:
      return (visitedIdx, directions)
    return result

  def bfsFindPathWithPath(self, visitedIdx, startIdx, directions, depth, counter):
    # print "visitedIdx", visitedIdx, "startIdx", startIdx, "directions", directions, "depth", depth
    noMoveCount = 0
    while noMoveCount != 4:
      currDir = directions[counter%4]
      linkList = self.nodeStates[startIdx]['linkage']
      # print "startIdx"+ startIdx+ "-->", self.nodeStates[startIdx]['linkage']
      # print "counter", counter, "currDir", currDir, "linkList[currDir]", linkList[currDir]
      if linkList[currDir] != "null" and linkList[currDir] not in visitedIdx and startIdx not in visitedIdx:
        visitedIdx.append(startIdx)
        startIdx = linkList[currDir]
        noMoveCount=0
      else:
        noMoveCount+=1
      counter+=1
    visitedIdx.append(startIdx)
    return visitedIdx

  def fillRemainDir(self, dirs):
    remain = []
    for i in xrange(4):
      if i not in dirs:
        remain.append(i)
    dirs.extend(remain)
    return dirs


  def getalldir (self, result):
    newDirs = []
    if not result:
      return newDirs
    for idx in xrange(1,len(result),2):
      newDirs.append(self.fillRemainDir(result[idx]))
    return newDirs

  def thinkMove(self):
    self.Paths = []
    thinkresult = []
    count2Consider = 0
    whileCount = 0
    while len(thinkresult) <= 0 and whileCount<=4:
      count2Consider+=1
      whileCount+=1
      if whileCount==4:
        print "++++++++++ ohohoh ++++++++++"
        print "nodeConCount", self.nodeConCount
        count2Consider = 0
      for i in xrange(len(self.nodeConCount)):
        count = self.nodeConCount[i]
        curNodeIdx = str(i)
        if count == count2Consider:
          result = self.bfsFindPath2([], curNodeIdx, [], 0)
          allDirs = self.getalldir(result)
          # print '----------------------------------------'
          for eachDir in allDirs:
            fullPath = self.bfsFindPathWithPath([], curNodeIdx, eachDir, 0, 0)
            # print "FINAL:", fullPath
            thinkresult.append((fullPath, eachDir))
      thinkresult.sort(key=lambda tup: len(tup[0]))
      print "thinkresult", thinkresult
    if len(thinkresult) == 0:
      return (None, None)
    return thinkresult[-1]



  def code2Letter(self, code):
    if code == 0:
      return "UP"
    elif code ==1:
      return "DOWN"
    elif code ==2:
      return "LEFT"
    else:
      return "RIGHT"

  def dataReceived(self, data):
    self.parseStates(data)
    pos, dirs = self.thinkMove()
    if pos != None:
      myR = pos[0]+","+",".join(map(self.code2Letter, dirs))+"\n"
    else:
      myR = "PASS\n"

    print "myR", myR
    print "totalNanos", self.totalNanos, self.playerStates
    # myR = str(random.randint(0, len(self.nodeStates.keys()))) + ",UP,DOWN,LEFT,RIGHT" + "\n"
    self.transport.write(myR)


  def connectionMade(self):
    self.transport.write('REGISTER: {0}\n'.format(self.name))

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
  parser.add_argument("-p", "--port", type=int, default="1377", help="Server port to connect to.")
  args = parser.parse_args()
  client_name = args.name
  port = args.port
  factory = ClientFactory(client_name)
  reactor.connectTCP("localhost", port, factory)
  reactor.run()

if __name__ == '__main__':
    main()