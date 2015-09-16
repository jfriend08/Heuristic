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



if __name__ == "__main__":
  arg = sys.argv[1]
  solution = exactChange(float(arg))
  print solution.getExactChange(25)
  # for i in xrange(240):
  #   print getExactChange(i)