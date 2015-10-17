#!/usr/bin/env python

#  validator.py (Python2.3 or higher required) [oct. 14 2004]

#  by Yusuke Shinyama (yusuke at cs dot nyu dot edu)

import sys, os, re, fileinput


def timetake(a,b):
 return abs(a.x-b.x)+abs(a.y-b.y)


# Exception class
class ValidationError(ValueError): pass
class FormatSyntaxError(ValidationError): pass
class DataMismatchError(ValidationError): pass
class IllegalPlanError(ValidationError): pass


##  Person object
##
PID = 0
class Person:

  def __init__(self, x, y, st):
    global PID
    PID += 1
    self.pid = PID
    self.x = x
    self.y = y
    self.st = st
    self.rescued = False
    return
  
  def __repr__(self):
    return '%d: (%d,%d,%d)' % (self.pid, self.x, self.y, self.st)


##  Hostpital object
##
HID = 0
class Hospital:
  
  def __init__(self, x, y, namb):
    global HID
    HID += 1
    self.hid = HID
    self.x = x
    self.y = y
    # ambtime array represents the time each ambulance have already spent.
    # NOTE: this should be sorted in a decreasing order (larger value first).
    self.ambtime = [0] * namb
    return
    
  def __repr__(self):
    return '%d: (%d,%d)' % (self.hid, self.x, self.y)
  
  def decamb(self, t):
    self.ambtime[t] -= 1
    if self.ambtime[t] == 0: del self.ambtime[t]
    return
  
  def incamb(self, t):
    if t not in self.ambtime: self.ambtime[t] = 0
    self.ambtime[t] += 1
    return
  
  def rescue(self, pers):
    if 2 < len(pers):
      raise IllegalPlanError('Cannot rescue more than two people at once: %s' % pers)
    already_rescued = filter(lambda p: p.rescued, pers)
    if already_rescued:
      raise IllegalPlanError('Person already rescued: %s' % already_rescued)
    # t: time to take
    if len(pers) == 1:
      t = timetake(self, pers[0])+1+timetake(pers[0], self)+1
    else:
      t = timetake(self, pers[0])+1+timetake(pers[0], pers[1])+1+timetake(pers[1], self)+1
    # try to schedule from the busiest ambulance at the hospital.
    for (i,t0) in enumerate(self.ambtime):
      if not filter(lambda p: p.st < t0+t, pers): break
    else:
      raise IllegalPlanError('Either person cannot make it: %s' % pers)
    # proceed the time.
    self.ambtime[i] += t
    # keep it sorted.
    self.ambtime.sort()
    self.ambtime.reverse()
    for p in pers:
      p.rescued = True
    print 'Rescued:', ' and '.join(map(str, pers)), 'taking', t
    return


# readdata
def readdata(fname):
  print >>sys.stderr, 'Reading data:', fname
  persons = []
  hospitals = []
  mode = 0
  for line in file(fname):
    line = line.strip().lower()
    if line.startswith("person") or line.startswith("people"):
      mode = 1
    elif line.startswith("hospital"):
      mode = 2
    elif line:
      (a,b,c) = map(int, line.split(","))
      if mode == 1:
        persons.append(Person(a,b,c))
      elif mode == 2:
        hospitals.append(Hospital(a,b,c))
  return (persons, hospitals)


# read_results
def readresults(persons, hospitals):
  print >>sys.stderr, 'Reading results...'
  p1 = re.compile(r'(\d+\s*:\s*\(\s*\d+\s*,\s*\d+(\s*,\s*\d+)?\s*\))')
  p2 = re.compile(r'(\d+)\s*:\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)')
  p3 = re.compile(r'(\d+)\s*:\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)')

  score = 0
  for line in fileinput.input():
    line = line.strip().lower()
    if not line: continue
    if not line.startswith('ambulance'):
      print >>sys.stderr, '!!! Ignored: %r' % line
      continue
    try:
      hos = None
      rescue_persons = []
      for (i,(w,z)) in enumerate(p1.findall(line)):
        m = p2.match(w)
        if m:
          # Hospital n:(x,y)
          if i != 0:
            raise FormatSyntaxError('Specify a person now: %r' % line)
          (a,b,c) = map(int, m.groups())
          if a <= 0 or len(hospitals) < a:
            raise FormatSyntaxError('Illegal hospital id: %d' % a)
          hos = hospitals[a-1]
          if hos.x != b or hos.y != c:
            raise DataMismatchError('Hospital mismatch: %s != %d:%s' % (hos, a,(b,c)))
          continue
        m = p3.match(w)
        if m:
          # Person n:(x,y,t)
          if i == 0:
            raise FormatSyntaxError('Specify a hospital first: %r' % line)
          (a,b,c,d) = map(int, m.groups())
          if a <= 0 or len(persons) < a:
            raise FormatSyntaxError('Illegal person id: %d' % a)
          per = persons[a-1]
          if per.x != b or per.y != c or per.st != d:
            raise DataMismatchError('Person mismatch: %s != %d:%s' % (per, a,(b,c,d)))
          rescue_persons.append(per)
          continue
        # error
        raise FormatSyntaxError('Expected "n:(x,y)" or "n:(x,y,t)": %r' % line)

      if not hos or not rescue_persons:
        print >>sys.stderr, '!!! Insufficient data: %r' % line
        continue
      hos.rescue(rescue_persons)
      score += len(rescue_persons)
    except ValidationError, x:
      print >>sys.stderr, '!!!', x
  #
  print 'Total score:', score
  return


# main
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print 'usage: validator.py datafile [resultfile]'
    sys.exit(2)
  (persons, hospitals) = readdata(sys.argv[1])
  del sys.argv[1]
  readresults(persons, hospitals)
