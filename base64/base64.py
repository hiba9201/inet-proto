#!/usr/bin/env python3
import sys


CODE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

if __name__ == '__main__':
    word_bytes = bytes(sys.argv[1], 'utf-8')
    bits = ''.join(list(map(lambda l: bin(l)[2:].zfill(8), word_bytes)))
    right = len(bits) % 6
    bits = bits.ljust(len(bits) + 6 - right, '0')

    splitted = [bits[x:x + 6] for x in range(0, len(bits), 6)]
    res = []

    for octet in splitted:
        if len(octet) < 6:
            octet = octet + (6 - len(octet)) * "0"
        res.append(CODE[int(octet, 2)])

    if len(res) % 4 != 0:
        for _ in range(4 - len(res) % 4):
            res.append('=')

    print(''.join(res))
