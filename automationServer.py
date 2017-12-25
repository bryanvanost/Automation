#!/usr/bin/python3

import socket
import time
import eventlog
#import insteon
import extron
#import PDU
#TEST

def startServer():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    HOST = '0.0.0.0'
    PORT = 47808
    server_address = (HOST, PORT)
    eventlog.record('Starting Automation Server on %s port %s' % server_address)
    
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print ('Waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print ('  connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                eventtime=time.asctime( time.localtime(time.time()) )
                print ('    ',eventtime,'received "%s"' % data)
                if data:
                    interpret (data)
                    eventlog.record(data)
                    print ('      sending data back to the client')
                    connection.sendall(data)
                else:
                    print ('  no more data from', client_address)
                    break
        finally:
            # Clean up the connection
            connection.close()

def interpret (data):
    try:
        #if (chr(data[0])=='a')
        #        print ("A has been pushed")

        data=data.decode("utf-8")
        if (data[:2]=='on'):
            print ("      ON")
            IPL_A = extron.Extron()
            IPL_A.connect('192.168.1.13')
            IPL_A.sendIRmsg(1)
        if (data[:7]=='off'):
            print ("       OFF")

    except:
        print("Unable to interpret command")

def main():
    startServer()

if __name__ == '__main__':
    main()
