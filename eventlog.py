#!/usr/bin/python3



import time

def record(msg):
        eventtime=time.asctime( time.localtime(time.time()) )
        print (msg)
        file = open('testfile.txt','a+')
        file.write(eventtime + " " + str(msg) + "\n")
        file.close()

