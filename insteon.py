#!/usr/bin/python3
import extron
import devices
import sys
import time


#print (sys.version)




class Insteon:
    def __init__(self):
        self.s = None
        self.msg=b''
        
    def __del__(self):
        print("Insteon Class Closed")

    def connect(self,HOST,serialPort):
        try:

            #Connetc to IPL250
            #HOST is the IP devices in sting
            #PORT is the serial port {1,2..} in string
            self.s=extron.Extron()
            self.s.connectToSerialPort(HOST, serialPort)

            print ('Connected to PLM ' + HOST )
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
            self.s.sendToSerialPort(msg)
            
        except:
            print ("  -Failed to Send to Serial Port")
        
    def unpackStdMsg(self,msg):         
        msgOriginator=msg[2:5]
        msgAdr=msg[6:8]
        cmd1=msg[9]
        cmd2=msg[10]
        
        eventtime=time.asctime( time.localtime(time.time()) )
        
        print(eventtime + ": Received ",end='')
        #b'\x030'
        if (cmd1==48):
            print('Ping ACK',end='')
        #b'\x11'
        elif cmd1==17:
             print('UP/ON',end='')
        elif cmd1==18:
             print('Double UP/ON',end='')
        #b'\x13
        elif cmd1==19:
            print('DOWN/OFF',end='')
        elif cmd1==20:
            print('Double DOWN/OFF',end='')
            
        else:
            print('unk..',end='')
            print(hex(cmd1),end=' ')
            print(hex(cmd2),end='')
            
        print(" from ",end='')
        
        if ((msgOriginator)==b'\x1D\xDB\xCC'):
            print ('kitchen')
        elif ((msgOriginator)==b'\x1D\xE3\x5B'):
            print ('downstairs wall')
        elif ((msgOriginator)==b'\x1D\xDE\x9A'):
            print('upstairs bedroom') 
        elif ((msgOriginator)==b'\x13\x99\xA2'):
            print('living Room') 
        elif ((msgOriginator)==b'\x0E\xA7\xA6'):
            print('lamp1')  
        elif ((msgOriginator)==b'\x0E\x9A\x17'):
            print('lamp2')  
        else:
            for i in msgOriginator:
                print (hex(i),end=' ')
        print()
        return (cmd1)
        
        #print("\nReceived Standard Message:",end='')  
        #for i in msg:
        #    print (hex(i),end=' ')
        
        #print("  Device Category: %s %s"%(hex(msg[5]),hex(msg[6])))
        # print("  Firmware Revision: %s"%(hex(msg[7])))
       
        
    def listen(self,toAddr='',cmd1='',cmd2=''):
        start=time.time()
        
        self.msg=b''
        while True:
            self.msg=self.msg+self.s.listenToSerialPort()
            
            while (False):
                for i in self.msg:
                    print(hex(i),end=' ')
                    print()
            
            if ((self.msg[-1:])==b'\x15'):
                print ('FAIL')
                return (msg)
            
            #elif ((msg[-1:])==b'\x06'):
            #    return(msg)
            
             
            elif ((self.msg[:3])==b'\x02\x54\x02'):
                print("The SET Button was Tapped")
                self.msg=b''
                
            elif ((self.msg[:3])==b'\x02\x54\x03'):
                print("There was a SET Button Press and Hold for more than three seconds.")
                self.msg=b''
                
            elif ((self.msg[:3])==b'\x02\x54\x04'):
                print("The SET Button was released after a SET Button Press and Hold event was recorded.")
                self.msg=b''
                
            elif ((self.msg)==b"".join([b'\x02',b'\x62',toAddr,b'\x0f',cmd1,cmd2,b'\x06'])):
                print ('  <Command confirmed by PLM')
                self.msg=b''
                    
            elif (len(self.msg)>=11):
                if (self.msg[:2]==b'\x02\x50'):
                    if (self.msg[2:5]==toAddr):
                        delay=time.time()-start
                        print ('  <Received Ping ACK after',delay,'seconds')
                        break
                    
            elif (len(self.msg)>=11):
                if (self.msg[:2]==b'\x02\x50'):
                    delay=time.time()-start
                    print('  <' + delay + ': Valid Standard Message Received from',end=" ")
                    print(self.getDeviceName(msg[2:5]))
                    
                    print ('  <Flag', hex(self.msg[8]))
                                        
                    if (self.msg[8]==47):
                        print('  <SD ACK Message')
                        
                        
                    print ('  <Command1', int(self.msg[9]))
                    print ('  <Command2', int(self.msg[10]))
        
                    for i in msg:
                        print (hex(i),end=' ')
                    opflg=msg[-1]
                    print(bin(opflg))              
                    break  

                        
            #elif (len(msg)>1):
            #    print('dd')
            #   for i in msg:
            #      print (hex(i),end=' ')
                

    def reset(self):
        """
        send 2 bytes
        Rx 9 Bytes
        """
        print (' -Reset IM')
        msg=b'\x02\x67'
        self.s.sendToSerialPort(msg)
        while True:
                msg=self.s.listenToSerialPort()
                if (msg == b'\x02\x67\x06'):
                    print ('  -IM has been Reset')
                    break
                
    def getInfo(self):
        """
        send 2 bytes
        Rx 9 Bytes
        """
        print (" >Requesting IM Info")
        msg=b'\x02\x60'
        self.send (msg)
        msg=self.listen()
        if len(msg)==9 and msg[8]==6:
            print("  <PLM Address: %s %s %s"%(hex(msg[2]),hex(msg[3]),hex(msg[4])))
            print("  <Device Category: %s %s"%(hex(msg[5]),hex(msg[6])))
            print("  <Firmware Revision: %s"%(hex(msg[7])))
        else:
            print("  -Request for IM Information Fail")
            for i in msg:
                print (hex(i))
                sys.exit()
                

    def getConfig(self):
        ## send 2 bytes
        # Received 6 bytes
        # system returing 4 bytes??
        print (' >Requesting IM Configuration')
        msg=b'\x02\x73'
        self.send (msg)
        msg=self.listen()     
        if msg[-1]==6:
            print("  <IM Configuration Received %s (%s)"%(hex(msg[2]),bin (msg[2])))
        else:
            print ('FAIL: ',)
            for i in msg:
                print (hex(i)), 
    
        #bit 6 = 1 Puts the IM into Monitor Mode 
        #bit 4 = 1 Disable host communications Deadman feature (i.e. allow host to delay more than 240 milliseconds between sending bytes to the IM)

    def setConfig(self,configFlag):
        ## Send 3 byte
        #Rx 4 bytes
        print (" >Setting IM Configuration")       
        msg=b'\x02\x6B' + (bytes([configFlag]))
        self.send (msg)
        msg=self.listen()
        if len(msg)==4 and msg[3]==6:
            print ("  <IM Configuration Set: %s (%s)"%(hex(msg[2]),bin (msg[2])))

    def unpackAllLinkResponse(self,msg):
        pass
    
    def getFirstAllLink(self):
        print (' -Request First All Link')
        msg=b'\x02\x69'
        rx=self.send (msg)
        if rx[-1:]==b'\x06':
            print ("  -Database is Not Empty")
            msg=self.s.listenToSerialPort()
            if (msg[:2]==(b'\x02W')):
                msgOriginator=msg[4:7]
                msgAdr=msg[6:8]
                print("ALL-Link Record Response Received from",end=' ')
                for i in msgOriginator:
                    print (hex(i),end=' ')
                
                
        elif rx[-1:]==b'\x15':
            print ("  -Database is Empty")
        else:
            print("WTF")
            
    
    def sendInsteonCmd(self,deviceAddr,cmd1,cmd2):
        startofIMCmd=b'\x02'
        sendInsteonStdMsgCmd =b'\x62'
        msgFlag=b'\x0f'
        #print ('Sending Standard Insteon Command')
        msg=(b"".join([startofIMCmd, sendInsteonStdMsgCmd,deviceAddr,msgFlag,cmd1,cmd2]))
        msg=self.send (msg)
          
    def getDeviceName(self,deviceAddr):
        if ((deviceAddr)==b'\x1D\xDB\xCC'):
            return ('kitchen')
        elif ((deviceAddr)==b'\x1D\xE3\x5B'):
            return ('downstairs wall')
        elif ((deviceAddr)==b'\x1D\xDE\x9A'):
            return('upstairs bedroom') 
        elif ((deviceAddr)==b'\x13\x99\xA2'):
            return('living Room')  
        elif ((deviceAddr)==b'\x0E\xA7\xA6'):
            return('lamp1')  
        elif ((deviceAddr)==b'\x0E\x9A\x17'):
            return('lamp2')  
        elif ((deviceAddr)==b'\x43\x6E\xFE'):
            return('PLM')  
        else:
            for i in deviceAddr:
                print(hex(i))

    def ping(self,deviceAddr):
        
        startofIMCmd=b'\x02'
        sendInsteonStdMsgCmd =b'\x62'
        msgFlag=b'\x0f'
        
        print(" >Sending ping to ",end='')   
        print(self.getDeviceName(deviceAddr))
        
                
        pingCmd=b'\x30'
        cmd1=pingCmd
        cmd2=b'\xff'
        #send command and listen for a response 
        self.sendInsteonCmd(deviceAddr, cmd1, cmd2)
        self.listen(deviceAddr, cmd1, cmd2)
       
        
    
    def status(self,deviceAddr):
        startofIMCmd=b'\x02'
        sendInsteonStdMsgCmd =b'\x62'
        msgFlag=b'\x0f'
        lightStatusRequest=b'\x19'
        cmd1=lightStatusRequest
        cmd2=b'\x00'
        
        print(" >Requesting status from ",end='')
        print(self.getDeviceName(deviceAddr))
        
        
        self.sendInsteonCmd(deviceAddr, cmd1, cmd2)

        msg=b''
        while True:
            msg=msg+self.s.listenToSerialPort()
        
            if ((msg[-1:])==b'\x15'):
                print ('fail')
                break
                
            elif ((msg)==b"".join([startofIMCmd,sendInsteonStdMsgCmd,deviceAddr,msgFlag,cmd1,cmd2,b'\x06'])):
                #print ('  <Status command confirmed by PLM')
                msg=b''
                     
            elif (len(msg)>=11):
                if (msg[:2]==b'\x02\x50'):
                    print('Insteon Message',end=' ')
                    if (msg[2:5]==deviceAddr):
                        print('from',self.getDeviceName(deviceAddr))
                        onlvl=round((int(msg[10])/2.55),2)
                        print ('  <Device is at',onlvl,'%')   
                        break  
                    
    def getID(self,deviceAddr): 
        startofIMCmd=b'\x02'
        sendInsteonStdMsgCmd =b'\x62'
        msgFlag=b'\x0f'
        getID=b'\x10'
        cmd1=getID
        cmd2=b'\x00'
            
        print(" >Requesting ID from ",end='')
        print(self.getDeviceName(deviceAddr))
            
        self.sendInsteonCmd(deviceAddr, cmd1, cmd2)
    
        msg=b''
        while True:
            msg=msg+self.s.listenToSerialPort()
           
            if ((msg[-1:])==b'\x15'):
                print ('fail')
                break
                    
            elif ((msg)==b"".join([startofIMCmd,sendInsteonStdMsgCmd,deviceAddr,msgFlag,cmd1,cmd2,b'\x06'])):
                #print ('  <Status command confirmed by PLM')
                msg=b''
 
            elif (len(msg)>=11):
                if (msg[:2]==b'\x02\x50'):
                    #print('  <Insteon Message',end=' ')
                    if (msg[2:5]==deviceAddr):
                        #print('from',self.getDeviceName(deviceAddr),end=' ')            
                        if (msg[5:8]==b'\x43\x6e\xfe'):
                            #print('to PLM', end=' ')
                            msg=b''
                            
                        elif (msg[9]==1):
                            devCat=msg[5]
                            subCat=msg[6]
                            if (devCat==1):
                                print("  <Dimmable Lighting Control")
                                
                                if (subCat==0):
                                    print("  <LampLinc V2 [2456D3]")
                                elif (subCat==25):
                                    print('  <SwitchLinc Dimmer [with beeper] [2476D]')
                                elif (subCat==32):
                                    print('  <SwitchLinc Dimmer (Dual-Band) [2477D]')
                                print('  <Firmware',hex(msg[7]))
                                break
                            else:
                                print('No Idea')
                                
                            
            
                    
    def set(self,deviceAddr,onLvl):
        start=time.time()
        startofIMCmd=b'\x02'
        sendInsteonStdMsgCmd =b'\x62'
        msgFlag=b'\x0f'
        
        print(" >Sending direction to ",end='')   
        print(self.getDeviceName(deviceAddr))
        cmd1=b'\x11'
        if (onLvl==100):
            cmd2=b'\xff'
        if (0<= onLvl < 100):
            onLvl=int(onLvl*2.55)
            cmd2=bytes([onLvl])
        else:
            onLvl=b'0'
        
        self.sendInsteonCmd(deviceAddr, cmd1, cmd2)
        
        msg=b''
        while True:
            msg=msg+self.s.listenToSerialPort()
            #print(msg)
            
            if ((msg[-1:])==b'\x15'):
                print ('fail')
                break
                
            elif ((msg)==b"".join([startofIMCmd,sendInsteonStdMsgCmd,deviceAddr,msgFlag,cmd1,cmd2,b'\x06'])):
                #print ('  <Status command confirmed by PLM')
                msg=b''
                     
            elif (len(msg)>=11):
                if (msg[:2]==b'\x02\x50'):
                    if (msg[2:5]==deviceAddr):
                        onlvl=round((int(msg[10])/2.55),2)
                        print ('  <Device is at',onlvl,'%')   
                        break  
    

    def getOpFlag(self,deviceAddr):
        start=time.time()
        startofIMCmd=b'\x02'
        sendInsteonStdMsgCmd =b'\x62'
        msgFlag=b'\x0f'
        
        print(" >Sending reqeust for Op Flag to ",end='')   
        print(self.getDeviceName(deviceAddr))

        cmd1=b'\x1F'
        cmd2=b'\x00'       
        self.sendInsteonCmd(deviceAddr, cmd1, cmd2)
        
        msg=b''
        while True:
            msg=msg+self.s.listenToSerialPort()
            print(msg)
            
            
            if ((msg[-1:])==b'\x15'):
                print ('fail')
                break
                
            elif ((msg)==b"".join([startofIMCmd,sendInsteonStdMsgCmd,deviceAddr,msgFlag,cmd1,cmd2,b'\x06'])):
                #print ('  <Status command confirmed by PLM')
                msg=b''
                     
            elif (len(msg)>=11):
                if (msg[:2]==b'\x02\x50'):
                    for i in msg:
                        print (hex(i),end=' ')
                    opflg=msg[-1]
                    print(bin(opflg))              
                    break  



    def allON(self):
        
        self.set(devices.lamp2,100)
        self.set(devices.kitchen,100)
        self.set(devices.upstairsBedRm,100)
        #self.set(devices.livingRm,100)
        self.set(devices.lamp1,100)
        
    def allOFF(self):
        
        self.set(devices.lamp2,0)
        self.set(devices.kitchen,0)
        self.set(devices.upstairsBedRm,0)
        #self.set(devices.livingRm,0)
        self.set(devices.lamp1,0)
       
    def peek(self,toAddr):
        setAddrMSB=b'\20'
        
        peekOneByte=b'\x2B'
        cmd1=setAddrMSB
        cmd2=b'\x00'
        
        print(" >Peek ",end='')   
        print(self.getDeviceName(toAddr))

              
        self.sendInsteonCmd(toAddr, cmd1, cmd2)
        
        msg=b''
        while True:
            msg=msg+self.s.listenToSerialPort()
            if ((msg[-1:])==b'\x15'):
                print ('fail')
                break
                
            elif ((msg)==b"".join([b'\x02',b'\x62',toAddr,b'\x0f',cmd1,cmd2,b'\x06'])):
                print ('  <Command confirmed by PLM')
                msg=b''
                
            elif (len(msg)>=11):
                if (msg[:2]==b'\x02\x50'):
                    print('  <Valid Standard Message Received from',end=" ")
                    print(self.getDeviceName(msg[2:5]))
                    
                    print ('  <Flag', hex(msg[8]))
                                        
                    if (msg[8]==47):
                        print('  <SD ACK Message')
                        
                        
                    print ('  <Command1', int(msg[9]))
                    print ('  <Command2', int(msg[10]))
        
                    for i in msg:
                        print (hex(i),end=' ')
                    opflg=msg[-1]
                    print(bin(opflg))              
                    break  




def main ():
    ##Host='www.vansot.com
    HOST='192.168.1.14'
    serialPort='1'
    print('Insteon script running')
    lighting=Insteon()
    lighting.connect(HOST, serialPort)
    #lighting.getInfo()
    #lighting.getConfig()
    #lighting.getOpFlag(devices.livingRm)
    
    #lighting.reset()
    #configFlag=0b01000000
        #        76543210
        #Bit 7 = 1 Disables automatic linking when the user pushes and holds the SET Button (see Button Event Report). 
        #Bit 6 = 1 Puts the IM into Monitor Mode
        #Bit 5 = 1 Disables automatic LED operation by the IM. The host must now control the IMs LED using LED On50 Off51.
        #Bit 4 = 1 Disable host communications Deadman feature (i.e. allow host to delay more than 240 milliseconds between sending bytes to the IM). See IM RS232 Port Settings8
        #Bits 3 - 0 Reserved for internal use. Set these bits to 0.
    #lighting.setConfig(configFlag)
   
    lighting.ping(devices.kitchen)
    lighting.ping(devices.wall)
    lighting.ping(devices.upstairsBedRm)
    #lighting.ping(devices.lamp1)
    #lighting.ping(devices.lamp2)
    #lighting.ping(devices.livingRm)
    
    #lighting.status(devices.kitchen)
    #    lighting.status(devices.wall)
    #    lighting.status(devices.upstairsBedRm)
    #lighting.getID(devices.lamp1)
    #lighting.getID(devices.lamp2)
    #lighting.getID(devices.kitchen)
    #lighting.getID(devices.wall)
    #lighting.getID(devices.livingRm)
    #lighting.status(devices.lamp2)
    
    lighting.peek(devices.lamp1)
    
    
    #lighting.allON()
    #lighting.allOFF()
    #lighting.set(devices.kitchen,100)
    
    
    
    #lighting.getFirstAllLink()
    #print()
    #pingCmd=b'\x30'
    #onCmd=(b'\x12')
    #offCmd =(b'\x13')
   
    #address=devices.upstairsBedRm
    
    #address=devices.kitchen
    #address=devices.lamp1
    #address=devices.lamp2
    #cmd1=pingCmd
    #cmd2=b'\xff'
    #lighting.sendInsteonCmd(address, cmd1, cmd2)
    
    

if __name__ == "__main__":
    main()
else:
    print ('Insteon Module Imported')

