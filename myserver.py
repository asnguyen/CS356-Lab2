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
 for line in f:                                               #Reads in the database file into a dictionary for random access
  ln = line.split()
  lookup[ln[0]] = int(ln[1])
 
 #create socket and bind it
 tempSocket = socket(AF_INET,SOCK_DGRAM)                      #This temporary socket will be used to figure out what the 
 tempSocket.connect(("128.83.144.56",35604))                  #host's IP address is
 clientname = tempSocket.getsockname()

 mySocket = socket(AF_INET,SOCK_DGRAM)                        #This is our main socket that will recieve input from 
 mySocket.bind((clientname[0],54327))                         #the CS Server. The port will be fixed on 54327
 socketName = mySocket.getsockname()
 print socketName                                             #Displays the IP address and the socket of server
 
 tempSocket.close()                                           #Closes the temporary packet
 
 #server loop 
 while(True):
  #recieve packet
  retpkt = mySocket.recvfrom(65565)                           #Continuously waits and recieve UDP packets
  retarray = unpack("!HHHHHHHH", retpkt[0])                   #Unpacks the packet in order to read as an array of 16bit numbers
  #check version/format/checksum
  bSyntax   = 1	                                              #boolean for Syntax. Assumed to be correct
  bChecksum = 1                                               #boolean for Checksum. Assumed to be correct
  bLookup   = 1                                               #boolean for our Lookup dictionary. Assumed that it exists
  retFormat1 = retarray[0]                                    #retFormat1 and retFormat2 are used to check the format of
  retFormat2 = retarray[1]                                    #our packet. 
  retChecksum = create_checksum(retarray)                     #uses our checksum algo to calculate checksum
  if int(retFormat1)!=0x0164 or int(retFormat2)!=0x0107:      #The format needs to be in the hex form 01 64 01 07
   bSyntax = 0
  if int(retChecksum) != 65535:                               #checks to see if the checksum is 65535 or contains 16 ones
   bChecksum = 0
  #look up ssn
  ssn = ''
  result = ''
  if bSyntax == 1 and bChecksum == 1:
   #need to recreat SSN and see if its our lookup table
   higherB = retarray[4]                                      #performs the inverse of the split_num function to recreate
   lowerB  = retarray[5]                                      #the original ssn input 
   ssn  = (higherB << 16) + lowerB
   if str(ssn) not in lookup:                                 #dict function: x not in dict checks to see if x is in the set of 
    bLookup = 0                                               #keys in dict.
   if str(ssn) in lookup:
    result = lookup[str(ssn)]                                 #if key is there we can just access the dict with that index  
  #create response packet
  mask = 0xFFFF                                               #calculating a new checksum for the packet that we need to send
  myarray = array('l')                                        #to the client. We can do this by createing a new array with the
  myarray.append(0x4164)                                      #values that we want to be in our packet
  myarray.append(0x0107)
  myarray.append(retarray[2])
  myarray.append(retarray[3])
  myarray.append(retarray[4])
  myarray.append(retarray[5])
  myarray.append(0)                                           #adds a dummy value as checksum in order to calculate the new one
  if bLookup == 0:                                            #need to add the correct result 
   myarray.append(0x8004)
  if bChecksum == 0:
   myarray.append(0x8001)
  if bSyntax == 0:
   myarray.append(0x8002)
  if bLookup == 1:
   myarray.append(result)
  checksum = create_checksum(myarray)
  checksum = checksum ^ mask
  myarray[6] = checksum                                       #replaces the dummy value with the correct value of checksum

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
