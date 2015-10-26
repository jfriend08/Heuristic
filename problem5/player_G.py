import argparse
import random
import numpy as np
import datetime
import math

from twisted.internet import reactor, protocol

import genVoronoi
from client import Client, ClientFactory

class MonteCarlo(object):
  def __init__(self, player, **kwargs):
    self.player = player
    self.myMoves = kwargs.get('myMoves', 10)
    self.oppMoves = kwargs.get('oppMoves', 10)
    self.numMoves = kwargs.get('numMoves', 10)
    seconds = 110 / self.numMoves
    self.calculation_time = datetime.timedelta(seconds=seconds)

  def greedy_play(self):
    begin = datetime.datetime.utcnow()
    maxScore, currMove = 0.0, self.player.make_random_move()
    while datetime.datetime.utcnow() - begin < self.calculation_time:
      move = self.player.make_random_move()
      self.player.updatePoints(self.player.playerIdx, self.myMoves, move[0], move[1])
      score = self.player.get_score()[0]
      if score > maxScore:
        maxScore = score
        currMove = move

    return currMove

  def get_play(self):
    begin = datetime.datetime.utcnow()
    maxScore, currMove = 0, self.player.make_random_move()
    while datetime.datetime.utcnow() - begin < self.calculation_time:
      move = self.player.make_random_move()
      self.player.updatePoints(self.player.playerIdx, self.myMoves, move[0], move[1])
      self.myMoves += 1
      score = self.run_simulation(False)
      if self.player.get_score()[0] > 500000 and score > maxScore:
        maxScore = score
        currMove = move
      #Undo
      self.myMoves -= 1
      self.player.undoPoints(self.player.playerIdx, self.myMoves, move[0], move[1])

    return currMove

  def run_simulation(self, myTurn):
    if self.myMoves >= self.numMoves and self.oppMoves >= self.numMoves:
      result = self.player.get_score()[0]
      print 'Score: ' + str(result)
      return result

    if myTurn:
      numMove = self.myMoves
      self.myMoves += 1
      player = self.player.playerIdx
    else:
      numMove = self.oppMoves
      self.oppMoves += 1
      player = self.player.oppIdx

    move = self.player.make_random_move()
    self.player.updatePoints(player, numMove, move[0], move[1])
    score = self.run_simulation(myTurn ^ True)
    if myTurn:
      self.myMoves -= 1
    else:
      self.oppMoves -= 1
    self.player.undoPoints(player, numMove, move[0], move[1])

    return score

class Player(Client):
  def __init__(self, name, idx, numMoves):
    Client.__init__(self, name)
    self.numMoves = numMoves
    genVoronoi.init_cache()
    self.points = np.zeros([2, numMoves, 2], dtype=np.int)
    self.points.fill(-1)
    self.colors = np.zeros([2, 3], dtype=np.uint8) #Dummy data to run score script
    self.playerIdx = idx
    self.oppIdx = idx ^ 1
    self.board = np.zeros([1000, 1000], dtype=np.uint8)
    self.board.fill(-1)
    self.myMoves = 0
    self.oppMoves = 0

    '''
    Return tuple of player scores, first element is our score, second one is opponent's
    '''
  def get_score(self):
    scores = genVoronoi.get_scores(2)
    return scores[self.playerIdx], scores[self.oppIdx]

  '''
  Calculate score of a given move
  '''
  def probe_score(self, moveNum, player, x, y):
    self.points[player][moveNum][0] = x
    self.points[player][moveNum][1] = y
    genVoronoi.generate_voronoi_diagram(2, self.numMoves, self.points, self.colors, None, 0, 0)
    scores = self.get_score()

    #undo
    self.points[player][moveNum][0] = -1
    self.points[player][moveNum][1] = -1
    genVoronoi.generate_voronoi_diagram(2, self.numMoves, self.points, self.colors, None, 0, 0)

    return scores

  def validMove(self, x, y):
    return self.board[x][y] == -1

  def makeMove(self):
    '''
    move = self.make_random_move()
    '''
    simulation = MonteCarlo(self, myMoves = self.myMoves,
                                  oppMoves = self.oppMoves,
                                  numMoves = self.numMoves)

    print '{0} using greedy'.format(self.name)
    move = simulation.greedy_play()

    self.updatePoints(self.playerIdx, self.myMoves, move[0], move[1])
    genVoronoi.generate_voronoi_diagram(2, self.numMoves, self.points, self.colors, None, 0, 0)
    print 'Current score: {0}'.format(self.get_score())

    return move

  def reset(self):
    Client.reset(self)
    self.points.fill(-1)
    self.board.fill(-1)
    self.myMoves = 0
    self.oppMoves = 0

  def updatePoints(self, player, move, x, y):
    self.points[player][move][0] = x
    self.points[player][move][1] = y
    self.board[x][y] = player
    genVoronoi.generate_voronoi_diagram(2, self.numMoves, self.points, self.colors, None, 0, 0)

  def undoPoints(self, player, move, x, y):
    self.points[player][move][0] = -1
    self.points[player][move][1] = -1
    self.board[x][y] = -1
    genVoronoi.generate_voronoi_diagram(2, self.numMoves, self.points, self.colors, None, 0, 0)

  def dataReceived(self, data):
    print 'Player {0} Received: {1}'.format(self.name, data)
    line = data.strip()
    items = line.split('\n')
    if items[-1] == 'TEAM':
      self.transport.write(self.name)
    elif items[-1] == 'MOVE':
      if items[0] == 'RESTART':
        self.reset()
        del items[0]

      for item in items[:-1]:
        parts = item.split()
        x, y = int(parts[1]), int(parts[2])
        self.updatePoints(self.oppIdx, self.oppMoves, x, y)
        self.oppMoves += 1 #TODO: Need to update of want to play multiplayer games

      move = self.makeMove()
      print 'Player {0} making move: {1}'.format(self.name, move)
      self.transport.write('{0} {1}'.format(move[0], move[1]))
      self.myMoves += 1

class PlayerFactory(ClientFactory):
  def __init__(self, name, idx, numMoves):
    ClientFactory.__init__(self, name)
    self.idx = idx
    self.numMoves = numMoves

  def buildProtocol(self, addr):
    c = Player(self.name, self.idx, self.numMoves)
    c.addr = addr
    return c

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('name', help='Team Name')
  parser.add_argument('seq', help='0 for first player, 1 for second player')
  parser.add_argument('-p', '--port', type=int, default=1337, help='Server port')
  parser.add_argument('-m', '--numMoves', type=int, default=10, help='Number of moves available')
  args = parser.parse_args()

  name = args.name
  idx = int(args.seq)
  port = args.port
  numMoves = args.numMoves
  factory = PlayerFactory(name, idx, numMoves)
  reactor.connectTCP('127.0.0.1', port, factory)
  reactor.run()

if __name__ == '__main__':
  main()