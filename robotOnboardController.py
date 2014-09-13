import socket
import serial.tools.list_ports as list_ports
import serial
import json


def prepInt(i):
  # Prepares an integer for writing to serial.
  return str(i)+"q"

#Variable Setup
originSpeed = 47
motorOffset = 55 #The offset for the left motor (see Arduino Program).


#Check each COM port for Arduino's special "ACM0" port.
serialConnection = None
for port in list_ports.comports():
  for data in port:
    if "ACM0" in data:
      print "-- Attempting serial connection..."
      serialConnection = serial.Serial(data, baudrate=9600)
      print "-- Established serial connection!"
      break

if not serialConnection:
  print "ERROR: Failed to make serial connection!"


#Set up the TCP connection.
print "-- Server ready..."
bufferSize = 4096
TCP_port = 50007
TCP_host = ""
socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketConnection.bind((TCP_host, TCP_port))
socketConnection.listen(1)

controllerConnection, controllerAddress = socketConnection.accept()
print "\n-- Connected to the controller at address: {}".format(controllerAddress)

while True:
  raw_data = controllerConnection.recv(4096)
  if data==None:
    timeout += 1
    print "ERROR: No data received! ({})".format(timeout)
  else:
    timeout = 0

  if timeout > 1000:
    break

  try:
    mostRecentData = raw_data.split("$")[-2]
    data = json.loads(mostRecentData)

  except IndexError:
    break

  except Exception as e:
    print e
    continue

  #Create a string representation of the `left` and `right` motor values.
  left = data["left"]
  right = data["right"]+motorOffset

  #Make sure `left` and `right` are each 3-digits long.

  #Write the speeds to the serial ports
  serialConnection.write(prepInt(left))
  serialConnection.write(prepInt(right))

  print "Left: {}   --  Right: {}".format(left, right)

  #NOTE: Requires that integers are being written to Serial by the Arduino.
  #print "Arduino: {} -- {}".format(serialConnection.read(3), serialConnection.read(3))


#On quit, write the motors to stop.
serialConnection.write(prepInt(originSpeed+motorOffset))
serialConnection.write(prepInt(originSpeed))

controllerConnection.close()
print "Stopping robit!"

