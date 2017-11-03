#!/usr/bin/python

from socket import *
from random import *
from array  import *
from struct import *
from sys    import *


def main():
 print "Start"

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
