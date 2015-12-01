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
    self.gameover = False
    self.timeNow = None
    self.walls = []
    self.publisherMsg = False
    self.willGetCaughtDist = 300
    self.allDirs = {(0,0):"X", (0,-1):"N", (0,1):"S", (1,0):"E", (-1,0):"W", (1,-1):"NE", (-1,-1):"NW", (1,1):"SE", (-1,1):"SW"}
    # self.allDirs = {"0_0":"X", "0_-1":"N", "0_1":"S", "1_0":"E", "-1_0":"W", "1_-1":"NE", "-1_-1":"NW", "1_1":"SE", "-1_1":"SW"}
    self.Dir2Coordinate = {"X":(0,0), "N":(0,-1), "S":(0,1), "E":(1,0), "W":(-1,0), "NE":(1,-1), "NW":(-1,-1), "SE":(1,1), "SW":(-1,1)}
    self.getOppDir = {"X":"X", "S":"N", "N":"S", "W":"E", "E":"W", "NE":"SW", "SW":"NE", "NW":"SE", "SE":"NW"}
    self.wallBoundary = self.setWallBoundary()

  def getGameOverState(self):
    return self.gameover

  def setTime(self, time):
    self.timeNow = time

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
    self.hunterDirection = self.allDirs[(dx,dy)]
    # self.hunterDirection = self.allDirs[str(dx)+"_"+str(dy)]
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

      for i in xrange(length+1):
        newPos = startPos + aWallDirection*i
        aWall.add(tuple(newPos))
      self.walls.append([aWallDirection.tolist(), aWall])
    print "Done wallUpdate. Length:", len(self.walls)

  def recvPublisher(self):
    result = json.loads(mainSocket.recv())
    # print "walls", result["walls"]
    self.updateHDriection(self.hunterPos, result["hunter"])
    self.gameover = result["gameover"]
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

  def hitWallThenChange(self, idealDir):
    idealDir_coor = list(self.Dir2Coordinate[idealDir])
    if self.preyPos[0] == 0 and idealDir_coor[0]<0:
      idealDir_coor[0] = 0
    elif self.preyPos[0] == 300 and idealDir_coor[0]>0:
      idealDir_coor[0] = 0
    elif self.preyPos[1] == 0 and idealDir_coor[1]<0:
      idealDir_coor[1] = 0
    elif self.preyPos[1] == 300 and idealDir_coor[1]>0:
      idealDir_coor[1] = 0
    return self.allDirs[tuple(idealDir_coor)]

  def headingRight(self):
    x, y = self.preyPos
    headingRight = x
    headingLeft = x
    headingUp = y
    headingDown = y
    while headingRight!=300:
      for (wall_dir, wall) in self.walls:
        if (headingRight, y) in wall:
          return sorted(wall), headingRight
      headingRight += 1
    return None, headingRight

  def headingLeft(self):
    x, y = self.preyPos
    headingRight = x
    headingLeft = x
    headingUp = y
    headingDown = y
    while headingLeft!=0:
      for (wall_dir, wall) in self.walls:
        if (headingLeft, y) in wall:
          print "2 yea!!!!!!"
          return sorted(wall), headingLeft
      headingLeft -= 1
    return None, headingLeft

  def headingUp(self):
    x, y = self.preyPos
    headingRight = x
    headingLeft = x
    headingUp = y
    headingDown = y
    while headingUp!=0:
      for (wall_dir, wall) in self.walls:
        if (x, headingUp) in wall:
          print "3 yea!!!!!!"
          return sorted(wall), headingUp
      headingUp -= 1
    return None, headingUp

  def headingDown(self):
    x, y = self.preyPos
    headingRight = x
    headingLeft = x
    headingUp = y
    headingDown = y
    while headingDown!=300:
      for (wall_dir, wall) in self.walls:
        if (x, headingDown) in wall:
          print "4 yea!!!!!!"
          return sorted(wall), headingDown
      headingDown += 1
    return None, headingDown

  def gotSandwich(self):
    print "++++++++++ self.preyPos", self.preyPos, "++++++++++"
    print "++++++++++ self.hunterPos", self.hunterPos, "++++++++++"
    x, y = self.preyPos
    hx, hy = self.hunterPos
    rightwall, headRight = self.headingRight()
    leftwall, headLeft = self.headingLeft()
    downwall, headDown = self.headingDown()
    upwall, headUp = self.headingUp()
    rldiff = headRight - headLeft
    uddiff = headDown - headUp
    print "rightwall", rightwall
    print "leftwall", leftwall
    print headRight, headLeft, headDown, headUp
    print "rldiff", rldiff, "uddiff", uddiff
    if rldiff < 10:
      # rightBount = (rightwall[0][0] if rightwall!=None else 300)
      # leftBount = (leftwall[0][0] if leftwall!=None else 0)
      # upPoint = 
      # downPoint = 
      if hy <= y:
        return "S"
      else:
        return "N"
    elif uddiff < 10:
      upBound = (upwall[0][1] if upwall!=None else 0)
      lowBound = (downwall[0][1] if downwall!=None else 300)
      try:
        leftPoint = max(upwall[0][0], downwall[0][0])
      except:
        leftPoint = 0
      try:
        rightPoint = min(upwall[-1][0], downwall[-1][0])
      except:
        rightPoint = 300
      print "upBound", upBound, "lowBound", lowBound, "leftPoint", leftPoint, "rightPoint", rightPoint
      if hy > upBound or hy < lowBound:
        ''' hunter not in sandwich, find the cloest exit'''
        if leftPoint==0 or rightPoint ==300:
          return ("W" if leftPoint !=0 else "E")
        elif abs(x - leftPoint) < abs(x - rightPoint):
          return "W"
        else:
          return "E"
      elif hx <= x:
        return "E"
      else:
        return "W"
    return None

  def ifWillGetCaughtChangeDir(self, idealDir):
    # TODO: should be more determine to decide new_idealDir semi-opposit to self.hunterDirection, instead just rand
    nextPosition_prey = numpy.array(self.preyPos) + numpy.array(self.Dir2Coordinate[idealDir])
    nextPosition_hunter = numpy.array(self.hunterPos) + 2*numpy.array(self.Dir2Coordinate[self.hunterDirection])
    dist = euclidean(nextPosition_prey, nextPosition_hunter)

    print "Inside ifWillGetCaughtChangeDir. Distance: ", dist

    if self.willGetCaughtDist-dist < 0:
      self.willGetCaughtDist = dist
      return idealDir

    self.willGetCaughtDist = dist
    if dist > 100:
      return idealDir
    else:
      print "TOO close. RUN"
      '''Opps too close ==> run up or down! '''
      hunterDirection_coor = list(self.Dir2Coordinate[self.hunterDirection])
      preyDirection_coor = list(self.Dir2Coordinate[idealDir])
      for i in xrange(-40, 300):
        H_testPos = numpy.array(self.hunterPos) + i*numpy.array(hunterDirection_coor)
        if H_testPos[0] == nextPosition_prey[0] and nextPosition_prey[1] >= H_testPos[1]:
          '''situation will get caught and prey is at-or-below Hunter'''
          if hunterDirection_coor[1] > 0:
            print "consideration1"
            runDir = (preyDirection_coor[0], -1*preyDirection_coor[1])
          else:
            print "consideration2"
            runDir = (-1*preyDirection_coor[0], preyDirection_coor[1])
          return self.allDirs[runDir]
        elif H_testPos[0] == nextPosition_prey[0] and nextPosition_prey[1] < H_testPos[1]:
          '''situation will get caught and prey is above Hunter'''
          if hunterDirection_coor[1] > 0:
            print "consideration3"
            runDir = (-1*preyDirection_coor[0], preyDirection_coor[1])
          else:
            print "consideration4"
            runDir = (preyDirection_coor[0], -1*preyDirection_coor[1])
          return self.allDirs[runDir]
      return idealDir

    # #Below are rand method, but not determinded enough
    # considerCount = 0
    # while dist <= 6 and considerCount<15:
    #   dirIdx = randint(0,len(self.allDirs.keys())-1);
    #   new_idealDir = self.allDirs[self.allDirs.keys()[dirIdx]]
    #   nextPosition_prey = numpy.array(self.preyPos) + numpy.array(self.Dir2Coordinate[new_idealDir])
    #   dist = euclidean(nextPosition_prey, nextPosition_hunter)
    #   idealDir = new_idealDir
    #   print "may get caught new_idealDir", new_idealDir
    #   print "may get caught idealDir", idealDir
    #   considerCount += 1
    # return idealDir

  def getHitPoint(self, position, direction):
    positionAhead = numpy.array(position)
    headingDirection = numpy.array(direction)
    print "getHitPoint. position", position, direction
    while positionAhead[0]!=0 and positionAhead[0]!=300 and positionAhead[1]!=0 and positionAhead[1]!=300:
      for (wall_dir, wall) in self.walls:
        if tuple(positionAhead) in wall:
          print "******", "hitWall", wall_dir, tuple(positionAhead), "******"
          return (list(positionAhead - headingDirection), wall_dir, list(self.Dir2Coordinate[self.getOppDir[self.allDirs[tuple(wall_dir)]]]), wall)
      positionAhead = positionAhead + headingDirection
    return (None, None, None, None)

  def hitEarly(self, idealDir):
    idealDir_coor = list(self.Dir2Coordinate[idealDir])
    (hitPosition, wallDir, wallOppDir, wallSet) = self.getHitPoint(self.preyPos, self.Dir2Coordinate[idealDir])

    if hitPosition == None:
      return idealDir

    dist = (euclidean(hitPosition, self.preyPos) if hitPosition != None else 1000)

    if dist > 100:
      return idealDir

    if hitPosition != None:
      # Means we will hit the wall within dist if we keep current idealDir
      print "hitPosition", hitPosition, "wallDir", wallDir, "wallOppDir", wallOppDir
      (hitPosition1, wallDir1, wallOppDir1, wallSet1) = self.getHitPoint(hitPosition, wallDir)
      (hitPosition2, wallDir2, wallOppDir2, wallSet2) = self.getHitPoint(hitPosition, wallOppDir)

      if hitPosition1 != None and hitPosition2 != None:
        '''situation that will hit both wall'''
        connectivity1 = wallSet1 & wallSet
        connectivity2 = wallSet2 & wallSet
        if connectivity1 != None and connectivity2 != None:
          # both walls are closed
          # current method is to go the same direction as the Hunter. So to keep the area larger
          return self.hunterDirection
        elif connectivity1 == None:
          ''' the idea for this is to change the ideaDirection to the wall1's hole where's not closed '''
          if (wallDir[0] != 0):
            idealDir_coor[0] = (idealDir_coor[0] if idealDir_coor[0]*wallDir[0]>0 and self.preyAtBack() == 2 else -1*idealDir_coor[0])
            idealDir_coor[1] = (idealDir_coor[1] if hitPosition[0]!=self.preyPos[0] and hitPosition[1]!=self.preyPos[1] else 0)
            # idealDir_coor[1] = 0
          if (wallDir[1] != 0):
            idealDir_coor[0] = (idealDir_coor[0] if hitPosition[0]!=self.preyPos[0] and hitPosition[1]!=self.preyPos[1] else 0)
            # idealDir_coor[0] = 0
            idealDir_coor[1] = (idealDir_coor[1] if idealDir_coor[1]*wallDir[1]>0 else -1*idealDir_coor[1])
          return self.allDirs[tuple(idealDir_coor)]
        elif connectivity2 == None:
          ''' the idea for this is to change the ideaDirection to the wall2's hole where's not closed '''
          if (wallOppDir[0] != 0):
            idealDir_coor[0] = (idealDir_coor[0] if idealDir_coor[0]*wallOppDir[0]>0 and self.preyAtBack() == 2 else -1*idealDir_coor[0])
            idealDir_coor[1] = (idealDir_coor[1] if hitPosition[0]!=self.preyPos[0] and hitPosition[1]!=self.preyPos[1] else 0)
            # idealDir_coor[1] = 0
          if (wallOppDir[1] != 0):
            # idealDir_coor[0] = 0
            idealDir_coor[0] = (idealDir_coor[0] if hitPosition[0]!=self.preyPos[0] and hitPosition[1]!=self.preyPos[1] else 0)
            idealDir_coor[1] = (idealDir_coor[1] if idealDir_coor[1]*wallOppDir[1]>0 and self.preyAtBack() == 2 else -1*idealDir_coor[1])
          return self.allDirs[tuple(idealDir_coor)]
        else:
          return idealDir

      elif hitPosition1 == None:
        ''' Means if we follow wallDir then there we won't get closed '''
        ## TODO: consider connectivity?
        if (wallDir[0] != 0):
          idealDir_coor[0] = (idealDir_coor[0] if idealDir_coor[0]*wallDir[0]>0 and self.preyAtBack() == 2 else -1*idealDir_coor[0])
          idealDir_coor[1] = (idealDir_coor[1] if hitPosition[0]!=self.preyPos[0] and hitPosition[1]!=self.preyPos[1] else 0)
          # idealDir_coor[1] = 0
        if (wallDir[1] != 0):
          # idealDir_coor[0] = 0
          idealDir_coor[0] = (idealDir_coor[0] if hitPosition[0]!=self.preyPos[0] and hitPosition[1]!=self.preyPos[1] else 0)
          idealDir_coor[1] = (idealDir_coor[1] if idealDir_coor[1]*wallDir[1]>0 and self.preyAtBack() == 2 else -1*idealDir_coor[1])
        return self.allDirs[tuple(idealDir_coor)]

      elif hitPosition2 == None:
        ''' Means if we follow oppo-wallDir then there we won't get closed '''
        ## TODO: consider connectivity?
        if (wallOppDir[0] != 0):
          idealDir_coor[0] = (idealDir_coor[0] if idealDir_coor[0]*wallOppDir[0]>0 and self.preyAtBack() == 2 else -1*idealDir_coor[0])
        if (wallOppDir[1] != 0):
          idealDir_coor[1] = (idealDir_coor[1] if idealDir_coor[1]*wallOppDir[1]>0 and self.preyAtBack() == 2 else -1*idealDir_coor[1])
        return self.allDirs[tuple(idealDir_coor)]
  def getPandHDist(self):
    dist = euclidean(self.hunterPos, self.preyPos)

  def decideMove(self):
    atBack = self.preyAtBack()
    idealDir = self.getOppDir[self.hunterDirection]
    sandwichDir = self.gotSandwich()

    if sandwichDir != None:
      idealDir = sandwichDir
      print "got sandwiched. idealDir", idealDir
    elif euclidean(self.hunterPos, self.preyPos) < 100 :
      idealDir = self.ifWillGetCaughtChangeDir(idealDir)
      print "after ifWillGetCaughtChangeDir. idealDir", idealDir
    else:
      print "idealDir", idealDir
      if (idealDir != "X"):
        idealDir = self.hitEarly(idealDir)
        print "after hitEarly. idealDir", idealDir
      idealDir = self.hitWallThenChange(idealDir)
      print "after hitWallThenChange. idealDir", idealDir
      # idealDir = self.ifWillGetCaughtChangeDir(idealDir)
      # print "after ifWillGetCaughtChangeDir. idealDir", idealDir

    print "--preyAtBack", atBack, "--prey idealDir", idealDir
    return idealDir

def main():
  myPrey = Prey()

  stepCount = 1
  while(not myPrey.getGameOverState()):
    myPrey.setTime(stepCount)

    if stepCount == 1:
      myPrey.printBoundary()

    print "------------------", "stepCount", stepCount, "------------------"
    if stepCount%2 == 1:
      myPrey.recvPublisher()

    elif stepCount%2 == 0:
      # #check states
      # myPrey.checkPosition()

      #prey decide moves, and make move
      nextMove = myPrey.decideMove()
      myPrey.addMove(nextMove)

      myPrey.recvPublisher()

    stepCount += 1


if __name__ == '__main__':
  main()