#!/usr/bin/python3
import extron
import devices
from unittest import case




class Insteon:
    def __init__(self):
        self.s = None

    def connect(self,HOST,serialPort):
        try:

            #Connetc to IPL250
            #HOST is the IP devices in sting
            #PORT is the serial port {1,2..} in string
            #extron.connect(
            self.s=extron.Extron()
            self.s.connectToSerialPort(HOST, serialPort)
            print (self.s)
            #Extron.openSerialPort(HOST,PORT)

            print ('Connected to PLM ' + HOST )
            #self.getIMInfo()
        except:
            print ("Failed to Connect to IPL")



    def close(self):
        try:
            self.s.close()
            #print  (self.s)
            print ('Closed')
        except:
            print ("Failed to Close")

    def send (self,msg):
        try:
            #msg = bytes.fromhex(msg)
            print ('  -Sending ' + str(len(msg)) + ' character message:',end=' ')
            for i in msg:
                print (hex(i),end=' ')

            print()
            msg=self.s.sendToSerialPort(msg)
        except:
            print ("  -Failed to Send to Serial Port")
        finally:
            return (msg)
        
    def unpackStdMsg(self,msg): 
        print("Received Standard Message:",end='')  
        for i in msg:
            print (hex(i),end=' ')
        msgOriginator=msg[2:5]
        msgAdr=msg[6:8]
        cmd1=msg[9]
        cmd2=msg[10]
        #b'\x030'
        if (cmd1==48):
            print('Ping',end='')
        #b'\x11'
        elif cmd1==17:
             print('ON',end='')
        #b'\x13
        elif cmd1==19:
            print('OFF',end='')
        else:
            print (hex(cmd1),end='')
        
        print("  from:",end=' ')
        for i in msgOriginator:
            print (hex(i),end=' ')
        #print("  Device Category: %s %s"%(hex(msg[5]),hex(msg[6])))
        # print("  Firmware Revision: %s"%(hex(msg[7])))
       
       
       
       
       
        
    def listen(self):
        msg=b''
        print("\nListening..\n")
        msg=msg+self.s.listentoSerialPort()
        #Check if this is a Standard Message Received
        for i in msg:
                print (hex(i),end=' ')
        if (len(msg)==11):
            if (msg[:2]==b'\x02\x50'):
                self.unpackStdMsg(msg)
            
                

    def reset(self):
        """
        send 2 bytes
        Rx 9 Bytes
        """
        print ('Reset IM')
        msg=b'\x02\x67'
        rx=self.send (msg)
        if (rx == b'\x02\x67\x06'):
            print ('IM has been Reset')

    def getInfo(self):
        """
        send 2 bytes
        Rx 9 Bytes
        """
        print (" -Requesting IM Info")
        msg=b'\x02\x60'
        msg=self.send (msg)
        if len(msg)==9 and msg[8]==6:
            print("  PLM Address: %s %s %s"%(hex(msg[2]),hex(msg[3]),hex(msg[4])))
            print("  Device Category: %s %s"%(hex(msg[5]),hex(msg[6])))
            print("  Firmware Revision: %s"%(hex(msg[7])))
        else:
            print(" -Request for IM Information Fail")
            for i in msg:
                print ((i))

    def getConfig(self):
        ## send 2 bytes
        # Received 6 bytes
        # system returing 4 bytes??
        print ('Requesting IM Configuration')
        msg=b'\x02\x73'
        msg=self.send (msg)     
        if msg[-1]==6:
            print("  IM Configuration Received %s (%s)"%(hex(msg[2]),bin (msg[2])))
        else:
            print ('FAIL: ',)
            for i in msg:
                print ((i)), 
    
        #bit 6 = 1 Puts the IM into Monitor Mode 
        #bit 4 = 1 Disable host communications Deadman feature (i.e. allow host to delay more than 240 milliseconds between sending bytes to the IM)

    def setConfig(self,configFlag):
        ## Send 3 byte
        #Rx 4 bytes
        print ("Setting IM Configuration")       
        msg=b'\x02\x6B' + (bytes([configFlag]))
        print (type(msg))
        msg=self.send (msg)
        if len(msg)==4 and msg[3]==6:
            print ("  IM Configuration Set: %s (%s)"%(hex(msg[2]),bin (msg[2])))


    def getFirstAllLink(self):
        print ('Request First All Link')
        msg=b'\x02\x69'
        rx=self.send (msg)
        if rx[-1:]==b'\x15':
            print ("Database is Empty")

    def sendInsteonCmd(self,deviceAddr,cmd1,cmd2):
        startofIMCmd=b'\x02'
        sendInsteonStdMsgCmd =b'\x62'
        msgFlag=b'\x0f'
        print ('Sending Standard Insteon Command')
        msg=(b"".join([startofIMCmd, sendInsteonStdMsgCmd,deviceAddr,msgFlag,cmd1,cmd2]))
        msg=self.send (msg)   
        print(msg)
    


"""
        



        

        


        
def bullshit():
        #BedRm=   insteonDevice("Bed Room",'\x13\x99\xA2','2477D')
        #LivingRm=insteonDevice("Living Room",'\x1D\xE3\x5B','2477D')
        #DiningRm=insteonDevice("Dining Room",'\x1D\xDE\x9A','2477D')
        #CouchLamp=insteonDevice("Couch Lamp",'\x13\xB3\x25','2475D')
        #Other=insteonDevice("OTHER",'\x13\xB1\x00','2475D')
        
        HOST = "192.168.1.14"
        PORT = 1
        S2 = Extron()
        #0250+devices+flags+cmd1+cmd2
        insteonHeader = bytes.fromhex('0262')
        Device1=bytes.fromhex('0ea7a6')
        #devAddr_LivingRm= bytes.fromhex('1399A2')
        
        DeviceA=bytes.fromhex('1DDBCC')
        DeviceB=bytes.fromhex('1DE35B')
        
        
        Lamp2=b'\x0E\xA5\x44'
        Lamp3=b'\x0E\xA7\xA6'
        #devices=Device2
        msgflag=bytes.fromhex('0f')
        pingCmd='0f'
        onCmd=bytes.fromhex('30')
        offCmd='13'
        beep=b'\x30'
        cmd1=onCmd
        cmd2=bytes.fromhex('FF')
        try:
                print ('Sending Standard Insteon Command')
                onlevel=255
                #print (bin(onlevel))
                #print (hex(onlevel))
                #msg=insteonHeader+LivingRm+msgflag+cmd1+cmd2
                
                msg=insteonHeader+DeviceA+msgflag+cmd1+cmd2
                
                #msg=insteonHeader+Device4+msgflag+cmd1+cmd2
                print (msg)

                inMessage=Insteon.connect (HOST, 1, msg)
                for i in inMessage:
                        print (hex(i),end=' ')
                print()



                #
                
                #msg='0262'+Device3+msgflag+cmd1+cmd2
                #msg=S2.openSerialPort (HOST, 1, msg)
                #time.sleep(1)
                
                #msg='0262'+Device4+msgflag+cmd1+cmd2
                #msg=S2.openSerialPort (HOST, 1, msg)
                #time.sleep(1)

                #msg='0262'+Device5+msgflag+cmd1+cmd2
                #msg=S2.openSerialPort (HOST, 1, msg)
                #time.sleep(1)

                #msg='0262'+Device6+msgflag+cmd1+cmd2
                #msg=S2.openSerialPort (HOST, 1, msg)
                #time.sleep(1)

                #msg='0262'+Device7+msgflag+cmd1+cmd2
                #msg=S2.openSerialPort (HOST, 1, msg)
                #time.sleep(1)
                
        except: 
            print ('FAIL')
            exit()





def main():
        
        
        devices=Kitchen
        

        
        cmd1=pingCmd
        cmd2=b'\x00'
        #Apt501.sendInsteonCmd(devices,cmd1,cmd2)



        #Apt501.sendInsteonCmd(LivingRm,cmd1,cmd2)
        #Apt501.sendInsteonCmd(Upstairs,cmd1,cmd2)
        #Apt501.sendInsteonCmd(Kitchen,cmd1,cmd2)
        
                
        TriLamp=b'\x0E\x9A\x17'
        devices=TriLamp
        Apt501.getFirstAllLink()
        
        
        
        #Apt501.sendInsteonCmd(devices,cmd1,cmd2)
        
        
        Apt501.close()

        #PLM01Adr='\x0f\x43\x69','2412S'
        #PLM='\x43\x6E\xFE'
        #TriLamp= insteonDevice("Office Lamp",'\x0e\xa7\xa6','2456D3')
        #Office=  insteonDevice("Office",'\x09\x97\x01','2486D')
        #BedRm=   insteonDevice("Bed Room",'\x13\x99\xA2','2477D')
        #LivingRm=insteonDevice("Living Room",'\x1D\xE3\x5B','2477D')
        #DiningRm=insteonDevice("Dining Room",'\x1D\xDE\x9A','2477D')
        #CouchLamp=insteonDevice("Couch Lamp",'\x13\xB3\x25','2475D')
        #Other=insteonDevice("OTHER",'\x13\xB1\x00','2475D')
        #try:
                
                #getIMInfo()
                #getIMConfig()
                #resetIM()
                #setIMConfig()
                #getIMConfig()
                #sendInsteonCmd()
                #resetIM()
               

        #finally:
                #IPL_A.close()
                #IPL_B.close()
                #PDU_A.close()
                #print ('Connection Closed')


"""


def main ():
    HOST='192.168.1.14'
    serialPort='1'
    print('Inston script running')

    lighting=Insteon()
    lighting.connect(HOST, serialPort)
    
    lighting.getInfo()
    
    configFlag=0b01000000
        #        76543210
        #Bit 7 = 1 Disables automatic linking when the user pushes and holds the SET Button (see Button Event Report49). 
        #Bit 6 = 1 Puts the IM into Monitor Mode (see About Monitor Mode45in the Notes below). 
        #Bit 5 = 1 Disables automatic LED operation by the IM. The host must now control the IMs LED using LED On50 Off51.
        #Bit 4 = 1 Disable host communications Deadman feature (i.e. allow host to delay more than 240 milliseconds between sending bytes to the IM). See IM RS232 Port Settings8
        #Bits 3 - 0 Reserved for internal use. Set these bits to 0.
    lighting.setConfig(configFlag)
    lighting.getConfig()
    #lighting.reset()
    
    #lighting.getFirstAllLink()
    print()
    pingCmd=b'\x30'
    onCmd=(b'\x12')
    offCmd =(b'\x13')
   
    address=devices.kitchen
    cmd1=pingCmd
    cmd2=b'\xff'
    #lighting.sendInsteonCmd(address, cmd1, cmd2)
    
    address=devices.upstairsBedRm
    cmd1=pingCmd
    cmd2=b'\xff'
    lighting.sendInsteonCmd(address, cmd1, cmd2)
    lighting.listen()
    while 1:
        lighting.listen()
    

if __name__ == "__main__":
    main()
else:
    print ('Insteon Module Imported')

