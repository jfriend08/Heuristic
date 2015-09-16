#!/usr/bin/python
import sys

class exactChange(object):
  def __init__(self, N):
    self.N = N
    self.maxChange = 239

  def getExactChange(self, changeAmount, Denoms):
    result = []
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
        changeArray[idx] = bestExactChange

    # make mudification for each multiple of 5
    for idx in xrange(len(changeArray)):
      if (idx + 1) % 5 == 0:
        changeArray[idx] = changeArray[idx] * self.N

    return sum(changeArray)






if __name__ == "__main__":
  arg = sys.argv[1]
  solution = exactChange(float(arg))
  print solution.getExactChange(238,[25,10,5,1]) ## for checking
  print solution.getScoreWithGivenDenominations([1])
