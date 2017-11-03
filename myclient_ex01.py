#!/usr/bin/python

from socket import *
from random import *
from array  import *
from struct import *
from sys    import *


def main():
 print "Start"
 print "Exercise 0 using port 35607\n"
 serverName = "128.83.144.56"
 serverPort = 35607

 clientSocket = socket(AF_INET,SOCK_DGRAM)
 
 #PACKET CREATION STEP
 myarray = array('l')
 #myarray.append(0x071F)
 myarray.append(0x0164)
 myarray.append(0x0107)
 
 cookie = create_cookie()
 myarray.append(int(cookie[0],16))
 myarray.append(int(cookie[1],16))

 myinput = input("Enter Social Security Number: ")
 mytuple = split_num(myinput)
 #mytuple = split_num(111111111)
 myarray.append(int(mytuple[0],16))
 myarray.append(int(mytuple[1],16))

 #creating checksum
 mask = 0xFFFF
 checksum = create_checksum(myarray)
 checksum = checksum ^ mask
 myarray.append(checksum)
 myarray.append(0x0000)
 
 #creating the packet#
 mypkt = pack_packet(myarray)

 #PACKET SENDING STEP
 clientSocket.settimeout(5)
 count=0
 clientSocket.sendto(mypkt,(serverName, serverPort))
 
 #PACKET RECIEVING STEP
 retpkt = ''
 while count < 5 and retpkt == '':
  try:
   retpkt = clientSocket.recvfrom(65565)
  except OSError as msg:
   count = count + 1
   
 if retpkt != '':  
  retarray =  unpack('!HHHHHHHH', retpkt[0])
  retChecksum = create_checksum(retarray)
  if int(retChecksum) == 65535:
   print "P.O Box number is " + str(retarray[7])+'\n'
  else:
   print "Error: Incorrect Checksum\n"
 else:
  print "Unexpected Error Occured" 
 clientSocket.close()
 print "End"

#HELPER FUNCTIONS
#   split_num() takes in an integer and returns a tuple 
#   of the higher 16 bits and the lower 16 bits
def split_num(num):
 higherB = num >> 16
 lowerB = num - (higherB << 16)
 return hex(higherB), hex(lowerB)

#   ones_comp_add() takes in two number and performs
#   ones compliment addtion on the two numbers
def ones_comp_add(num1, num2):
 mod = 1<<16
 result = num1+num2
 return result if result < mod else (result+1) % mod

#   create_checksum() takes in an array of eight 16 bit numbers and 
#   creates a checksum by adding all the numbers using one's complement
def create_checksum(ar):
 checksum = 0
 for i in range(0,len(ar)):
  checksum = ones_comp_add(checksum,ar[i])
 return checksum

#   create_cookie() create a random integer to be used the cookie and
#   returns a tuple of the highter bits and lower bits
def create_cookie():
 num = randrange(0,9000)
 return split_num(num)
  

#   pack_packet() takes in an array of 16 bit integers and addes them 
#   one by one to the packe 
def pack_packet(ar):
 pkt = ''
 for i in range(0,len(ar)):
  pkt = pkt + pack('!H',ar[i])
 return pkt

if __name__ == "__main__":
  main()
