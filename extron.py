#!/usr/bin/python3
import socket
import eventlog
#import time;  # This is required to include time module.



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
            #print(received)
            if(received[2:68]==str("(c) Copyright 2009, Extron Electronics, IPL 250, V1.15, 60-1026-81")):
                print ("Connected to IPL250 @ " + HOST +":" + str(PORT))
            if(received[2:68]==str("(c) Copyright 2009, Extron Electronics, IPL T S2, V1.15, 60-544-81")):
                print ("Connected to IPL T S2 @ " + HOST +":" + str(PORT))
        except:
            print ("Failed to Connect to IPL")


    def openSerialPort (self,HOST,serialPort):
        print("Making Connection to " + HOST + " serial Port " + serialPort)
        try:
            #Connect to IPL250
            PORT = 2000+ int(serialPort)
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((HOST, PORT))
            #received = str(self.s.recv(128), "utf-8")
            print("Connection established to "  + HOST + " serial Port " + serialPort)

        except:
            print ("Failed to Connect to Serial Port")


    def sendToSerialPort(self,msg):
        self.s.sendall(msg,"utf-8")

        print (msg)

    def RelayClose(self,Rly):
        try:
            print ("Attempt to close relay " + str(Rly),)
            self.s.sendall(bytes(str(Rly) + "*1O","utf-8"))    
            received = str(self.s.recv(128), "utf-8")
            #print (received)
            if(received[:10]==str("Cpn0" + str(Rly) + " Rly1")):
                print ("Relay "+ str(Rly) + " is closed",)
        except:
            print ("Realy " + Rly + "Failed to ON")

    def RelayOpen(self,Rly):
        try:
            print ("Attempt to open relay " + str(Rly),)
            self.s.sendall(bytes(str(Rly) + "*2O","utf-8"))
            received = str(self.s.recv(128), "utf-8")
            if(received[:10]==str("Cpn0" + str(Rly) + " Rly0")):
                print ("Relay "+ str(Rly) + " is open")

        except:
            print ("Realy " + Rly + "Failed to OFF")



    def sendIRmsg(self,IRFunction):
        IRFile=0
        IRPort=1
        try:
            function=self.getIRcommandInfo(IRFile,IRFunction)
            print ("Send " + function + " command to port " + str(IRPort))
            
            #print("Sending IR code")
            msg = chr(27)+"1,0,"+ str(IRFunction)+ ",0IR" + chr(13)
            self.s.sendall(bytes(msg, "utf-8"))
            #time.sleep(.01)
            received = str(self.s.recv(512), "utf-8")
            #X1
            IRPort=(int(received[3:6]))
            #X57
            IRFile=(int(received[7:10]))
            #X58
            IRFunction=(int(received[11:14]))
            #X59
            PlaybackMode=(int(received[15:18]))
            #IR playback mode (0 = play once, 1 = play continuously, 2 = stop). The response includes leading zeros.
           
        except:
            print ("Fail")


    def getIRcommandInfo(self,IRFile,IRFunction):
        try:
            msg = chr(27) + str(IRFile) + ","+ str(IRFunction)+ "IR" + chr(13)
            self.s.sendall(bytes(msg, "utf-8"))
            #time.sleep(.01)
            received = str(self.s.recv(512), "utf-8")
            return (received[:-2])
        except:
            print ("Fail")
        
        

def testRly():
    print ("Test Open and Close of IPL relays")
    
    IPL1Addr='192.168.1.14'
    IPL2Addr='192.168.1.13'
    
    IPL1=Extron()
    IPL2=Extron()
    
    
    IPL1.connect (IPL1Addr)
    IPL2.connect (IPL2Addr)
    
    for i in range(1,5):
        IPL1.RelayClose(i)
        
    for i in range(1,5):
        IPL1.RelayOpen(i)
    
    
    for i in range(1,5):
        IPL2.RelayClose(i)
        
    for i in range(1,5):
        IPL2.RelayOpen(i)
        
       
    
    
def main():
    print('Extron Script Started')
    print('Test Connection to all devices')
    #testRly()
    
    IPL2Addr='192.168.1.13' 
    IPL2=Extron()
    IPL2.connect (IPL2Addr)
    #Power
    #IPL2.sendIRmsg(1)
    
    #Menu
    #IPL2.sendIRmsg(25)
    #Source
    IPL2.sendIRmsg(47)
    #for i in range (1,100):
    #    print(i,)
    #    print(IPL2.getIRcommandInfo(0, i))
   
    
   
    
    #IPL1.RelayClose(1)
    #IPL1.RelayOpen(1)
    
    
    
    
    #laundry.openSerialPort('192.168.1.14','1')
    





if __name__ == "__main__":
    main()
else:
    eventlog.record ("Extron Module Imported")
