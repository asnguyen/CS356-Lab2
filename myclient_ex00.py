#!/usr/bin/python

from socket import *
from random import *
from array  import *
from struct import *
from sys    import *


def main():
 print "Start"

 serverName = "128.83.144.56"
 serverPort = 35604

 clientSocket = socket(AF_INET,SOCK_DGRAM)
 print "Socket successfully created"
 
 #PACKET CREATION STEP
 myarray = array('l')
 #myarray.append(0x071F)
 myarray.append(0x01640107)
 for i in range(0,len(myarray)):
  print myarray[i]
 
 cookie = create_cookie()
 print "cookie created"
 myarray.append(int(cookie,16))
 #myarray.append(0)

 #myinput = input("Enter Social Security Number: ")
 #print hex(myinput)
 myarray.append(123456789)

 #creating checksum
 myarray.append(0)

 print myarray

 #creating the packet#
 mypkt = pack_packet(myarray)
 print "created packet"

 #PACKET SENDING STEP
 clientSocket.settimeout(5)
 clientSocket.sendto(mypkt,(serverName, serverPort))
 
 #PACKET RECIEVING STEP
 retpkt = clientSocket.recvfrom(65565)  
 


 print "End"

def create_checksum(ar):
 #read in the array and convert each entry to two 16-integer and then add them 1 compliment style
 checksum = 0
 return checksum

def create_cookie():
 num = randrange(0,9000)
 cookieNum = hex(num)
 return cookieNum
  

def pack_packet(ar):
 pkt = ''
 for i in range(0,len(ar)):
  #pkt = pkt + pack('!H',ar[i])
  pkt = pkt + pack('!I',ar[i])
 return pkt

if __name__ == "__main__":
  main()
