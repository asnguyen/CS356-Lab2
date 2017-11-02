#!/usr/bin/python

from socket import *
import random
import array



def main():
 print "Start"

 serverName = "128.83.144.56"
 serverPort = "35604"

 clientSocket = socket(AF_INET,SOCK_DGRAM)
 print "Socket successfully created"
 
 #clientSocket.connect((serverName, serverPort))

 myarray = array.array('l')
 myarray.append(0x071F)
 #myarray.append(0x01640107)
 for i in range(0,len(myarray)):
  print myarray[i]

 print "End"




########
if __name__ == "__main__":
  main()
