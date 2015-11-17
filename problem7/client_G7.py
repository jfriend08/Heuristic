import sys
import random
import time
import argparse
import itertools
import math

from twisted.internet import reactor, protocol

class Node(object):
  def __init__(self, id, x, y):
    self.label = id
    self.pos = (x, y)
    self.neighbors = {}
    self.status = 'FREE'

  def addNeighbor(self, direction, neigh):
    if neigh == 'null':
      return
    self.neighbors[direction] = int(neigh)

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
    self.others = []

  def addNode(self, pos, node):
    self.nodes[node.label] = node
    self.grid[pos] = node

  def fetchCandidates(self):
    for n in self.nodes:
      if len(self.nodes[n].neighbors) == 0:
        self.alone.append(n)
      elif len(self.nodes[n].neighbors) == 1:
        self.candidates.append(n)
      else:
        self.others.append(n)
  
  def updateCandidates(self):
    newCandidates = []
    newAlone = []
    newOthers = []
    for n in self.nodes:
      if self.nodes[n].getStatus() != 'FREE':
        continue
      count = 0
      for neigh in self.nodes[n].neighbors.values():
        if self.nodes[neigh].status == 'FREE':
          count += 1

      if count == 1:
        newCandidates.append(n)
      if count == 0:
        newAlone.append(n)
      else:
        newOthers.append(n)

    self.candidates[:] = newCandidates
    self.alone[:] = newAlone
    self.others[:] = newOthers

  def getNode(self, id):
    return self.nodes.get(id)

class Muncher(object):
  def __init__(self, pos, loop):
    self.pos = pos
    self.loop = loop
    self.counter = 0

  def nextMove(self, node, visited, grid):
    for i in xrange(4):
      ptr = (self.counter + i) % 4
      direction = self.loop[ptr]
      neigh = node.getNeighbor(direction)
      if neigh is not None and not neigh in visited and grid.getNode(neigh).status == 'FREE':
        self.counter = (ptr + 1) % 4
        self.pos = neigh
        return neigh

    return None


class Client(protocol.Protocol):
  def __init__(self, name):
    self.name = name
    self.prev_moves = []
    self.grid = Grid()
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
    self.lastTimeMove = 0
    self.currTime = 0

  def updateNode(self, data):
    id = int(data[0])
    x, y = int(data[1]), int(data[2])
    status = data[3]
    node = self.grid.getNode(id) or Node(id, x, y)
    node.addNeighbor('UP', data[4])
    node.addNeighbor('DOWN', data[5])
    node.addNeighbor('LEFT', data[6])
    node.addNeighbor('RIGHT', data[7])
    self.grid.addNode((x, y), node)

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

  def randomMove(self):
    if random.randint(1, 10) < 3 and self.myMunchers['UNUSED'] > 0:
      seq = ['UP', 'DOWN', 'LEFT', 'RIGHT']
      random.shuffle(seq)
      return ','.join([str(random.choice(self.grid.candidates))] + seq) + '\n'
    else:
      return 'PASS\n'

  def countScore(self, node):
    maxCount = 0
    maxDir = None
    node = self.grid.getNode(node)
    for directions in itertools.permutations(['UP', 'DOWN', 'LEFT', 'RIGHT']):
      muncher = Muncher(node.label, directions)
      count = 0
      visited = set([])
      nextNode = muncher.nextMove(node, visited, self.grid)
      while nextNode is not None:
        count += 1
        visited.add(nextNode)
        nextNode = self.grid.getNode(nextNode)
        nextNode = muncher.nextMove(nextNode, visited, self.grid)
      if count > maxCount:
        maxCount = count
        maxDir = directions

    return maxCount, node.label, maxDir

  def nodesWillVisit(self, muncher, start):
    visited = set([start])
    nextNode = muncher.nextMove(self.grid.getNode(start), visited, self.grid)
    while nextNode is not None:
      visited.add(nextNode)
      nextNode = muncher.nextMove(self.grid.getNode(nextNode), visited, self.grid)

    return visited

  def makeMove(self):
    if self.myMunchers['UNUSED'] == 0 or (self.currTime > 0 and self.currTime < self.lastTimeMove + 2):
      print self.myMunchers
      return 'PASS\n'

    tar = []
    if len(self.grid.candidates) > 0:
      tar[:] = self.grid.candidates
    elif len(self.grid.others) > 0:
      tar[:] = self.grid.others
    elif len(self.grid.alone) > 0:
      tar[:] = self.grid.alone
    else:
      print 'No available moves...'
      return 'PASS\n'

    scores = sorted(map(self.countScore, tar), key=lambda x: x[0], reverse=True)
    moves = []
    nodes = set([])
    for i in xrange(self.myMunchers['UNUSED'] if self.myMunchers['UNUSED'] < len(scores) else len(scores)):
      visits = self.nodesWillVisit(Muncher(scores[i][1], scores[i][2]), scores[i][1])
      if len(nodes | visits) > (1.1 * len(nodes)):
        nodes = nodes | visits
        moves.append(','.join([str(scores[i][1])] + list(scores[i][2])))
      else:
        break

    if len(moves) > 1 and len(moves) > self.myMunchers['UNUSED'] / 3:
      m = int(math.ceil(self.myMunchers['UNUSED'] / 3.0))
      if m > len(moves):
        m = len(moves)
      moves = moves[:m]

    self.lastTimeMove = self.currTime
    return '|'.join(moves) + '\n'

  def dataReceived(self, data):
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

    next = self.makeMove()
    self.currTime += 1
    print 'next: ' + next
    self.transport.write(next)

  def connectionMade(self):
    self.grid.fetchCandidates()
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
