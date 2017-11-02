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
 myarray.append(0x0164)
 myarray.append(0x0107)
 for i in range(0,len(myarray)):
  print myarray[i]
 
 cookie = create_cookie()
 print "cookie created"
 myarray.append(int(cookie[0],16))
 myarray.append(int(cookie[1],16))

 myinput = input("Enter Social Security Number: ")
 mytuple = split_num(myinput)
 myarray.append(int(mytuple[0],16))
 myarray.append(int(mytuple[1],16))

 #creating checksum
 checksum = create_checksum(myarray)
 myarray.append(checksum)
 myarray.append(0x0000)
 

 print myarray

 #creating the packet#
 mypkt = pack_packet(myarray)
 print "created packet"

 #PACKET SENDING STEP
 clientSocket.settimeout(5)
 clientSocket.sendto(mypkt,(serverName, serverPort))
 
 #PACKET RECIEVING STEP
 retpkt = clientSocket.recvfrom(65565)  
 
 "End"

def split_num(num):
 higherB = num >> 16
 lowerB = num - (higherB << 16)
 return hex(higherB), hex(lowerB)

def ones_comp_add(num1, num2):
 mod = 1<<16
 result = num1+num2
 return result if result < mod else (result+1) % mod

#def create_checksum(ar):
# checksum = 0
# mask = 0xFF 
# for i in range(0,len(ar)):
#  higherB = ar[i] >> 16
#  lowerB = ar[i] - (higherB << 16)
#  checksum = ones_comp_add(checksum,higherB)
#  checksum = ones_comp_add(checksum,lowerB)
# checksum = ones_comp_add(checksum,0)
# checksum = ones_comp_add(checksum,0)
# checksum = checksum ^ mask 
# return checksum

def create_checksum(ar):
 checksum = 0
 mask = 0xFFFF
 for i in range(0,len(ar)):
  checksum = ones_comp_add(checksum,ar[i])
 checksum = ones_comp_add(checksum,0)
 checksum = ones_comp_add(checksum,0)
 checksum = checksum ^ mask
 return checksum

def create_cookie():
 num = randrange(0,9000)
 #num = 2726
 return split_num(num)
  

def pack_packet(ar):
 pkt = ''
 for i in range(0,len(ar)):
  #pkt = pkt + pack('!H',ar[i])
  pkt = pkt + pack('!H',ar[i])
 return pkt

if __name__ == "__main__":
  main()
