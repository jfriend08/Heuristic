#!/usr/bin/python
import sys

class exactChange(object):
  def __init__(self, N):
    self.N = N

  def getExactChange(self, changeAmount):
    diffChanges = [25, 10, 5, 1] #quatar, dime, nickel, pennie
    result = []
    for eachChange in diffChanges:
      numChange = int(changeAmount/eachChange)
      if changeAmount <= 0:
        result.append(0)
      else:
        result.append(numChange)
        changeAmount -= numChange*eachChange
    return result

  def getScoreWithGivenDenominations(self, Denoms):
    maxChange = 239
    if not Denoms:
      return
    changeArray = [0 for i in range(maxChange)]

    for idx in xrange(len(changeArray)):
      changeAmount = idx + 1
      bestExactChange = sys.maxint
      if changeAmount == 1:
        changeArray[idx] = 1
      else:
        for eachDenom in Denoms:
          diff = changeAmount - eachDenom
          if diff > 0:
            bestExactChange = min(bestExactChange, changeArray[diff-1] + 1)
        changeArray[idx] = bestExactChange

    print changeArray





if __name__ == "__main__":
  arg = sys.argv[1]
  solution = exactChange(float(arg))
  solution.getScoreWithGivenDenominations([1])
