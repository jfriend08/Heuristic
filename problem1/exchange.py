#!/usr/bin/python
import sys


class exChange(object):
  def __init__(self, N):
    self.N = N # will be assign. Penalty of multiple of 5
    self.maxChange = 99 # max change of english piund
    self.numDoms = 5 # num of denomaitions need to design
    self.bestScore = sys.maxint # store the current best score
    self.bestDenoms =[] # store the best score's corresponding denomaitions
    self.numTry = 3 # number of possible values to hold at each level
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
    # input denomination list, then calculate exchangeArray, and then return the score
    if not Denoms:
      return

    changeArray = [0 for i in range(self.maxChange)] # each element is the min exact number of change
    exchangeArray = [0 for i in range(self.maxChange)] # each element is the min of exchange

    # get changeArray with given denoms list
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

    for idx in xrange(len(changeArray)):
      amount = idx + 1
      print "amount: %s" %amount
      minExchange = changeArray[idx]
      for eachDenom in Denoms:
        if eachDenom < amount:
          if amount % eachDenom == 0:
            testAmount = (int(amount/eachDenom) + 1) * eachDenom
          else:
            testAmount = (int(amount/eachDenom)) * eachDenom
          if testAmount < len(changeArray):
            exceedAmount = testAmount
        else:
          exceedAmount = eachDenom
        print "exceedAmount: %s, amount: %s" % (exceedAmount,amount)
        print "changeArray[exceedAmount-1]: %s" % changeArray[exceedAmount-1]
        print "changeArray[exceedAmount-amount-1]: %s" %changeArray[exceedAmount-amount-1]
        minExchange = min(minExchange, changeArray[exceedAmount-1] + changeArray[exceedAmount-amount-1])
        exchangeArray[idx] = minExchange


    print changeArray[42]
    print exchangeArray[42]

if __name__ == "__main__":
  arg = sys.argv[1]
  solution = exChange(float(arg))
  solution.getScoreWithGivenDenominations([1, 5, 10, 25, 50]) ## for checking
  print solution.getExactChange(50,[1, 5, 10, 25, 50])






