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


def main():
  myPrey = Prey()
  stepCount = 1
  while(stepCount<100):
    myPrey.checkPosition()
    stepCount += 1


if __name__ == '__main__':
  main()