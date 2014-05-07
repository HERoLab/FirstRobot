'''
UNFINISHED:
    incrementSpeed

I DECLARE THIS CODE AND ALL TRADEMARKS OF THE WALT DISNEY CORPORATION MY PROPERTY.  SO SAY WE ALL.
@author: jack
'''
import time
import serial.tools.list_ports as list_ports
import serial
import Tkinter as tk
from subprocess import check_output

class Robot_Driver(object):
    def __init__(self):
        self.mySerial = serial.Serial() #initialize a blank serial object
            
        #Jaguar speed range:
        self.j_mid = 47 #STOP
        self.j_min = 20 #Full REVERSE
        self.j_max = 74 #Full FORWARD
        self.offset = 55 #offset for left motor settings (see arduino program)
        self.ESTOP = 0 #Command to stop both motors immediately.
        
        #Motor speed settings (stopped by default):
        self.l_motor = self.j_mid
        self.r_motor = self.j_mid
        
        root = tk.Tk()
        self.cvs = tk.Canvas(root,height=600,width=600)
        
        self.arduinoLink(None) #initialize connection with arduino
        self.bindings()  #Bind the robot command keys
        
        self.cvs.pack()
        self.cvs.mainloop()

    def arduinoLink(self,event):
        '''Check COM ports for an arduino (ACM0)'''
        if event and event.char==' ':
            print 'space'
        if self.mySerial.name is None:
            ports = list_ports.comports() #Get currently list of COM ports
            #print ports
            for port in ports:
                for data in port:
                    if 'ACM0' in data:  #ACM0 is the special COM port created for microcontrollers like arduino
                        mySerial = serial.Serial(data,baudrate=9600)
                        print 'serial started on ' + data
                        self.bindings()
                        break
            print 'Arduino not found!'
        else:
            print 'already connected on port ' + str(self.mySerial.port)
    

            
    
    def setSpeed(self,l_speed=0,r_speed=0):
        '''Checks if specified motor speeds are withhin the allowed range, 
        and then sets them via serial.'''
        if (l_speed <= self.j_max+self.offset and 
            l_speed >= self.j_min+self.offset):#if l_speed is in range
                self.mySerial.write(bytes(l_speed))
                self.l_speed = l_speed
        if (r_speed <= self.j_max and r_speed >= self.j_min):#if l_speed is in range
                self.mySerial.write(bytes(r_speed))
                self.r_speed = r_speed      
       
#     def incrementSpeed(self,event):
#         if event.char =='w':
#             
#         elif event.char =='a': 
#         elif event.char =='s':
#         elif event.char =='d':
            
    def center(self,event):
        '''Sets robot on a straight path by equalizing motor speeds.'''
        if ((self.l_motor > self.j_mid and self.r_motor > self.j_mid) or #if robot is isn't just spinning in place
            (self.l_motor < self.j_mid and self.r_motor < self.j_mid)):
            temp = bytes((self.l_motor+self.r_motor)/2)
            self.setSpeed(l_motor=temp, r_motor=temp)
        else: #if robot is spinning, just stop it.
            self.setSpeed(l_motor = self.j_mid, r_motor = self.j_mid)
            
    def bindings(self):
        self.cvs.bind_all('<KeyPress-p>', self.arduinoLink) #manually check for an arduino connection
        if self.mySerial.name is not None:
            '''bind WASD for incrementing speed:'''
            self.cvs.bind_all('<KeyPress-w>', self.incrementSpeed) #more FORWARD
            self.cvs.bind_all('<KeyPress-a>', self.incrementSpeed) #more LEFT
            self.cvs.bind_all('<KeyPress-s>', self.incrementSpeed) #more REVERSE
            self.cvs.bind_all('<KeyPress-d>', self.incrementSpeed) #more REVERSE
            
            self.cvs.bind_all('<KeyPress-space>', self.incrementSpeed) #STOP
            self.cvs.bind_all('<KeyPress-c>', self.center) #CENTER (set motor speeds equal)
            
            #self.cvs.bind_all('<Shift-KeyPress-space>', self.emergencyStop) #EMERGENCY STOP
            
    
if __name__=="__main__":
    robit = Robot_Driver()

    
    
    