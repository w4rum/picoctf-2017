#!/bin/python

import binascii
import dpkt
import struct
import sys

# Start the pcap file parsing
f = open(sys.argv[1], 'rb')
pcap = dpkt.pcap.Reader(f)

# Create a partial mapping from keycodes to ASCII chars
keysLowercase = {}
keysUppercase = {}
keysLowercase.update({
    i: '[L/' + hex(i) + ']'
    #i: ''
    for i in range(256)
})

keysUppercase.update({
    i: '[U/' + hex(i) + ']'
    #i: ''
    for i in range(256)
})

keysLowercase.update({
    i + 0x4: chr(i + ord('a'))
    for i in range(26)
})
keysUppercase.update({
    i + 0x4: chr(i + ord('A'))
    for i in range(26)
})
keysLowercase.update({
    i + 0x1e: chr(i + ord('1'))
    for i in range(9)
})

keysLowercase[0x27] = '0'
keysLowercase.update({
    0x28: '\n',
    0x2c: ' ',
    0x2d: '-',

    0x2e: '+',
    0x2f: '[',
    0x30: ']',
    51: ';',
    52: '\'',
    55: '.',
    81: '∨',
    82: '∧',
})
keysUppercase.update({
    0x2d: '_',
    0x2f: '{',
    0x30: '}',
})

# Then iterate over each USB frame

# This CTF case includes switching rows by pressing DOWN and UP. The flag is on the third row (indicated by two ENTER-strokes before the first "f"), so we ignore all characters written onto the other lines
layer=0
out=''
for ts, buf in pcap:
    # We are interested only in packets that have one of the expected URB IDs
    ##urb_id = buf[2:10][::-1] # ID is in reverse notation
    #if binascii.hexlify(urb_id) != b'ffffffff84bbec00' and binascii.hexlify(urb_id) != b'ffffffff84bba880':
    #    continue
    #data_length = buf[0:1]
    #if data_length != b'\x1b':
    #    continue
    key_code = buf[0x1D]
    shift = (buf[0x1B] == 0x20)
    if not key_code:
        continue
    # ENTER or DOWN
    #if key_code == 81 or key_code == 0x28:
    #    layer = layer+1
    #    continue
    # UP
    #if key_code == 82:
    #    layer = layer-1
    #    continue
    #if layer == 2:
    if shift:
        out = out + keysUppercase[key_code]
    else:
        out = out + keysLowercase[key_code]
#print('FLAG:')
print(out)
