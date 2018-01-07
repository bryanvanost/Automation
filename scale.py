
#!/usr/bin/env python

import serial
import struct
import time


SERIALPORT = "/dev/ttyUSB0"
BAUDRATE = 9600
#PS60 communicates at 9600 baud and has Sevin Bits
scale= serial.Serial(SERIALPORT, BAUDRATE,timeout=.05,bytesize=7,parity='E')

if scale.isOpen():
    print(scale)
    scale.flushInput() #flush input buffer, discarding all its contents
    scale.flushOutput()#flush output buffer, aborting current output
    print("ready")
    #H==72==\x48
    #Reqest high resolution weight data by sending 'H', 'L' is Standard Weight, 'K' is Metric Weight 
    getWeight=b'K'

    while True:
        try:
            scale.write(getWeight)
            #read one response
            response = scale.read(10)
            #check for full message; 8 characters starting with STX ending with CR
            for i in response:
                print(hex(i))
            if (len(response)==8):
                print (response[0])
                if (response[0]==2):
                    print (response[7])
                    if (response[7]==13):
                        w=''
                        for i in response[1:7]:
                            w+=chr(i)
                        weight=float(w)
                        print(time.time(),weight,'Kg') 
        except:
            print('fail')
    scale.close()
