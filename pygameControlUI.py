import sys, time

import socket
import json

import pygame
from pygame.locals import *

#Variable Setup.
originSpeed = 47
maxSpeed = 74
minSpeed = 20
turnSpeed = 10
brakeSpeed = 1 #The speed at which to brake per "loop"
stabilizeSpeed = 3 #The speed at which to "stabilize" turns.
leftSpeed = originSpeed
rightSpeed = originSpeed
breakDelay = 10
eventWait = 100
motorOffset = 55 #The offset for the left motor (see Arduino Program).
keysPressed = None

# # # # # # # # # # #  Main UI Function  # # # # # # # # # # #
def main():
  global rightSpeed, leftSpeed, originSpeed, breakDelay, eventWait

  # Initialise screen
  print "__"*10
  print "\n-- Starting the Robit Operator..."
  pygame.init()
  screen = pygame.display.set_mode((400, 250))
  fontStyle = pygame.font.SysFont("Comic Sans MS", 24)
  pygame.display.set_caption('Robit Operiter')

  # Fill background
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0, 0, 0))

  # Blit everything to the screen
  screen.blit(background, (0, 0))
  pygame.display.flip()

  #Final Variable Setup:
  noKeyDuration = 0
  turning = False

  #Set up the TCP connection.
  robotIP = raw_input("\n-- What is the IP of the robit? ")
  TCP_Port = 50007
  socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  socketConnection.connect((robotIP, TCP_Port))
  print "\n-- Connection established!"

  running = True
  while running:

    pygame.event.pump() #Flush the last key presses.
    for event in pygame.event.get():
      try:
        if event.type == QUIT:
            running = False
            break
        elif event.type == KEYUP:
            #Allow only one turn event to trigger at a time.
            if event.key == pygame.K_LEFT:
                turning = False
            elif event.key == pygame.K_RIGHT:
                turning = False
      except KeyboardInterrupt:
        running = False


    #Get the keys that are currently pressed.
    key = pygame.key.get_pressed()

    # # # # # # Session Controls # # # # # # #
    #End the session if "q" "b" or "ESC" are pressed. Also slow the 'bot.
    if key[ pygame.K_q ] or key[ pygame.K_b ] or key[ pygame.K_ESCAPE ]:
      rightSpeed = changeSpeed(originSpeed)
      leftSpeed = changeSpeed(originSpeed)
      running = False

    # # # # # Wheel Speed Controls # # # # # #
    #Increase/Decrease Speed
    if key[ pygame.K_UP ]:
      rightSpeed = incrementSpeed(1, rightSpeed)
      leftSpeed = incrementSpeed(1, leftSpeed)
    elif key[ pygame.K_DOWN ]:
      rightSpeed = incrementSpeed(-1, rightSpeed)
      leftSpeed = incrementSpeed(-1, leftSpeed)

    #Turn By Altering Speeds Choose car-turn and pivot-turn based on speed.
    if key[ pygame.K_LEFT ] and not turning:
      turning = True
      if leftSpeed+turnSpeed > maxSpeed:
          leftSpeed = changeSpeed(maxSpeed-turnSpeed)
          rightSpeed = changeSpeed(maxSpeed)
      else:
          rightSpeed = changeSpeed(leftSpeed+turnSpeed)
    if key[ pygame.K_RIGHT ] and not turning:
      turning = True
      if rightSpeed+turnSpeed > maxSpeed:
          rightSpeed = changeSpeed(maxSpeed-turnSpeed)
          leftSpeed = changeSpeed(maxSpeed)
      else:
          leftSpeed = changeSpeed(rightSpeed+turnSpeed)

    #If no key is pressed, slow to a stop.
    if noKeyPressed(key):
      if noKeyDuration > breakDelay:
        noKeyDuration = noKeyDuration*3/4
        if rightSpeed > originSpeed: rightSpeed -= brakeSpeed
        elif rightSpeed < originSpeed: rightSpeed += brakeSpeed

        if leftSpeed > originSpeed: leftSpeed -= brakeSpeed
        elif leftSpeed < originSpeed: leftSpeed += brakeSpeed

        #Allow the bot to stabilize to be moving forward as well.
        if abs(leftSpeed-rightSpeed) < stabilizeSpeed:
          leftSpeed = (leftSpeed+rightSpeed)/2
          rightSpeed = leftSpeed
        elif originSpeed > leftSpeed > rightSpeed: rightSpeed += stabilizeSpeed
        elif originSpeed > rightSpeed > leftSpeed: leftSpeed += stabilizeSpeed
        elif leftSpeed > rightSpeed > originSpeed: leftSpeed -= stabilizeSpeed
        elif rightSpeed > leftSpeed > originSpeed: rightSpeed -= stabilizeSpeed

      else:
        noKeyDuration += 1

    #Actually send the new speed to the bot.
    print encodeSpeeds(leftSpeed, rightSpeed)
    socketConnection.send(encodeSpeeds(leftSpeed, rightSpeed))

    #Render the UI elements.
    color = (55, 255, 100)
    left = fontStyle.render("Left: {}".format(leftSpeed-originSpeed), 1, color)
    right = fontStyle.render("Right: {}".format(rightSpeed-originSpeed), 1, color)
    direction = fontStyle.render("Direction: {}".format(getDirection()), 1, color)

    #Draw the rendered elements on the screen (strangely called "blit" in PyGame).
    screen.blit(background, (0, 0))
    screen.blit(left, (50, 50))
    screen.blit(right, (50, 80))
    screen.blit(direction, (50, 110))

    #Display (or apparently "flip") the screen.
    pygame.display.flip()

    #Add a delay so the operations don't occur too quickly.
    pygame.time.delay(eventWait)

  #Close the window.
  print "-- Quitting..."
  pygame.quit()
  sys.exit()

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
    print "ERROR: Cannot set speed to {}".format(newSpeed)
    return originSpeed

def getDirection():
  if leftSpeed > rightSpeed:
    return "Right"
  elif rightSpeed > leftSpeed:
    return "Left"
  elif leftSpeed==originSpeed:
    return "Standing"
  elif leftSpeed < originSpeed:
    return "Backward"
  else:
    return "Forward"

#Check if any one of the control keys are pressed.
def noKeyPressed(key):
  return not (
	key[ pygame.K_LEFT ] or
        key[ pygame.K_RIGHT ] or
        key[ pygame.K_UP ] or
        key[ pygame.K_DOWN ] or
        key[ pygame.K_SPACE ] or
        key[ pygame.K_LSHIFT ]
	)

#Delimit JSON by dollar signs in case packets are concatenated.
def encodeSpeeds(leftSpeed, rightSpeed):
  data = {"left": int(leftSpeed), "right": int(rightSpeed)}
  return json.dumps(data)+"$"

#If called from the command line, run the UI function.
if __name__ == "__main__": main()
