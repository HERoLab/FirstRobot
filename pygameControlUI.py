import sys, tty, termios, thread, time

import pygame
from pygame.locals import *

#Variable Setup.
originSpeed = 47
maxSpeed = 74
minSpeed = 20
turnSpeed = 10
leftSpeed = originSpeed
rightSpeed = originSpeed
breakDelay = 10
eventWait = 50
keysPressed = None

# # # # # # # # # # #  Main UI Function  # # # # # # # # # # # 
def main():
  global rightSpeed, leftSpeed, originSpeed, breakDelay, eventWait

  # Initialise screen
  pygame.init()
  screen = pygame.display.set_mode((400, 250))
  fontStyle = pygame.font.SysFont("Comic Sans MS", 24)
  pygame.display.set_caption('Robit Operiter')

  # Fill background
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((250, 250, 250))

  # Blit everything to the screen
  screen.blit(background, (0, 0))
  pygame.display.flip()

  #Final Variable Setup:
  noKeyDuration = 0


  while True:
    pygame.event.pump() #Flush the last key presses.

    #Get the keys that are currently pressed.
    key = pygame.key.get_pressed()

    # # # # # # Session Controls # # # # # # # 
    #End the session if "q" "b" or "ESC" are pressed. Also slow the 'bot.
    if key[ pygame.K_q ] or key[ pygame.K_b ] or key[ pygame.K_ESCAPE ]:
      rightSpeed = changeSpeed(originSpeed)
      leftSpeed = changeSpeed(originSpeed)
      print "QUITTING"
      return 

    # # # # # Wheel Speed Controls # # # # # #
    #Increase/Decrease Speed
    if key[ pygame.K_UP ]:
      rightSpeed = incrementSpeed(1, rightSpeed)
      leftSpeed = incrementSpeed(1, leftSpeed)
    elif key[ pygame.K_DOWN ]: 
      rightSpeed = incrementSpeed(-1, rightSpeed)
      leftSpeed = incrementSpeed(-1, leftSpeed)

    #Turn By Altering Speeds Choose car-turn and pivot-turn based on speed.
    if key[ pygame.K_LEFT ]:
      if leftSpeed+turnSpeed > maxSpeed:
          leftSpeed = changeSpeed(maxSpeed-turnSpeed)
          rightSpeed = changeSpeed(maxSpeed)
      elif leftSpeed == originSpeed:
          leftSpeed = changeSpeed(originSpeed-turnSpeed)
          rightSpeed = changeSpeed(turnSpeed)
      else:
          rightSpeed = changeSpeed(leftSpeed+turnSpeed)
    if key[ pygame.K_RIGHT ]:
      if rightSpeed+turnSpeed > maxSpeed:
          rightSpeed = changeSpeed(maxSpeed-turnSpeed)
          leftSpeed = changeSpeed(maxSpeed)
      elif rightSpeed == originSpeed:
          rightSpeed = changeSpeed(originSpeed-turnSpeed)
          leftSpeed = changeSpeed(turnSpeed)
      else:
          leftSpeed = changeSpeed(rightSpeed+turnSpeed)

    #If no key is pressed, slow to a stop.
    if noKeyPressed():
      if noKeyDuration > breakDelay:
        noKeyDuration = noKeyDuration*3/4
        if rightSpeed > originSpeed: rightSpeed -= 1
        elif rightSpeed < originSpeed: rightSpeed += 1
  
        if leftSpeed > originSpeed: leftSpeed -=1
        elif leftSpeed < originSpeed: leftSpeed += 1
      else:
        noKeyDuration += 1

    color = (255, 100, 100)
    left = fontStyle.render("Left: {}".format(leftSpeed-originSpeed), 1, color)
    right = fontStyle.render("Right: {}".format(rightSpeed-originSpeed), 1, color)
    direction = fontStyle.render("Direction: {}".format(getDirection()), 1, color)

    screen.blit(background, (0, 0))
    screen.blit(left, (50, 50))
    screen.blit(right, (50, 80))
    screen.blit(direction, (50, 110))
    pygame.display.flip()
    pygame.time.delay(eventWait)

# # # # # # # # # # #  Helper Functions  # # # # # # # # # # #
def incrementSpeed(change, speed):
  if change > 0 and speed+change < maxSpeed:
    return speed+change
  elif change < 0 and speed+change > minSpeed:
    return speed+change
  else:
    return speed 

def changeSpeed(newSpeed):
  if minSpeed <= newSpeed <= maxSpeed:
    return newSpeed
  else:
    print 0, 0, "ERROR: Cannot set speed to {}".format(newSpeed) 
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

#Mostly taken from: http://rosettacode.org/wiki/Keyboard_input/Keypress_check#Python
def getch():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch

def updateKeysPressed():
  global keysPressed
  print keysPressed
  keysPressed = getch()

def noKeyPressed():
  global keysPressed
  return keysPressed == None

#Start a thread to look for lack of key-presses.
thread.start_new_thread(updateKeysPressed, ())

#If called from the command line, run the UI function.
if __name__ == "__main__": main()
