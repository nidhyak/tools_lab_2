#!/usr/bin/env python3
import sys

def xor(argv):
    with open(argv[0], "rb") as file_0:
        byte_0 = bytearray(file_0.read())

    with open(argv[1], "rb") as file_1:
        byte_1 = bytearray(file_1.read())

    print(f"Length of {argv[0]}: {len(byte_0)}")
    print(f"Length of {argv[1]}: {len(byte_1)}")

    length = min(len(byte_0), len(byte_1))

    output = bytearray(length)

    for i in range(length):
        output[i] = byte_0[i] ^ byte_1[i]

    with open(argv[2], 'wb') as output_file:
        output_file.write(output)

if __name__ == '__main__':
    xor(sys.argv[1:])
