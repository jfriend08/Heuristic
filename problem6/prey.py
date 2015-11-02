from websocket import create_connection
import json

mainSocket = create_connection('ws://localhost:1990');
socketH = create_connection('ws://localhost:1991');
socketP = create_connection('ws://localhost:1992');


class Prey(object):
  def __init__(self):
    preyPos = [230, 200];
    hunterPos = [0, 0];
    hunterDirection = [0, 0];
    walls = [];
    publisherMsg = False;

  def checkPosition(self):
    data = {"command":"P"}
    socketP.send(json.dumps(data))
    result = json.loads(socketP.recv())
    self.preyPos = result["prey"]
    self.hunterPos = result["hunter"]
    print "self.preyPos", self.preyPos

  def addMove(self, direction):
    socketP.send(json.dumps({"command":"M", "direction": direction}))

  def recvPublisher(self):
    result = json.loads(mainSocket.recv())
    print "recvPublisher", result

  def checkWalls(self):
    return None
  def decideMove(self):
    return None

def main():
  myPrey = Prey()

  stepCount = 1
  while(stepCount < 10):
    print "stepCount", stepCount
    if stepCount%2 == 1:
      #in this round, prey do nothing
      socketH.send(json.dumps({"command":"M", "direction": "S"}))
      myPrey.recvPublisher()
    elif stepCount%2 == 0:
      #check states
      myPrey.checkPosition()
      myPrey.checkWalls()

      #prey decide moves, and make move
      nextMove = myPrey.decideMove()
      myPrey.addMove("NE")

      #hunter will make move
      socketH.send(json.dumps({"command":"M", "direction": "S"}))

      myPrey.recvPublisher()

    stepCount += 1


if __name__ == '__main__':
  main()