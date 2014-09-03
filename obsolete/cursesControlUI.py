import curses

#Screen setup.
screen = curses.initscr()
curses.cbreak()
curses.noecho()
screen.timeout(120) #Allow "no input" to be read as -1.

screen.keypad(1)
screen.addstr(0,10,"Controls started!")


#Taken mostly from: 
# http://stackoverflow.com/questions/10693256/how-to-accept-keypress-in-command-line-python


#Variable Setup.
originSpeed = 47
maxSpeed = 74
minSpeed = 20
turnSpeed = 10
leftSpeed = originSpeed
rightSpeed = originSpeed
key = ""

# # # # # # # # # # #  Helper Functions  # # # # # # # # # # #
def incrementSpeed(change, speed):
  if change > 0 and speed+change < maxSpeed:
    return speed+change

  elif change < 0 and speed+change > minSpeed:
    return speed+change

  else:
     screen.addstr(0, 0, "ERROR: Cannot increment speed to {}".format(speed+change)) 
     curses.endwin()
     return originSpeed
 

def changeSpeed(newSpeed):
  if minSpeed < newSpeed < maxSpeed:
    return newSpeed
  else:
    screen.addstr(0, 0, "ERROR: Cannot set speed to {}".format(newSpeed)) 
    curses.endwin()
    return originSpeed

def getDirection():
  if leftSpeed > rightSpeed:
    return "Right"
  elif rightSpeed < leftSpeed:
    return "Left"
  elif leftSpeed==originSpeed:
    return "Standing"
  elif leftSpeed < originSpeed:
    return "Backward"
  else:
    return "Forward"


# # # # # # # # # # #  Main Loop  # # # # # # # # # # #
#While "q" or the escape key is not pressed, loop...
while key!=ord('q') and key!=chr(27):
  #Get the keyboard input.
  key = screen.getch()

  #Clear the screen of previous inputs.
  screen.clear()

  if key==ord("b") or key==ord("q") or key==chr(27): 
    rightSpeed = changeSpeed(originSpeed)
    leftSpeed = changeSpeed(originSpeed)

  #Increase/Decrease Speed
  if key == curses.KEY_UP: 
    rightSpeed = incrementSpeed(1, rightSpeed)
    leftSpeed = incrementSpeed(1, leftSpeed)
  elif key == curses.KEY_DOWN: 
    rightSpeed = incrementSpeed(-1, rightSpeed)
    leftSpeed = incrementSpeed(-1, leftSpeed)

  #Turn By Altering Speeds.
  #Also, allow two turning styles depending on speed: car-turn and pivot-turn.
  if key==curses.KEY_LEFT:
    if leftSpeed+turnSpeed > maxSpeed:
      leftSpeed = changeSpeed(maxSpeed-turnSpeed)
      rightSpeed = changeSpeed(maxSpeed)
    elif leftSpeed == originSpeed:
      leftSpeed = changeSpeed(originSpeed-turnSpeed)
      rightSpeed = changeSpeed(turnSpeed)
    else:
      rightSpeed = changeSpeed(leftSpeed+turnSpeed)
  if key==curses.KEY_RIGHT:
    if rightSpeed+turnSpeed > maxSpeed:
      rightSpeed = changeSpeed(maxSpeed-turnSpeed)
      leftSpeed = changeSpeed(maxSpeed)
    elif rightSpeed == originSpeed:
      rightSpeed = changeSpeed(originSpeed-turnSpeed)
      leftSpeed = changeSpeed(turnSpeed)
    else:
      leftSpeed = changeSpeed(rightSpeed+turnSpeed)

  #If no key is pressed, slow to a stop.
  if key==-1:
    if rightSpeed > originSpeed: rightSpeed -= 1
    elif rightSpeed < originSpeed: rightSpeed += 1

    if leftSpeed > originSpeed: leftSpeed -=1
    elif leftSpeed < originSpeed: leftSpeed += 1

  screen.addstr(1, 0, "Left Speed: {}".format(leftSpeed-originSpeed))
  screen.addstr(2, 0, "Right Speed: {}".format(rightSpeed-originSpeed))
  screen.addstr(3, 0, "Direction: {}".format(getDirection()))
  screen.refresh()


curses.endwin()

