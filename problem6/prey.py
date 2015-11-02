from websocket import create_connection
import json, numpy
from  scipy.spatial.distance import euclidean
from random import randint

mainSocket = create_connection('ws://localhost:1990')
socketH = create_connection('ws://localhost:1991')
socketP = create_connection('ws://localhost:1992')


class Prey(object):
  def __init__(self):
    self.preyPos = [230, 200]
    self.hunterPos = [0, 0]
    self.hunterDirection = None
    self.wallString = ""
    self.walls = []
    self.publisherMsg = False
    self.allDirs = {"0_0":"X", "0_-1":"N", "0_1":"S", "1_0":"E", "-1_0":"W", "1_-1":"NE", "-1_-1":"NW", "1_1":"SE", "-1_1":"SW"}
    self.Dir2Coordinate = {"X":(0,0), "N":(0,-1), "S":(0,1), "E":(1,0), "W":(-1,0), "NE":(1,-1), "NW":(-1,-1), "SE":(1,1), "SW":(-1,1)}
    self.getOppDir = {"X":"X", "S":"N", "N":"S", "W":"E", "E":"W", "NE":"SW", "SW":"NE", "NW":"SE", "SE":"NW"}
    self.wallBoundary = self.setWallBoundary()

  def setWallBoundary(self):
    EastBound = set()
    SouthBound = set()
    NorthBound = set()
    WestBound = set()

    eastDir = numpy.array([1,0])
    southDir = numpy.array([0,1])
    northDir = numpy.array([0,-1])
    westDir = numpy.array([-1,0])

    startP1 = numpy.array([-1,-1])
    startP2 = numpy.array([301,301])

    for i in range(303):
      new_E_Point = startP1 + eastDir*i
      EastBound.add(tuple(new_E_Point))
      new_S_Point = startP1 + southDir*i
      SouthBound.add(tuple(new_S_Point))
      new_N_Point = startP2 + northDir*i
      NorthBound.add(tuple(new_N_Point))
      new_W_Point = startP2 + westDir*i
      WestBound.add(tuple(new_W_Point))
    return [[eastDir.tolist(),EastBound], [southDir.tolist(),SouthBound], [northDir.tolist(),NorthBound], [westDir.tolist(),WestBound] ]

  def printBoundary(self):
    print self.wallBoundary

  def checkPosition(self):
    data = {"command":"P"}
    socketP.send(json.dumps(data))
    result = json.loads(socketP.recv())
    self.preyPos = result["prey"]
    self.hunterPos = result["hunter"]

  def addMove(self, direction):
    socketP.send(json.dumps({"command":"M", "direction": direction}))

  def getDriection(self, HPos0, PPos1):
    if len(HPos0)==0 or len(PPos1)==0:
      return
    dx = (1 if PPos1[0] - HPos0[0] > 0 else PPos1[0] - HPos0[0])
    dx = (-1 if PPos1[0] - HPos0[0] < 0 else dx)
    dy = (1 if PPos1[1] - HPos0[1] > 0 else PPos1[1] - HPos0[1])
    dy = (-1 if PPos1[1] - HPos0[1] < 0 else dy)
    return (dx,dy)

  def updateHDriection(self, HPos0, HPos1):
    if len(HPos0)==0 or len(HPos1)==0:
      return
    dx = (1 if HPos1[0] - HPos0[0] > 0 else HPos1[0] - HPos0[0])
    dx = (-1 if HPos1[0] - HPos0[0] < 0 else dx)
    dy = (1 if HPos1[1] - HPos0[1] > 0 else HPos1[1] - HPos0[1])
    dy = (-1 if HPos1[1] - HPos0[1] < 0 else dy)
    self.hunterDirection = self.allDirs[str(dx)+"_"+str(dy)]
    print "hunterDirection", self.hunterDirection

  def getWallDirection(self, wallDir):
    #wall direction can be list or letter, convert it to our numpy array format
    if isinstance(wallDir, list):
      direction = numpy.array(wallDir)
    else:
      direction = numpy.array(self.Dir2Coordinate[wallDir])
    return direction

  def wallUpdate(self, walls):
    self.walls = []
    print "Before wallUpdate. Length:", len(self.walls)
    for eachWall in walls:
      aWall = set()
      length = eachWall["length"]
      startPos = numpy.array(eachWall["position"])
      aWallDirection = self.getWallDirection(eachWall["direction"])

      for i in xrange(length):
        newPos = startPos + aWallDirection*i
        aWall.add(tuple(newPos))
      self.walls.append([aWallDirection.tolist(), aWall])
    print "Done wallUpdate. Length:", len(self.walls)
    print self.walls

  def recvPublisher(self):
    result = json.loads(mainSocket.recv())
    self.updateHDriection(self.hunterPos, result["hunter"])
    self.preyPos = result["prey"]
    self.hunterPos = result["hunter"]
    if not self.wallString == json.dumps(result["walls"]):
      print "wallUpdate ..."
      self.wallString = json.dumps(result["walls"])
      self.wallUpdate(result["walls"])
    # self.walls = result["walls"]
    print "preyPos", self.preyPos
    print "hunterPos", self.hunterPos

  def preyAtBack(self):
    #return 0 if can be close by both H or V walls
    #return 1 if can be close by either H or V or Hor walls
    #return 2 if cannot be closed by any walls
    dir_P2H = self.getDriection(self.hunterPos, self.preyPos)
    hunterDirection = self.Dir2Coordinate[self.hunterDirection]
    product1 = hunterDirection[0]*dir_P2H[0]
    product2 = hunterDirection[1]*dir_P2H[1]
    if product1 >0 and product2 >0:
      return 0
    elif product1 <0 and product2 <0:
      return 2
    else:
      return 1

  def getFarAndSeeIfThereIsAWall(self, idealDir):
    # server will handle this case
    pass
    # nextPosition = tuple(numpy.array(self.preyPos) + numpy.array(self.Dir2Coordinate[idealDir]))
    # for (wallDirection, wallPointSet) in self.walls:
    #   if nextPosition in wallPointSet:
    #     print "hit the wall"

  def ifWillGetCaughtChangeDir(self, idealDir):
    # TODO: should be more determine to decide new_idealDir semi-opposit to self.hunterDirection, instead just rand
    nextPosition_prey = numpy.array(self.preyPos) + numpy.array(self.Dir2Coordinate[idealDir])
    nextPosition_hunter = numpy.array(self.preyPos) + numpy.array(self.Dir2Coordinate[self.hunterDirection])
    dist = euclidean(nextPosition_prey, nextPosition_hunter)

    considerCount = 0
    while dist <= 6 and considerCount<15:
      dirIdx = randint(0,len(self.allDirs.keys()));
      new_idealDir = self.allDirs[self.allDirs.keys()[dirIdx]]
      nextPosition_prey = numpy.array(self.preyPos) + numpy.array(self.Dir2Coordinate[new_idealDir])
      dist = euclidean(nextPosition_prey, nextPosition_hunter)
      idealDir = new_idealDir
      print "may get caught new_idealDir", new_idealDir
      print "may get caught idealDir", idealDir
      considerCount += 1

    return idealDir

  def decideMove(self):
    atBack = self.preyAtBack()
    idealDir = self.getOppDir[self.hunterDirection]
    idealDir = self.ifWillGetCaughtChangeDir(idealDir)
    print "--preyAtBack", atBack, "--prey idealDir", idealDir
    return idealDir

def main():
  myPrey = Prey()

  stepCount = 1
  while(stepCount < 1000):
    if stepCount == 1:
      myPrey.printBoundary()

    print "------------------", "stepCount", stepCount, "------------------"
    if stepCount%2 == 1:
      #in this round, prey do nothing
      # socketH.send(json.dumps({"command":"M", "direction": "S"}))
      myPrey.recvPublisher()
    elif stepCount%2 == 0:
      # #check states
      # myPrey.checkPosition()

      #prey decide moves, and make move
      nextMove = myPrey.decideMove()
      myPrey.addMove(nextMove)

      #hunter will make move
      # socketH.send(json.dumps({"command":"M", "direction": "S"}))

      myPrey.recvPublisher()

    stepCount += 1


if __name__ == '__main__':
  main()