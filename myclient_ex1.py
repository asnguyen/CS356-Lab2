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
 serverPort = 35605

 clientSocket = socket(AF_INET,SOCK_DGRAM)
 
 #PACKET CREATION STEP
 myarray = array('l')
 myarray.append(0x8164)
 myarray.append(0x0107)
 
 cookie = create_cookie()
 myarray.append(int(cookie[0],16))
 myarray.append(int(cookie[1],16))

 clientSocket.connect((serverName,serverPort))
 clientName = clientSocket.getsockname()
 ipaddr = int(ip_to_hex(clientName[0]),16)
 print ipaddr
 mytuple = split_num(int(ipaddr))
 myarray.append(int(mytuple[0],16))
 myarray.append(int(mytuple[1],16))
 
 myarray.append(0) #dummy Checksum
 myarray.append(54327)

 #creating checksum
 mask = 0xFFFF
 checksum = create_checksum(myarray)
 checksum = checksum ^ mask
 myarray[6] = checksum
 
 #creating the packet#
 mypkt = pack_packet(myarray)

 #PACKET SENDING STEP
 clientSocket.settimeout(10)
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
   ret = retarray[7]
   if (ret & 0x8000) == 0x0000:
    print "P.O Box number is " + str(retarray[7])+'\n'
   else: 
    if (ret & 0x8000) == 0x8000:
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
 print "End"

#HELPER FUNCTIONS
def ip_to_hex(ipaddr):
  ret = binascii.hexlify(inet_aton(ipaddr))
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
