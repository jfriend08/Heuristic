from websocket import create_connection
import json, numpy

mainSocket = create_connection('ws://localhost:1990');
socketH = create_connection('ws://localhost:1991');
socketP = create_connection('ws://localhost:1992');


class Prey(object):
  def __init__(self):
    self.preyPos = [230, 200];
    self.hunterPos = [0, 0];
    self.hunterDirection = None;
    self.wallString = "";
    self.walls = [];
    self.publisherMsg = False;
    self.allDirs = {"0_-1":"N", "0_1":"S", "1_0":"E", "-1_0":"W", "1_-1":"NE", "-1_-1":"NW", "1_1":"SE", "-1_1":"SW"}
    self.Dir2Coordinate = {"N":(0.-1), "S":(0,1), "E":(1,0), "W":(-1,0), "NE":(1,-1), "NW":(-1,-1), "SE":(1,1), "SW":(-1,1)}
    self.getOppDir = {"S":"N", "N":"S", "W":"E", "E":"W", "WS":"NE", "SE":"NW", "NW":"SE", "NE":"SW"}

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
    print self.hunterDirection

  def wallUpdate(self, walls):
    for eachWall in walls:
      aWall = set()
      length = eachWall["length"]
      startPos = numpy.array(eachWall["position"])
      direction = numpy.array(self.Dir2Coordinate[eachWall["direction"]])
      for i in xrange(length):
        newPos = startPos + direction*i
        aWall.add(tuple(newPos))
      self.walls.append(aWall)

  def recvPublisher(self):
    result = json.loads(mainSocket.recv())
    self.updateHDriection(self.hunterPos, result["hunter"])
    self.preyPos = result["prey"]
    self.hunterPos = result["hunter"]
    if not self.wallString == json.dumps(result["walls"]):
      print "wallUpdate ..."
      self.wallString = json.dumps(result["walls"])
      self.wallUpdate(result["walls"])
    self.walls = result["walls"]
    print "preyPos", self.preyPos
    print "hunterPos", self.hunterPos

  def preyAtBack(self):
    #return 0 if can be close by both HorV walls
    #return 1 if can be close by either HorV walls
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

  def checkWalls(self):
    return None

  def decideMove(self):
    print "preyAtBack", self.preyAtBack()
    return self.getOppDir[self.hunterDirection]

def main():
  myPrey = Prey()

  stepCount = 1
  while(stepCount < 1000):
    print "------------------", "stepCount", stepCount, "------------------"
    if stepCount%2 == 1:
      #in this round, prey do nothing
      # socketH.send(json.dumps({"command":"M", "direction": "S"}))
      myPrey.recvPublisher()
    elif stepCount%2 == 0:
      # #check states
      # myPrey.checkPosition()
      # myPrey.checkWalls()

      #prey decide moves, and make move
      nextMove = myPrey.decideMove()
      myPrey.addMove(nextMove)

      #hunter will make move
      # socketH.send(json.dumps({"command":"M", "direction": "S"}))

      myPrey.recvPublisher()

    stepCount += 1


if __name__ == '__main__':
  main()