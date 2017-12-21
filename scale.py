'''
Created on Dec 20, 2017

@author: bryanvanost
'''

import extron
import sys
import time


class Scale(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.s = None
        self.msg=b''
        
        
    def __del__(self):
        print("Insteon Class Closed")
        
    def connect(self,HOST,PORT):
        try:

            #Connetc to IPL250
            #HOST is the IP devices in sting
            #PORT is the serial port {1,2..} in string
            self.s=extron.Extron()
            self.s.connectToSerialPort(HOST, PORT)
            
            #print(self.s.listenToSerialPort())

            print ('Connected to ' + HOST )
        except:
            print ("Failed to Connect to IPL")
        
    def getWeight(self):
        msg=b'\x48'
        self.s.sendToSerialPort(msg)
        print(self.s.listenToSerialPort())
        
        
def main ():
    ##Host='www.vansot.com
    HOST='192.168.1.13'
    serialPort='1'
    print('Start Scale Module')
    PS50=Scale()
    PS50.connect(HOST, serialPort)
    PS50.getWeight()
    
    
    
    
if __name__ == "__main__":
    main()
else:
    print ('Scale Module Imported')