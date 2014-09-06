import socket
import serial.tools.list_ports as list_ports
import serial
import json

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
  left = str(data["left"]+motorOffset)
  right = str(data["right"])

  #Make sure `left` and `right` are each 3-digits long.
  while (len(left)<3):
    left = "0"+left
  while (len(right)<3):
    right = "0"+right

  #Write the speeds to the serial ports
  serialConnection.write(left)
  serialConnection.write(right)

  print "Left: {}   --  Right: {}".format(left, right)
  print "Arduino: {}".  format(serialConnection.read())


#On quit, write the motors to stop.
serialConnection.write(str(originSpeed+motorOffset))
serialConnection.write(str(originSpeed))

controllerConnection.close()
print "Stopping robit!"

