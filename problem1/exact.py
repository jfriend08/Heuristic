#!/usr/bin/python
import sys

class exactChange(object):
  def __init__(self, N):
    self.N = N # will be assign. Penalty of multiple of 5
    self.maxChange = 239 # max change of english piund
    self.numDoms = 7 # num of denomaitions need to design
    self.bestScore = sys.maxint # store the current best score
    self.bestDenoms =[] # store the best score's corresponding denomaitions
    self.numTry = 10 # number of possible values to hold at each level

  def getExactChange(self, changeAmount, Denoms):
    # for testing exact change
    result = []
    Denoms.sort(reverse=True)
    for eachChange in Denoms:
      numChange = int(changeAmount/eachChange)
      if changeAmount <= 0:
        result.append(0)
      else:
        result.append(numChange)
        changeAmount -= numChange*eachChange
    return result

  def getScoreWithGivenDenominations(self, Denoms):
    # input denomination list, then calculate changeArray, and then return the score
    if not Denoms:
      return

    # get changeArray with given denoms list
    changeArray = [0 for i in range(self.maxChange)]
    for idx in xrange(len(changeArray)):
      changeAmount = idx + 1
      bestExactChange = sys.maxint
      if changeAmount == 1:
        changeArray[idx] = 1
      else:
        for eachDenom in Denoms:
          # always need to add up one coin. dynamic programmingly check previous results and find the best one
          diff = changeAmount - eachDenom
          if diff > 0:
            bestExactChange = min(bestExactChange, changeArray[diff-1] + 1)
          elif diff ==0:
            bestExactChange = 1
        changeArray[idx] = bestExactChange

    # make penalty for each multiple of 5
    for idx in xrange(len(changeArray)):
      if (idx + 1) % 5 == 0:
        changeArray[idx] = changeArray[idx] * self.N

    return sum(changeArray)

  def getTheTopTries(self, denoms, currScore):
    rankList = []
    for testDenom in range(2,int(self.maxChange/2)):
        if testDenom in self.bestDenoms or testDenom in denoms:
          continue
        testDenoms = denoms[:]
        testDenoms.append(testDenom)
        testValue = self.getScoreWithGivenDenominations(testDenoms)
        if testValue < currScore:
          rankList.append((testValue, testDenom)) # tuple of goodValue and denom
    rankList.sort(key=lambda tup: tup[0])
    return rankList[:self.numTry]

  def findOptimalDenoms(self, denoms):
    # minimize the score. recurssively trying all possibilities
    currScore = self.getScoreWithGivenDenominations(denoms)
    if len(denoms) < self.numDoms: # which is 7
      rankList = self.getTheTopTries(denoms, currScore)
      for testValue, testDenom in rankList:
        testDenoms = denoms[:]
        testDenoms.append(testDenom)
        self.findOptimalDenoms(testDenoms)

    else:
      if currScore < self.bestScore:
        print 'self.bestScore: %s' %self.bestScore
        print 'self.bestDenoms: %s' %self.bestDenoms
        self.bestScore = currScore
        self.bestDenoms = denoms

    return self.bestScore, self.bestDenoms



if __name__ == "__main__":
  arg = sys.argv[1]
  solution = exactChange(float(arg))
  print solution.getExactChange(238,[1, 14, 33, 37, 57, 62, 79]) ## for checking
  print solution.getScoreWithGivenDenominations([1, 14, 33, 37, 57, 62, 79])
  print solution.findOptimalDenoms([1])










