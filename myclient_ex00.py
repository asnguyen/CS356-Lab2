#!/usr/bin/python

from socket import *
from random import *
from array  import *
from struct import *
from sys    import *


def main():
 print "Start"

 serverName = "128.83.144.56"                                 #The IP address of the CS server
 serverPort = 35604                                           #Using port 35604
 clientSocket = socket(AF_INET,SOCK_DGRAM)                    #create the UDP socket
 
 #PACKET CREATION STEP
 myarray = array('l')                                         #defines the type of array and addes the first two
 myarray.append(0x0164)                                       #entries that represent the desire format we want
 myarray.append(0x0107)
 
 cookie = create_cookie()                                     #gets the cookie that we will use
 myarray.append(int(cookie[0],16))
 myarray.append(int(cookie[1],16))                           

 myinput = input("Enter Social Security Number: ")            #prompts use for input
 mytuple = split_num(myinput)                                 #splits the integer into its higher order bits
 myarray.append(int(mytuple[0],16))                           #and lower order bits
 myarray.append(int(mytuple[1],16))

 #creating checksum                                           #creates the checksum by adding all of the elements
 mask = 0xFFFF                                                #in the array together using one's complement
 checksum = create_checksum(myarray)                          #addition and then taking the one's complement of 
 checksum = checksum ^ mask                                   #That number.
 myarray.append(checksum)
 myarray.append(0x0000)                                       #adds the empty result
 
 #creating the packet#
 mypkt = pack_packet(myarray)                                 #creates the packet

 #PACKET SENDING STEP            
 clientSocket.settimeout(5)                                   #sets the timeout to be 5 seconds
 clientSocket.sendto(mypkt,(serverName, serverPort))          #sends the packet
 
 #PACKET RECIEVING STEP
 retpkt = clientSocket.recvfrom(65565)                        #recieves the packet
 retarray =  unpack('!HHHHHHHH', retpkt[0])                   #unpacks the format into an array of 16 bit integers
 retChecksum = create_checksum(retarray)                      #calculates the checksum
 if int(retChecksum) == 65535:                                #checks the checksum to see if it is correct
  if (retarray[7] & 0x8000) == 0x8000:                        #checks to see if it was successful
   print "ERROR: "+ hex(retarray[7])+'\n'
  else:
   print "P.O Box number is " + str(retarray[7])+'\n'
 else:
  print "Error Occured\n"
 
 clientSocket.close()
 print "End"

def split_num(num):
 higherB = num >> 16
 lowerB = num - (higherB << 16)
 return hex(higherB), hex(lowerB)

def ones_comp_add(num1, num2):
 mod = 1<<16
 result = num1+num2
 return result if result < mod else (result+1) % mod

def create_checksum(ar):
 checksum = 0
 for i in range(0,len(ar)):
  checksum = ones_comp_add(checksum,ar[i])
 return checksum

def create_cookie():
 num = randrange(0,9000)
 return split_num(num)
  

def pack_packet(ar):
 pkt = ''
 for i in range(0,len(ar)):
  pkt = pkt + pack('!H',ar[i])
 return pkt

if __name__ == "__main__":
  main()
