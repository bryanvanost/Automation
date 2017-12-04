#!/usr/bin/python3
import socket
import sys
import time;  # This is required to include time module.



class Extron:
        def __init__(self):
              self.s = None

        def connect(self,HOST):
                try:
                        #Connetc to IPL250
                        PORT = 23
                        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.s.connect((HOST, PORT))
                        received = str(self.s.recv(128), "utf-8")
                        if(received[2:68]==str("(c) Copyright 2009, Extron Electronics, IPL 250, V1.15, 60-1026-81")):
                                print ("Connected to IPL250 @ " + HOST +":" + str(PORT))

                        if(received[2:68]==str("(c) Copyright 2009, Extron Electronics, IPL T S2, V1.15, 60-544-81")):
                                print ("Connected to IPL T S2 @ " + HOST +":" + str(PORT))
                        
                        
                except:
                        print ("Failed to Connect to IPL")
                        
        def openSerialPort (self,HOST,serialPort,msg):
                try:
                        #Connetc to IPL250
                        PORT = 2000+ serialPort
                        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.s.connect((HOST, PORT))
                        received = str(self.s.recv(128), "utf-8")
                                        
                        
                except:
                        print ("Failed to Connect to Serial Port")

                

        def RelayOn(self,Rly):

                try:
                        print ("Attempt to ON Relay")
                        self.s.sendall(bytes(str(Rly) + "*1O","utf-8"))
                        received = str(self.s.recv(128), "utf-8")
                        if(received[:10]==str("Cpn02 Rly1")):
                                print ("Relay "+ str(Rly) + " is ON")

                except:
                        print ("Realy " + Rly + "Failed to ON")   

        def RelayOff(self,Rly):
                try:
                        print ("Attempt to OFF Relay")
                        self.s.sendall(bytes(str(Rly) + "*2O","utf-8"))
                        received = str(self.s.recv(128), "utf-8")                
                        if(received[:10]==str("Cpn02 Rly0")):
                                print ("Relay "+ str(Rly) + " is OFF")
                
                except:
                        print ("Realy " + Rly + "Failed to OFF")      



        def sendIRmsg(self,command):
                try:
                        msg = chr(27)+"1,0,"+ str(command)+ ",0IR" + chr(13)
                        self.s.sendall(bytes(msg, "utf-8"))
                        #time.sleep(.01)
                        received = str(self.s.recv(512), "utf-8")
                        var1=(int(received[3:6]))
                        var2=(int(received[7:10]))
                        var3=(int(received[11:14]))
                        var4=(int(received[15:18]))
                        print (var1, var2, var3, var4)
                except:
                        print ("Fail")


        def send2SerialPort (self, port, msg):
                try:
                        null

                except:
                        print("Failed " + msg)

def main():
	print('hello')







if __name__ == "__main__":
    main()
else:
	print ('Import Extron Module')

