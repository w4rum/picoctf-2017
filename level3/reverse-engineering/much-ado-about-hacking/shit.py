#!/bin/python

from subprocess import *
import string

ending = open("ending.txt", "r").read()

alph = string.printable.replace('"', 'A').replace('`', 'A')
cur = ''
i = 0

while (len(cur) < len(ending)-1):
    for c in alph:
        trei = (cur[:i] + c + cur[i+1:])[::-1] + ' '
        try:
            output = check_output('echo "%s" | ./MuchAdoAboutHacking' % trei, shell=True, timeout=1).decode()
            if len(output) > i and output[i] == ending[i]:
                cur = cur[:i] + c + cur[i+1:]
                i += 1
                print('Progress: ' + cur[::-1])
                break
        except CalledProcessError:
            pass

print("DONE")
