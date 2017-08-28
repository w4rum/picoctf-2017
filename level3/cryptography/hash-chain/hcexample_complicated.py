#!/bin/python2

import md5 #Must be run in python 2.7.x
import re
from pwn import *
import pickle

f = open("users", 'rb')
users = pickle.load(f)
f.close()

#users = {
#    i : []
#for i in range(0,10000)
#}

def fill(user, target):
    newFill = []
    newFill.append(target)
    hashc = target
    for i in range(0,1000):
        hashc = md5.new(hashc).hexdigest()
        if len(users[user]) > 0 and hashc == users[user][0]:
            oldFill = users[user]
            users[user] = newFill
            users[user].append(oldFill)
            print('user len after %d' % len(users[user]))
            return
        newFill.append(hashc)
        #print('newFill len %d' % len(newFill))
    users[user] = newFill

def find(user, target):
    for i in range(1, len(users[user])):
        if users[user][i] == target:
            return users[user][i-1]
    return None


def makeConn():
    try:
        return remote('shell2017.picoctf.com', '5715')
    except pwnlib.exception.PwnlibException:
        return makeConn()

done = False
it = 0
while not done:
    it += 1
    try:
        conn = makeConn()
        conn.recv()
        conn.send('f\n')
        conn.recvline()
        request = conn.recvline()
        user = int(re.search(r'as user (\d+)', request).group(1))
        request = conn.recvline()
        target = re.search(r'[a-f0-9]+', request).group(0)
        conn.recv()
        curFind = None
        if len(users[user]) > 0:
            print 'FOUND AGAIN: %d' % user
            curFind = find(user, target)
        if curFind == None:
            print 'Filling (%d / %s)' % (user, target)
            fill(user, target)
        else:
            print 'Found for ' + str(user)
            conn.send(curFind + '\n')
            print conn.recv()
            done = True

        if it > 99:
            f = open("users", 'wb')
            pickle.dump(users, f)
            f.close()
            it = 0
        conn.close()
    except :
        f = open("users", 'wb')
        pickle.dump(users, f)
        f.close()
        conn.close()
        done = True
    

