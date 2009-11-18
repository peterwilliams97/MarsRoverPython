#!/bin/python

'''
Created on 14/11/2009

@author: peter

This program moves a squad of robotic rovers around a rectangular plateau.
  The plateau is divided up into a grid of unit squares to simplify navigation.
  
  A rover's position and direction are represented by x and y coordinates 
  and a letter representing one of the four cardinal compass points. 
  e.g. "0 0 N"  means the rover is in the bottom left corner facing North.
  
  The square directly North of (x, y) is (x, y+1).
  
  A rover's movement are controlled by a sequence of letters. The possible letters 
  are 'L', 'R' and 'M'. 'L' and 'R' makes the rover spin 90 degrees left or right 
  respectively without moving from its current spot. 'M' means move forward 
  one grid point and maintain the same heading. 
  
  Input is read from stdin and output is written to stdout.
  
  INPUT
  		The first line is the x,y coordinates of top-right of the plateau boundary. 
  			e.g. "5 5" . (The lower left is at 0,0)
  		The 2Nth line is the initial position/direction of the Nth rover. e.g "1 2 N"
  		The 2N+1th line is the movement commands for the Nth rover. e.g "LMLMLMLMM"
  OUTPUT
  		The Nth line is the final position and direction of the Nth rover. e.g. "1 3 N"	
  
  Each rover will be run sequentially, which means that the second rover
  won't start to move until the first one has finished moving.
  
  UNEXECUTABLE INSTRUCTIONS 
  		If a rover is started in an invalid position then it will remain there.
  		If a rover is instructed to move from a valid position to an invalid position 
  		 then it will remain in the valid position and not execute any more instruction.s
  
  MALFORMED INSTRUCTIONS
  		If instructions are not formated exactly as described above then this program's
  		behaviour is not defined.
'''

from math import *
import sys

# Convert between compass point and angle theta 
compass = 'ENWS'
def compass2theta(c): return compass.find(str(c))
def theta2compass(t): return compass[t]

# Function to create dicts representing points, rover states and state transforms
def Point(x, y):  return {'x':x, 'y':y }
def State(x, y, theta):  return {'x':x, 'y':y, 'theta':theta}
def Xform(distance, dtheta): return { 'distance':distance, 'dtheta':dtheta}

# Functions to convert a state to an (x,y) tuple and a string
def position(state): return (state['x'], state['y'])
def showState(state): return str(state['x']) + ' ' + str(state['y']) + ' ' + theta2compass(state['theta'])

# Apply a transform to a rover state
def applyXform(state, xform): 
    theta = (state['theta'] + xform['dtheta']) % 4
    x = state['x'] + int(round(cos(math.pi/2.0)*xform['distance']))
    y = state['y'] + int(round(sin(math.pi/2.0)*xform['distance']))
    return State(x,y,theta)

# The rover's environment comprises the plaateau boundary and the previous rovers
boundary = {'ll': Point(0, 0), 'ur':Point(0, 0) }
rovers = []

# Tell if a point is inside a boundary
def inside(point, boundary):
    ll, ur = boundary['ll'], boundary['ur']
    within = lambda i: ll[i] <= point[i] and point[i] <= ur[i]
    return within('x') and within('y')
  
# Tell is a state is valid  
def isValid(state):
    if not inside(state, boundary):
        return False;
    for r in rovers:
        if position(r) == position(state):
            return False;
    return True;

# Mappings of commands to state transforms
moves = {'M':Xform(1,0), 'L':Xform(0,1), 'R':Xform(0,-1) }

# Process a string of single letter movement commands
def performMoves(state, line):
    if isValid(state):
        for c in line:
            newState = applyXform(state, moves[c])
            if not isValid(newState):
                break
            state = newState
    return state

# Read a line from stdin and strip trailing spaces 
def readLine(): return sys.stdin.readline().rstrip('\r\n ')
  
# Process a mars rover script according to the directions at the start of this file
def processScript():
    line = readLine()
    if line:
        x1,y1 = map(int, line.split())
        boundary['ur'] = Point(x1, y1)
        while line:
            line = readLine()
            if line:
                start = line.split()
                x,y = map(int, start[:2])
                theta = compass2theta(start[2])
                state = State(x, y, theta)   
                line = readLine()
                if line:
                    state = performMoves(state, line)
                rovers.append(state)
                print showState(state)
           
if __name__ == '__main__':   
    processScript()

       

        