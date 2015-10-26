import argparse
import random
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
    self.points = np.zeros([2, numMoves, 2], dtype=np.int)
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
    self.states.append(self.playerIdx)
    legal = self.legal_plays(self.board)
    states = [((legal[0][i], legal[1][i]), tuple(self.states)) for i in xrange(len(legal[0]))]
    print "self.states", self.states
    # print legal
    begin, games = datetime.datetime.utcnow(), 0
    '''Start MonteCarlo method'''
    while datetime.datetime.utcnow() - begin < self.max_time:
      self.random_game()
      games += 1
    print "#random_game", games, datetime.datetime.utcnow() - begin

    move = max(
      (self.wins[self.playerIdx].get(S,0) / self.plays[self.playerIdx].get(S,1), p)
      for p, S in states)[1]
    # move = self.make_random_move()

    self.updatePoints(self.playerIdx, self.myMoves, move[0], move[1])
    genVoronoi.generate_voronoi_diagram(2, self.numMoves, self.points, self.colors, None, 0, 0)
    print 'Current score: {0}'.format(self.get_score())

    return move
  def random_game(self):
    game_moves = {0: set(), 1: set()}
    new_states = []
    new_states.append(self.states[:])
    expand = True
    max_moves = 100

    myBoard = np.copy(self.board)
    myPoints = np.copy(self.points)
    myMoves = copy.copy(self.myMoves)
    myOppMoves = copy.copy(self.oppMoves)

    for t in xrange(self.numMoves-max(myMoves, myOppMoves)):
      state = new_states[-1]
      player = state[-1]
      legal = self.legal_plays(myBoard)
      # print "state", state
      states = [((legal[0][i], legal[1][i]), tuple(state)) for i in xrange(len(legal[0]))]

      plays, wins = self.plays[player], self.wins[player] #they are hash invidually
      # print "plays", plays, type(plays)
      # print "wins", wins, type(wins)
      if all(plays.get(S) for p, S in states): ## state in plays
        log_total = log(sum(plays[S] for p, S in states))
        move, state = max(((wins[S] / plays[S]) + self.C * sqrt(log_total / plays[S]), p, S) for p, S in states)[1:]
      else:
        move, state = choice(states)

      new_states.append(state)
      myBoard[move[0]][move[1]] = player
      if(player==self.playerIdx):
        print "myMoves", myMoves
        myPoints[player][myMoves][0] = move[0]
        myPoints[player][myMoves][1] = move[1]
        myMoves += 1
      else:
        print "myOppMoves", myOppMoves
        myPoints[player][myOppMoves][0] = move[0]
        myPoints[player][myOppMoves][1] = move[1]
        myOppMoves += 1

      if expand and state not in plays: ## expand==TRUE && state not in plays
        expand = False
        plays[state] = 0
        wins[state] = 0

      game_moves[player].add(state)
      winner = self.winner(myMoves, myOppMoves, myPoints)
      if winner:
        break

    for player, M in game_moves.iteritems():
      for S in M:
        if S in self.plays[player]:
          self.plays[player][S] += 1

    if winner in (1, 2):
      for S in game_moves[winner]:
        if S in self.plays[winner]:
          self.wins[winner][S] += 1

  def winner(self, myMoves, myOppMoves, myPoints):
    if myMoves == myOppMoves and myOppMoves == self.numMoves:
      genVoronoi.generate_voronoi_diagram(2, myMoves, myPoints, self.colors, None, 0, 0)
      scores = genVoronoi.get_scores(2)
      myScore = scores[self.playerIdx]
      oppScore = scores[self.oppIdx]
      if myScore >= oppScore:
        return self.playerIdx
      else:
        return self.oppIdx
    else:
      return 0

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