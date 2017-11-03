#!/usr/bin/python

from socket import *
from random import *
from array  import *
from struct import *
from sys    import *


def main():
 print "Start"
 #load data file
 lookup = dict()
 f = open("ssn-po.dat","r")
 for line in f:
  ln = line.split()
  lookup[ln[0]] = int(ln[1])
 
 #create socket and bind it
 tempSocket = socket(AF_INET,SOCK_DGRAM)
 tempSocket.connect(("128.83.144.56",35604))
 clientname = tempSocket.getsockname()

 mySocket = socket(AF_INET,SOCK_DGRAM)
 mySocket.bind((clientname[0],clientname[1]+1))
 socketName = mySocket.getsockname()
 print socketName
 
 tempSocket.close()
 
 #server loop
 while(True):
  #recieve packet
  retpkt = mySocket.recvfrom(65565)
  retarray = unpack("!HHHHHHHH", retpkt[0])
  print retpkt[1]
  print retarray
  #check version/format/checksum
  bSyntax   = 1
  bChecksum = 1
  bLookup   = 1
  retFormat1 = retarray[0]
  retFormat2 = retarray[1]
  retChecksum = create_checksum(retarray)
  if int(retFormat1)!=0x0164 or int(retFormat2)!=0x0107:
   bSyntax = 0
  if int(retChecksum) != 65535:
   bChecksum = 0
  #look up ssn
  ssn = ''
  result = ''
  if bSyntax == 1 and bChecksum == 1:
   #need to recreat SSN and see if its our lookup table
   higherB = retarray[4]
   lowerB  = retarray[5]
   ssn  = (higherB << 16) + lowerB
   if str(ssn) not in lookup:
    bLookup = 0 
   if str(ssn) in lookup:
    result = lookup[str(ssn)]   
  #create response packet
  mask = 0xFFFF
  myarray = array('l')
  myarray.append(0x4164)
  myarray.append(0x0107)
  myarray.append(retarray[2])
  myarray.append(retarray[3])
  myarray.append(retarray[4])
  myarray.append(retarray[5])
  myarray.append(0)
  if bLookup == 0:
   myarray.append(0x8004)
  if bChecksum == 0:
   myarray.append(0x8001)
  if bSyntax == 0:
   myarray.append(0x8002)
  if bLookup == 1:
   myarray.append(result)
  checksum = create_checksum(myarray)
  checksum = checksum ^ mask
  myarray[6] = checksum

  mypkt = pack_packet(myarray)
  mySocket.sendto(mypkt,retpkt[1])
    
  #write/output response
  print "Client IP address/Port number: "+str(retpkt[1][0])+"-"+str(retpkt[1][1])
  print "-----------------------------------------------------------------------"
  print "[CLient -> MyServer] Request"
  print "[0-3]   "+hex(retarray[0])+" "+hex(retarray[1])
  print "[4-7]   "+hex(retarray[2])+" "+hex(retarray[3])
  print "[8-11]  "+hex(retarray[4])+" "+hex(retarray[5])
  print "[12-15] "+hex(retarray[6])+" "+hex(retarray[7])+"\n"
  if bLookup == 1:
   print "PO number is "+str(result)
  if myarray[7] == 0x8004:
   print "ERROR: Cannot find SSN in database"
  if myarray[7] == 0x8001:
   print "ERROR: Invalid Checksum"
  if myarray[7] == 0x8002:
   print "ERROR: Invalid Syntax"
  print "-----------------------------------------------------------------------"
  print "[MyServer -> Client] Type 0 Response"
  print "[0-3]   "+hex(myarray[0])+" "+hex(myarray[1])
  print "[0-7]   "+hex(myarray[2])+" "+hex(myarray[3])
  print "[8-11]  "+hex(myarray[4])+" "+hex(myarray[5])
  print "[12-15] "+hex(myarray[6])+" "+hex(myarray[7])
  
  
  
 print "End"

#HELPER FUNCTIONS
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
