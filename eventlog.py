#!/usr/bin/python3


import time
location='/tmp/testfile.txt'
def record(msg):
    eventtime=time.asctime( time.localtime(time.time()) )
    print (msg)
    file = open(location,'a+')
    file.write(eventtime + " " + str(msg) + "\n")
    file.close()
