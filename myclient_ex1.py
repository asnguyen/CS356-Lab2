#!/usr/bin/python

from socket import *
from random import *
from array  import *
from struct import *
from sys    import *
import binascii


def main():
 print "Start"

 serverName = "128.83.144.56"
 serverPort = 35604

 clientSocket = socket(AF_INET,SOCK_DGRAM)
 
 #PACKET CREATION STEP
 myarray = array('l')
 myarray.append(0x8164)                                       #The new format of the request message: 81 07 01 07
 myarray.append(0x0107)
 
 cookie = create_cookie()                                     #creates a cookie
 myarray.append(int(cookie[0],16))
 myarray.append(int(cookie[1],16))

 clientSocket.connect((serverName,serverPort))                #Connects to the the CS server
 clientName = clientSocket.getsockname()                      #figures out what the IP host is 
 ipaddr = int(ip_to_hex(clientName[0]),16)                    #converts the IP address from string from to a 32 binary format
 mytuple = split_num(int(ipaddr))                             #and then converts the that format to ascii hex so we can add
 myarray.append(int(mytuple[0],16))                           #it into our array
 myarray.append(int(mytuple[1],16))
 
 myarray.append(0)                                            #dummy Checksum 
 myarray.append(54327)                                        #hardcode in the port that our SUT will be using

 #creating checksum
 mask = 0xFFFF                                                #creates the checksum by adding the ones compliment of all
 checksum = create_checksum(myarray)                          #integers in our array and then taking the one's
 checksum = checksum ^ mask                                   #complement of the sum and replacing our dummy value
 myarray[6] = checksum
 
 #creating the packet#
 mypkt = pack_packet(myarray)                                 #packs the packet to send to the CS server

 #PACKET SENDING STEP
 clientSocket.settimeout(10)                                  #allow an ample timeout just in case the CS server has
 count=0                                                      #problems talking to our SUT
 clientSocket.sendto(mypkt,(serverName, serverPort))
 
 #PACKET RECIEVING STEP
 retpkt = ''                                                  #max attempt is 5 resends
 while count < 5 and retpkt == '':
  try:
   retpkt = clientSocket.recvfrom(65565)
  except OSError as msg:
   count = count + 1
   
 if retpkt != '':  
  retarray =  unpack('!HHHHHHHH', retpkt[0])                  #unpacking the packet as usual
  retChecksum = create_checksum(retarray)                     #checking checksum
  if int(retChecksum) == 65535:
   ret = retarray[7]                                          #if the last 16 bit integer is all 0 then we know that the 
   if (ret & 0x8000) == 0x0000:                               #CS server successfully talked to our SUT and got the PO number
    print "Success"
   else: 
    if (ret & 0x8000) == 0x8000:                              #if the most sig bit in on then there was an issue
     result = ret ^0x8000
     if ret == 1:
      print "ERROR: No Response From SUT At All"
     if ret == 2:
      print "ERROR: No Response From SUT To Some Requests"
     if ret == 4:
      print "ERROR: Bad Message From SUT"
     if ret == 8:
      print "ERROR: Probable Bad Message From SUT"
     if ret == 16: 
      print "ERROR: Wrong Result Returned by SUT for a SSN"
     if ret == 32:
      print "Incorrect Error Handling by SUT"
   #DONE WITH INNER ELSE 
  else:
   print "UNKNOWN ERROR"   
 else:
  print "Unexpected Error Occured" 
 clientSocket.close()
 print "\nEnd"

#HELPER FUNCTIONS
def ip_to_hex(ipaddr):                                        #inet_aton creates a 32 bit binary representation of the ip address
  ret = binascii.hexlify(inet_aton(ipaddr))                   #hexlify takes the binary format and converts it to readable hex
  print ret
  return ret
 
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
