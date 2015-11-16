import sys
import random
import time
import argparse

from twisted.internet import reactor, protocol

board_size = 1000

class Client(protocol.Protocol):
  """Random Client"""
  def __init__(self, name):
    self.name = name
    self.prev_moves = []
    self.nodeStates = {}
    self.nodeConCount = []
    self.playerStates = {}

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
            self.playerStates[states[1]] = {'id':states[0], 'remain':states[2], 'used':states[3] , 'inPlay':states[4] , 'score':states[5]}
        else:
          startToSavePlayer = True

    # second pass: get counts
    self.nodeConCount = [0 for i in xrange(len(self.nodeStates.keys()))]
    for key in self.nodeStates.keys():
      self.nodeConCount[int(key)] =  4 - "".join(self.nodeStates[key]['linkage']).count('null')
      print self.nodeConCount[int(key)]



  def dataReceived(self, data):
    self.parseStates(data)
    myR = self.thinkMove
    myR = str(random.randint(0, 158)) + ",UP,DOWN,LEFT,RIGHT" + "\n"
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