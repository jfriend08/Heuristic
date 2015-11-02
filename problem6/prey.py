from websocket import create_connection
import json

mainSocket = create_connection('ws://localhost:1990');
socketH = create_connection('ws://localhost:1991');
socketP = create_connection('ws://localhost:1992');


class Prey(object):
  def __init__(self):
    self.preyPos = [230, 200];
    self.hunterPos = [0, 0];
    self.hunterDirection = None;
    self.walls = [];
    self.publisherMsg = False;
    self.allDirs = {"0_-1":"N", "0_1":"S", "1_0":"E", "-1_0":"W", "1_-1":"NE", "-1_-1":"NW", "1_1":"SE", "-1_1":"SW"}

  def checkPosition(self):
    data = {"command":"P"}
    socketP.send(json.dumps(data))
    result = json.loads(socketP.recv())
    self.preyPos = result["prey"]
    self.hunterPos = result["hunter"]
    # print "self.preyPos", self.preyPos

  def addMove(self, direction):
    socketP.send(json.dumps({"command":"M", "direction": direction}))

  def updateHDriection(self, HPos0, HPos1):
    if len(HPos0)==0 or len(HPos1)==0:
      return
    dx = (1 if HPos1[0] - HPos0[0] > 0 else HPos1[0] - HPos0[0])
    dx = (-1 if HPos1[0] - HPos0[0] < 0 else dx)
    dy = (1 if HPos1[1] - HPos0[1] > 0 else HPos1[1] - HPos0[1])
    dy = (-1 if HPos1[1] - HPos0[1] < 0 else dy)
    self.hunterDirection = self.allDirs[str(dx)+"_"+str(dy)]


  def recvPublisher(self):
    result = json.loads(mainSocket.recv())
    self.updateHDriection(self.hunterPos, result["hunter"])
    self.preyPos = result["prey"]
    self.hunterPos = result["hunter"]
    self.walls = result["walls"]
    print "preyPos", self.preyPos
    print "hunterPos", self.hunterPos
    # print "recvPublisher", result

  def checkWalls(self):
    return None
  def decideMove(self):
    return None

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
      #check states
      myPrey.checkPosition()
      myPrey.checkWalls()

      #prey decide moves, and make move
      nextMove = myPrey.decideMove()
      myPrey.addMove("NW")

      #hunter will make move
      # socketH.send(json.dumps({"command":"M", "direction": "S"}))

      myPrey.recvPublisher()

    stepCount += 1


if __name__ == '__main__':
  main()