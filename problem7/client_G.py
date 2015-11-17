import sys
import random
import time
import argparse

from twisted.internet import reactor, protocol

board_size = 1000

direction = {
  'LEFT': (-1, 0),
  'RIGHT': (1, 0),
  'TOP': (0, 1),
  'DOWN': (0, -1)
}

class Node(object):
  def __init__(self, id, x, y):
    self.label = id
    self.pos = (x, y)
    self.neighbors = {}
    self.status = 'FREE'

  def addNeighbor(self, direction, neigh):
    self.neighbors[direction] = neigh

  def hasNeighbor(self, direction):
    return self.neighbors.get(direction) is not None

  def getNeighbor(self, direction):
    return self.neighbors.get(direction)

  def setStatus(self, status):
    self.status = status

  def getStatus(self):
    return self.status

class Grid(object):
  def __init__(self):
    self.nodes = {}
    self.grid = {}
    self.candidates = []
    self.alone = []

  def addNode(self, pos, node):
    self.nodes[node.label] = node
    self.grid[pos] = node

  def addEdge(self, nodeId1, nodeId2):
    node1, node2 = self.nodes[nodeId1], self.nodes[nodeId2]
    pos1, pos2 = node1.pos, node2.pos
    node1.addNeighbor((pos2[0] - pos1[0], pos2[1] - pos1[1]), node2)
    node2.addNeighbor((pos1[0] - pos2[0], pos1[1] - pos2[1]), node1)

  def fetchCandidates(self):
    for n in self.nodes:
      if len(self.nodes[n].neighbors) == 0:
        self.alone.append(n)
      elif len(self.nodes[n].neighbors) == 1:
        self.candidates.append(n)
  
  def updateCandidates(self):
    newCandidates = []
    newAlone = []
    for n in self.nodes:
      if self.nodes[n].getStatus() != 'FREE':
        continue
      count = 0
      for neigh in self.nodes[n].neighbors:
        if self.nodes[n].neighbors[neigh].status == 'FREE':
          count += 1

      if count == 1:
        newCandidates.append(n)
      if count == 0:
        newAlone.append(n)
    self.candidates[:] = newCandidates
    self.alone[:] = newAlone

  def getNode(self, id):
    return self.nodes[id]

class Client(protocol.Protocol):
  def __init__(self, name, grid):
    self.name = name
    self.prev_moves = []
    self.grid = grid
    self.myMunchers = {
      'UNUSED': 10,
      'ALIVE': 0,
      'DEAD': 0
    }
    self.oppMunchers = {
      'UNUSED': 10,
      'ALIVE': 0,
      'DEAD': 0
    }
    self.myScore = 0
    self.oppScore = 0

  def updateNode(self, data):
    id = int(data[0])
    status = data[3]
    if status.find('EATEN') != -1:
      status = 'EATEN'
    elif status.find('OCCUPIED') != -1:
      status = 'OCCUPIED'
    self.grid.getNode(id).setStatus(status)

  def updatePlayerState(self, data):
    name = data[1].strip()
    unused, alive, dead, score = int(data[2]), int(data[4]), int(data[3]), int(data[5])
    if name == self.name:
      self.myMunchers['UNUSED'] = unused
      self.myMunchers['ALIVE'] = alive
      self.myMunchers['DEAD'] = dead
      self.myScore = score
    else:
      self.oppMunchers['UNUSED'] = unused
      self.oppMunchers['ALIVE'] = alive
      self.oppMunchers['DEAD'] = dead
      self.oppScore = score

  def makeMove(self):
    return random.choice(self.grid.candidates)

  def dataReceived(self, data):
    print 'Received: ' + data
    lines = data.strip().split('\n')
    currScore = self.myScore
    for l in lines:
      if l in ('START', '', 'END'):
        continue

      if l.find('nodeid') != -1 or l.find('PlayerID') != -1:
        continue

      state = l.split(',')
      if len(state) == 8:
        self.updateNode(state)
      elif len(state) == 6:
        self.updatePlayerState(state)
    self.grid.updateCandidates()

    if self.myMunchers['UNUSED'] > 0:
      move = '{0},LEFT,RIGHT,UP,DOWN\n'.format(self.makeMove())
      print 'Move: ' + move
      self.transport.write(move)
    else:
      print 'PASS'
      self.transport.write('PASS')

  def connectionMade(self):
    self.grid.fetchCandidates()
    self.transport.write('REGISTER: {0}\n'.format(self.name))

  def connectionLost(self, reason):
      reactor.stop()

def readGrid(grid):
  f = open('./data.in', 'r')
  while True:
    line = f.readline()
    if not line:
      break

    data = line.split(',')
    if len(data) == 2:
      # Add Edge
      try:
        grid.addEdge(int(data[0]), int(data[1]))
      except:
        pass
    elif len(data) == 3:
      # Add Node
      try:
        newNode = Node(int(data[0]), int(data[1]), int(data[2]))
        grid.addNode((int(data[1]), int(data[2])), newNode)
      except:
        pass
  f.close()

class ClientFactory(protocol.ClientFactory):
  """ClientFactory"""
  def __init__(self, name):
    self.name = name

  def buildProtocol(self, addr):
    grid = Grid()
    readGrid(grid)
    c = Client(self.name, grid)
    c.addr = addr
    return c

  def clientConnectionFailed(self, connector, reason):
    print "Connection failed - goodbye!"
    reactor.stop()

  def clientConnectionLost(self, connector, reason):
    print "Connection lost - goodbye!"

def main():
    random.seed()
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
