from websocket import create_connection
import json

mainSocket = create_connection('ws://localhost:1990');
socketH = create_connection('ws://localhost:1991');

class Hunter(object):
  def __init__(self, cooldown, maxWalls):
    self.prey = [230, 200]
    self.hunter = [0, 0]
    self.direction = [1, 1]
    self.time = 0
    self.cooldown = cooldown
    self.maxWalls = maxWalls
    self.lastTimeBuiltWall = -1
    self.straight = 0
    self.grid = {
      'left': {
        'position': [-1, -1],
        'length': 301,
        'direction': 'N'
      },
      'right': {
        'position': [301, -1],
        'length': 301,
        'direction': 'N'
      },
      'top': {
        'position': [-1, -1],
        'length': 301,
        'direction': 'E'
      },
      'down': {
        'position': [-1, 301],
        'length': 301,
        'direction': 'E'
      }
    }
    self.walls = []

  def long_dist(self):
    return max(abs(self.prey[0] - self.hunter[0]), abs(self.prey[1] - self.hunter[1]))

  def short_dist(self):
    return min(abs(self.prey[0] - self.hunter[0]), abs(self.prey[1] - self.hunter[1]))

  def short_side(self):
    # Return direction of wall that should be built
    ver_area = self.prey_area(self.walls[:] + [self.new_vertical_wall()])
    hor_area = self.prey_area(self.walls[:] + [self.new_horizontal_wall()])
    return 'V' if ver_area < hor_area else 'H'

  def have_cooldown(self):
    return self.time - self.lastTimeBuiltWall < self.cooldown

  def prey_in_front(self):
    vector_h2p = self.prey[0] - self.hunter[0], self.prey[1] - self.hunter[1]
    return (vector_h2p[0] * self.direction[0] > 0) and (vector_h2p[1] * self.direction[1] > 0)

  def prey_area(self, walls):
    left, right, top, down = [], [], [], []
    for w in walls:
      if w['direction'] == 'E' or w['direction'] == 'W':
        dist = w['position'][1] - self.prey[1]
        met = False
        if w['direction'] == 'E':
          met = w['position'][0] <= self.prey[0] <= w['position'][0] + w['length']
        else:
          met = w['position'][0] - w['length'] <= self.prey[0] <= w['position'][0]

        if dist > 0:
          if met:
            down.append((dist, w))
        else:
          if met:
            top.append((dist, w))
      else:
        dist = w['position'][0] - self.prey[0]
        met = False
        if w['direction'] == 'S':
          met = w['position'][1] - w['length'] <= self.prey[1] <= w['position'][1]
        else:
          met = w['position'][1] <= self.prey[1] <= w['position'][1] + w['length']

        if dist:
          if met:
            left.append((dist, w))
        else:
          if met:
            right.append((dist, w))

    if len(left):
      left = sorted(left, key=lambda x: x[0])[-1][1]
    else:
      left = self.grid['left']
    if len(right):
      right = sorted(right, key=lambda x: x[0])[0][1]
    else:
      right = self.grid['right']
    if len(top):
      top = sorted(top, key=lambda x: x[0])[0][1]
    else:
      top = self.grid['top']
    if len(down):
      down = sorted(down, key=lambda x: x[0])[-1][1]
    else:
      down = self.grid['down']

    return abs(top['position'][1] - down['position'][1]) * abs(right['position'][0] - left['position'][0])

  def wall_between(self):
    ret = False
    for w in self.walls:
      if w['direction'] == 'E' or w['direction'] == 'W':
        ret = ret or ((self.prey[1] < w['position'][1] < self.hunter[1]) or (self.hunter[1] < w['position'][1] < self.prey[1]))
      else:
        ret = ret or ((self.prey[0] < w['position'][0] < self.hunter[0]) or (self.hunter[0] < w['position'][0] < self.prey[0]))

    return ret

  def new_vertical_wall(self):
    top, down = [], []

    for w in self.walls:
      if w['direction'] == 'E' or w['direction'] == 'W':
        dist = w['position'][1] - self.hunter[1]
        met = False
        if w['direction'] == 'E':
          met = w['position'][0] <= self.hunter[0] <= w['position'][0] + w['length']
        else:
          met = w['position'][0] - w['length'] <= self.hunter[0] <= w['position'][0]

        if dist > 0:
          if met:
            down.append((dist, w))
        else:
          if met:
            top.append((dist, w))

    if len(top):
      top = sorted(top, key=lambda x: x[0])[0][1]
    else:
      top = self.grid['top']
    if len(down):
      down = sorted(down, key=lambda x: x[0])[-1][1]
    else:
      down = self.grid['down']

    return {
      'length': abs(top['position'][1] - down['position'][1]),
      'position': [self.hunter[0], top['position'][1] + 1],
      'direction': 'N'
    }

  def new_horizontal_wall(self):
    left, right = [], []

    for w in self.walls:
      if w['direction'] == 'N' or w['direction'] == 'S':
        dist = w['position'][0] - self.hunter[0]
        met = False
        if w['direction'] == 'S':
          met = w['position'][1] - w['length'] <= self.hunter[1] <= w['position'][1]
        else:
          met = w['position'][1] <= self.hunter[1] <= w['position'][1] + w['length']

        if dist > 0:
          if met:
            right.append((dist, w))
        else:
          if met:
            left.append((dist, w))

    if len(left):
      left = sorted(left, key=lambda x: x[0])[-1][1]
    else:
      left = self.grid['left']
    if len(right):
      right = sorted(right, key=lambda x: x[0])[0][1]
    else:
      right = self.grid['right']

    return {
      'length': abs(right['position'][0] - left['position'][0]),
      'position': [left['position'][0] + 1, self.hunter[1]],
      'direction': 'E'
    }
      

  def remove_and_build_wall(self):
    wall = None
    for i in xrange(len(self.walls)):
      w = self.walls[i]
      if w['direction'] == 'E' or w['direction'] == 'W':
        if self.prey[1] < w['position'][1] < self.hunter[1] or self.hunter[1] < w['position'][1] < self.prey[1]:
          wall = i
          break
      else:
        if self.prey[0] < w['position'][0] < self.hunter[0] or self.hunter[0] < w['position'][0] < self.prey[0]:
          wall = i
          break

    # Check distance
    none = {'command': 'M'}
    if self.walls[wall]['direction'] == 'E' or self.walls[wall]['direction'] == 'W':
      if abs(self.walls[wall]['position'][1] - self.hunter[1]) > 2:
        return none
    else:
      if abs(self.walls[wall]['position'][0] - self.hunter[0]) > 2:
        return none

    cmd = {
      'command': 'BD',
      'wallIds': [self.walls[wall]['id']]
    }
    del self.walls[wall]
    
    ver_area = self.prey_area(self.walls[:] + [self.new_vertical_wall()])
    hor_area = self.prey_area(self.walls[:] + [self.new_horizontal_wall()])
    cmd['wall'] = {'direction': ('V' if ver_area < hor_area else 'H')}

    return cmd

  def good_time_for_wall(self, in_front):
    if self.have_cooldown():
      return False

    # Return a wall if it can corner prey into a smaller area
    curr_area = self.prey_area(self.walls)
    ver_area = self.prey_area(self.walls[:] + [self.new_vertical_wall()])
    hor_area = self.prey_area(self.walls[:] + [self.new_horizontal_wall()])

    return min(curr_area, ver_area, hor_area) < curr_area
      

  def remove_walls(self, cmd):
    cmd['command'] = 'BD'
    cmd['wallIds'] = []

    curr_area = self.prey_area(self.walls)
    for i in xrange(len(self.walls)):
      area = self.prey_area(self.walls[:i] + self.walls[i+1:])
      if area == curr_area:
        cmd['wallIds'].append(self.walls[i]['id'])

    return cmd

  def move_in_front(self):
    cmd = {'command': 'M'}

    if self.wall_between():
      cmd = self.remove_and_build_wall()
    else:
      if self.good_time_for_wall(True):
        cmd['command'] = 'B'
        cmd['wall'] = {'direction': self.short_side()}

    if len(self.walls) >= self.maxWalls:
      cmd = self.remove_walls(cmd)
      cmd['wall'] = {'direction': self.short_side()}

    return cmd

  def move_in_back(self):
    cmd = {'command': 'M'}
    if self.good_time_for_wall(False):
      cmd['command'] = 'B'
      cmd['wall'] = {'direction': self.short_side()}

    if len(self.walls) >= self.maxWalls:
      cmd = self.remove_walls(cmd)
      cmd['wall'] = {'direction': self.short_side()}

    return cmd

  def make_move(self, cmd):
    self.walls = cmd['walls']
    self.direction = [cmd['hunter'][0] - self.hunter[0], cmd['hunter'][1] - self.hunter[1]]
    if 0 in self.direction:
      self.straight += 1
    else:
      self.straight = 0
    self.hunter = cmd['hunter']
    self.prey = cmd['prey']
    self.time = cmd['time']

    if self.straight >= 10:
      cmd = {
        'command': 'D',
        'wallIds': [w['id'] for w in self.walls]
      }
      return cmd
    elif self.prey_in_front():
      return self.move_in_front()
    else:
      return self.move_in_back()


def main():
  hunter = Hunter(3, 5)
  socketH.send(json.dumps({'command': 'M'}))

  gameover = False
  while gameover is False:
    cmd = json.loads(mainSocket.recv())
    gameover = cmd['gameover']
    if gameover is False:
      newMove = hunter.make_move(cmd)
      socketH.send(json.dumps(newMove))
    else:
      print 'DONE: ' + str(cmd['time'])


if __name__ == '__main__':
  main()
