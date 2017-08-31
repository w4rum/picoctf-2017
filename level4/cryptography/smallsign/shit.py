#!/usr/bin/python2

from Crypto.PublicKey import RSA
from pwn import *
import re, sys
import socket

host        = 'shell2017.picoctf.com'
port        = '1814'

def info(s):
    log.info(s)

def crack(p):
    # get settings
    p.recvline()
    n = int(re.findall(r'\d+', p.recvline())[0])
    e = int(re.findall(r'\d+', p.recvline())[0])
    info('Collecting prime signatures')
    raw_primes = open("./primes.txt").read().split(', ')[1::2]
    primes = map(int, raw_primes)
    ciphers = {}
    i = 0
    for pr in primes:
        p.sendline(str(pr))
        out = p.recvline()
        ciphers.update({
            pr : int(re.findall(r'\d+', out)[1])
            })
        #print("%d set to %d" % (pr, ciphers[pr]))
        i += 1
        # Server is very slow at signing, can't do more than rougly 170 primes
        # Will take quite some luck - or time - to get a smooth challenge number
        if i > 170:
            primes = primes[0:i]
            break
        print(i)

    p.sendline('-1')
    chall = int(re.findall(r'\d+', p.recvline())[1])
    info('Challenge: %d' % chall)

    info('Factoring challenge')
    f = factor(chall, primes)
    if f == -1:
        return -1
    
    info('Forging signature')
    sig = 1
    print(f)
    for pf in f:
        sig = sig * ciphers[pf] % n
    p.sendline(str(sig))
    p.interactive()

def factor(n, primes):
    rest = n
    factors = []
    for i in range(0, len(primes)):
        if (rest % primes[i] == 0):
            #print('rest= ' + str(rest))
            #print('i= ' + str(i))
            #print('prime= ' + str(primes[i]))
            rest /= primes[i]
            factors.append(primes[i])
            #print('rest= ' + str(rest))
            i -= 1
            if rest == 1:
                break

    if rest == 1:
        return factors
    else:
        info('ERROR: NOT ENOUGH PRIMES TO FACTOR ' + str(n))
        return -1

def connect():
    if len(sys.argv) <= 1 or sys.argv[1] != "46-days":
        info("Executing locally")
        p = process(['./smallsign.py'])
        return p
    else:
        info("Executing on %s:%s" % (host, port))
        s = socket.socket()
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((host, int(port)))
        p = remote.fromsocket(s)
        return p

def reconnect(p):
    p.close()
    return connect()

p = connect()
while (crack(p) == -1):
    p = reconnect(p)
