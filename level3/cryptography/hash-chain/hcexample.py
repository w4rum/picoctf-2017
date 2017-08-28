#!/bin/python2

import md5 #Must be run in python 2.7.x
import re
from pwn import *
import pickle

def find(user, target):
    hashc = str(user)
    prev = ''
    while True:
        hashc = md5.new(hashc).hexdigest()
        if hashc == target:
            return prev
        prev = hashc

def makeConn():
    try:
        return remote('shell2017.picoctf.com', '5715')
    except pwnlib.exception.PwnlibException:
        return makeConn()

conn = makeConn()
conn.recv()
conn.send('f\n')
conn.recvline()
request = conn.recvline()
user = int(re.search(r'as user (\d+)', request).group(1))
request = conn.recvline()
target = re.search(r'[a-f0-9]+', request).group(0)
conn.recv()
curFind = find(user, target)
conn.send(curFind + '\n')
print conn.recv()
    

