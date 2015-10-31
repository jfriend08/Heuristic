import argparse
import random
import sys
import numpy as np
import datetime

import copy
from random import random, choice

from twisted.internet import reactor, protocol

import genVoronoi
from client import Client, ClientFactory

class MonteCarlo(object):
  def __init__(self):
    pass

class Player(Client):
  def __init__(self, name, idx, numMoves):
    Client.__init__(self, name)
    self.numMoves = numMoves
    genVoronoi.init_cache()
    self.points = np.zeros([2, numMoves+1, 2], dtype=np.int)
    self.points.fill(-1)
    self.colors = np.zeros([2, 3], dtype=np.uint8) #Dummy data to run score script
    self.playerIdx = idx
    self.oppIdx = idx ^ 1
    # self.board = np.zeros([1000, 1000], dtype=np.uint8)
    self.board = np.zeros([1000, 1000])
    self.board.fill(-1)
    self.myMoves = 0
    self.oppMoves = 0

    self.max_time = datetime.timedelta(seconds=1)
    self.C = 1.4
    self.wins = {0: {}, 1: {}}
    self.plays = {0: {}, 1: {}}
    self.states = []

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

  def legal_plays(self, board):
    return np.where(board == -1)

  def makeMove(self):

    # move = self.make_random_move()
    print "before thinkNextMove", self.myMoves
    move = self.thinkNextMove(self.board, 1, 2, self.points, self.myMoves, self.oppMoves)
    # if self.myMoves < self.numMoves-1:
    #   move = self.thinkNextMove(self.board, 1, 2, self.points, self.myMoves, self.oppMoves)
    # elif self.myMoves < self.numMoves-1 and self.playerIdx == 0:
    #   move = self.thinkNextMove(self.board, 1, 2, self.points, self.myMoves, self.oppMoves)
    #   # move = self.findBestLastOne(self.board, 1, 2, self.points, self.myMoves, self.oppMoves)
    # else:
    #   move = self.findBestLastOne(self.board, 1, 2, self.points, self.myMoves, self.oppMoves)

    print "makeMove", move
    self.updatePoints(self.playerIdx, self.myMoves, move[0], move[1])
    genVoronoi.generate_voronoi_diagram(2, self.numMoves, self.points, self.colors, None, 0, 0)
    print 'Current score: {0}'.format(self.get_score())

    return move

  def findBestLastOne(self, board, deep, deepSet, points, Moves, OppMoves):
    legalMoves = self.legal_plays(board)
    randIdx = np.random.choice(len(legalMoves[0]), 100)
    tmp = []
    for idx in randIdx:
      tmp.append((legalMoves[0][idx], legalMoves[1][idx]))
    legalMoves = tmp

    score = -sys.maxint - 1
    bestMove = ()
    for eachMove in legalMoves:
      points[self.playerIdx][Moves+1][0] = eachMove[0]
      points[self.playerIdx][Moves+1][1] = eachMove[1]
      genVoronoi.generate_voronoi_diagram(2, Moves+1, points, self.colors, None, 0, 0)
      scores = genVoronoi.get_scores(2)
      myScore = scores[self.playerIdx]
      print "myScore", myScore, eachMove
      if score < myScore:
        score = myScore
        bestMove = eachMove
      points[self.playerIdx][Moves+1][0] = -1
      points[self.playerIdx][Moves+1][1] = -1
    return bestMove

  def thinkNextMove(self, board, deep, deepSet, points, Moves, OppMoves):
    if Moves==0 and OppMoves ==0:
      return (500,500)
    if deep > deepSet:
      genVoronoi.generate_voronoi_diagram(2, Moves, points, self.colors, None, 0, 0)
      scores = genVoronoi.get_scores(2)
      myScore = scores[self.playerIdx]
      oppScore = scores[self.oppIdx]
      return myScore

    legalMoves = self.legal_plays(board)
    if deep%2 == 1:
      randSampling = 10
    else:
      randSampling = 10
    randIdx = np.random.choice(len(legalMoves[0]), randSampling)
    tmp = []
    for idx in randIdx:
      tmp.append((legalMoves[0][idx], legalMoves[1][idx]))
    legalMoves = tmp

    score = -sys.maxint - 1
    bestMove = ()
    for eachMove in legalMoves:
      # print deep, eachMove
      myBoard = np.copy(board)
      myPoints = np.copy(points)
      myMoves = copy.copy(Moves)
      myOppMoves = copy.copy(OppMoves)
      if deep%2 == 1: # it's me
        myPoints[self.playerIdx][myMoves][0] = eachMove[0]
        myPoints[self.playerIdx][myMoves][1] = eachMove[1]
        tmp_val = self.thinkNextMove(board, deep+1, deepSet, myPoints, myMoves+1, myOppMoves)
        board[eachMove[0]][eachMove[1]] = self.playerIdx
      else:
        myPoints[self.oppIdx][myOppMoves][0] = eachMove[0]
        myPoints[self.oppIdx][myOppMoves][1] = eachMove[1]
        tmp_val = self.thinkNextMove(board, deep+1, deepSet, myPoints, myMoves, myOppMoves+1)
        board[eachMove[0]][eachMove[1]] = self.oppIdx

      # tmp_val = self.thinkNextMove(board, deep, deepSet, myPoints, myMoves, myOppMoves)
      if not isinstance(tmp_val, tuple) and tmp_val > score:
        score = tmp_val
        bestMove = eachMove
    print "result in thinkNextMove"
    print score, bestMove, self.myMoves, deep
    if deep == 2:
      return score
    else:
      return bestMove
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
    # self.states.append(player)

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
        self.states.append(self.oppIdx)
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