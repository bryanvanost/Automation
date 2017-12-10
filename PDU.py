#!/usr/bin/python3

import eventlog

class PDU:
    def __init__(self):
        eventlog.record('Started PDU Module')
        self.PDU_A = []
        self.s= []

    def getPrompt(self):
        try:
            self.s.sendall(bytes("\n", "utf-8"))
            time.sleep(.02)
            received = str(self.s.recv(1024), "utf-8")
            if (received[2:5]=="pm>"):
                return (1)
            else:
                print (received)
                return (0)
        except:
            print ("Not Logged In")

    def connect (self,HOST,PORT):
        self.PDU_A = serialPort()
        self.s=self.PDU_A.connect(HOST,PORT)
        user="admin"
        passwd="1234qwer"
        try:
            self.s.sendall(bytes("\n", "utf-8"))
            time.sleep(.1)
            received = str(self.s.recv(1024), "utf-8")
            if (received[2:11]=="Username:"):
                s.sendall(bytes(user + "\n"+passwd+"\n", "utf-8"))
                print("Login Sent")
            elif (received[2:11]=="Password:"):
                self.s.sendall(bytes("\n", "utf-8"))
            elif (received[2:5]=="pm>"):
                print ("logged In")
            else:
                print("Received: {}".format(received))
                print (len (received))
        except:
            print("Failed to connect to PDU")

        finally:
            return None

    def ON(self,outlet):
        print (self.getPrompt())
        print (self.getPrompt())
        print (self.getPrompt())
        msg=("on "+str(outlet))
        self.s.sendall(bytes(msg, "utf-8"))
        time.sleep(.1)
        received = str(self.s.recv(1024), "utf-8")
        print (received)

    def OFF(self,outlet):
        print (self.getPrompt())
        print (self.getPrompt())
        print (self.getPrompt())
        msg=("off "+str(outlet))
        self.s.sendall(bytes(msg, "utf-8"))
        time.sleep(.1)
        received = str(self.s.recv(1024), "utf-8")
        print (received)


    def close (self):
        self.s.sendall(bytes("\n", "utf-8"))
        time.sleep(.02)
        received = str(self.s.recv(1024), "utf-8")
        if (received[2:5]=="pm>"):
            self.s.sendall(bytes("exit\n", "utf-8"))
            time.sleep(.02)
            received = str(self.s.recv(1024), "utf-8")
            print("Disconnected from PDU")
        self.s.close()


def main():
    print("start PDU")




if __name__ == '__main__':
        main()
else:
    eventlog.record("PDU Module Improted")
