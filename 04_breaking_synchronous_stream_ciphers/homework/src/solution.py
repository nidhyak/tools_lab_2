#!/usr/bin/env python3

### Filenames
KEYSTREAM = 'keystream'
HINT_GIF_ENC = 'hint.gif.enc'
HINT_GIF = 'hint.gif'
RULE_86_ENC = 'rule86.txt.enc'
RULE_86 = 'rule86.txt'
SUPER_CIPHER_ENC = 'super_cipher.py.enc'
SUPER_CIPER = 'super_cipher.py'

### Extracted from super_cipher.py.enc
RULE = [86 >> i & 1 for i in range(8)]
# reverses bin(86) = 0b01010110 to [0, 1, 1, 0, 1, 0, 1, 0]
N_BYTES = 32
N = 8 * N_BYTES     # 256 bits

def next(x):
    """Hash function that takes an integer and performs bitwise operations to
    generate an integer that is N-bits long.

    Extracted from super_cipher.py.enc

    Parameters
    ----------
    x : int
        Seed value to generate next keystream block 

    Returns
    -------
    y : int
        Next keystream block of N-bit length

    """
    x = (x & 1) << N+1 | x << 1 | x >> N-1
    # xABCDEFy --> yxABCDEFyx
    # (x & 1) << N+1: Prepends last bit to most significant bit (head)
    # x << 1: Shifts original bits to middle to make space
    # x >> N-1: Appends first bit to least significant bit (tail)

    # To reverse, trim the head and tail either
    # by AND with mask then trim tail
    #   x = (((1<<N+1)-1) & x) >> 1
    # or trim tail then AND with mask
    #   x = (x >> 1) & ((1<<N)-1)
    # or take advantage of python strings
    #   x = int('0'+bin(x)[3:-1], 2)

    y = 0
    for i in range(N):
        y |= RULE[(x >> i) & 7] << i
    # idx of RULE is chosen by 3-bit block of x, starting from the tail
    # the 3-bit block moves up by 1 bit per iteration
    # this builds a 256 bit length (32 byte) keystream from the back
    # which is used as the next keystream block
    return y

def prev(y):
    """Reverses next() function from super_cipher.py.

    next() generates the next keystream according to the following bit mapping:

    current triplet -> next possible triplet : current bit -> next possible bit
    0 000 --> (0 000, 4 100) : 0 --> (0, 1)
    1 001 --> (0 000, 4 100) : 1 --> (0, 1)
    2 010 --> (1 001, 5 101) : 1 --> (1, 0)
    3 011 --> (1 001, 5 101) : 0 --> (1, 0)
    4 100 --> (2 010, 6 110) : 1 --> (1, 1)
    5 101 --> (2 010, 6 110) : 0 --> (1, 1)
    6 110 --> (3 011, 7 111) : 1 --> (0, 0)
    7 111 --> (3 011, 7 111) : 0 --> (0, 0)

    To reverse, match the mapping of bits to triplets backwards.
    For example, if y = 0b1011, from left to right
      1 -->   0 -->   1 -->   1 is matched to
    001 --> 011 --> 110 --> 100 or
    010 --> 101 --> 010 --> 100 or
    100 --> 000 --> 001 --> 010 or
    110 --> 101 --> 010 --> 100 

    Therefore x = 001100 or 010100 (reject) or 100010 or 110100 (reject)
    We only accept bitstreams with matching front and back 2 bits (yxABCDEFyx)
    After trimming the bits on valid values of x:
    x = 0110 or 0001 (collision!)

    Parameters
    ----------
    y : int
        Keystream of N-bit length
    
    Returns
    -------
    x : int
        Previous keystream block of N-bit length

    """
    # initial bit to triplet mapping
    bit_to_triplet = {
        '0': ['000', '011', '101', '111'],
        '1': ['001', '010', '100', '110'],
        }
    # subsequent triplet and bit mapping
    triplet_to_triplet = {
        '000': {
            '0': '0',
            '1': '1',
            },
        '011': {
            '0': '1',
            '1': '0',
            },
        '101': {
            '0': '1',
            '1': '0',
            },
        '111': {
            '0': '1',
            '1': '0',
            },
        '001': {
            '0': '1',
            '1': '0',
            },
        '010': {
            '0': '1',
            '1': '0',
            },
        '100': {
            '0': '0',
            '1': '1',
            },
        '110': {
            '0': '1',
            '1': '0',
            },
        }
    # convert y to bit list of 0-padded N-bit binary which includes leading 0
    y = list(format(y, f'0{N}b'))
    # 4 possible inital bitstreams
    bitstreams = bit_to_triplet[y.pop(0)].copy()
    while y:
        bit = y.pop(0)
        # extend each bitstream according to value of bit
        for i, stream in enumerate(bitstreams):
            # check last 3 bits of stream for triplet block
            bitstreams[i] += triplet_to_triplet[stream[-3:]][bit]
    # find valid bitstream with matching 2 bits from head and tail (yxABCDEFyx)
    for stream in bitstreams:
        if stream[:2] == stream[-2:]:
            # trim bits from head and tail (yxABCDEFyx --> xABCDEFy)
            x = int(stream[1:-1], 2)
            return x

def get_seed(k_file=KEYSTREAM):
    """Recovers seed used to generate keystream in super_cipher.py.

    Parameters
    ----------
    k_file : string, optional
        Filename for keystream file
        Defaults to KEYSTREAM

    Returns
    -------
    seed : string
        Seed used to generate keystream

    """
    with open(k_file, 'rb') as key_file:
        keystream = bytearray(key_file.read())
    # extract first set of keystream values
    seed = int.from_bytes(keystream[:N_BYTES], 'little')
    # do 128 (N//2) iterations of prev() to reverse next()
    for i in range(N//2):
        seed = prev(seed)
    seed = seed.to_bytes(N_BYTES, 'little').decode()
    return seed

def next_keystream(keystream):
    """Converts keystream bytes into int before calling the next() function
    to generate the next keystream block.

    Parameters
    ----------
    keystream : bytearray
        Bytearray of keystream

    Returns
    -------
    keystream : bytearray
        Next keystream block

    """
    keystream = int.from_bytes(keystream, 'little')
    keystream = next(keystream)
    keystream = bytearray(keystream.to_bytes(N_BYTES, 'little'))
    return keystream

def xor(bytearray_0, bytearray_1):
    """Exclusive ORs (XOR) the values of two bytearrays.

    Parameters
    ----------
    bytearray_0 : bytearray
    bytearray_1 : bytearray

    Returns
    -------
    output : bytearray
        XOR value of two bytearrays

    """
    length = min(len(bytearray_0), len(bytearray_1))
    output = bytearray(length)
    for i in range(length):
        output[i] = bytearray_0[i] ^ bytearray_1[i]
    return output

def decrypt(e_file, o_file, k_file=KEYSTREAM):
    """Bitwise XOR the keystream to the encrypted file to decrypt it.
    Initial keystream values are obtained from keystream file. Further values
    will be iteratively generated until the entire encrypted file is processed.

    Parameters
    ----------
    e_file : string
        Filename for encrypted file
    o_file : string
        Filename for output file containing decrypted file
    k_file : string, optional
        Filename for keystream file
        Defaults to KEYSTREAM

    Returns
    -------
    None
        Decrypted file will be generated

    """
    with open(k_file, 'rb') as key_file:
        keystream = bytearray(key_file.read())
    with open(e_file, 'rb') as enc_file:
        encrypted_file = bytearray(enc_file.read())
    # extract first N_BYTES block from keystream
    keystream = keystream[:N_BYTES]
    output = bytearray()
    for cursor in range(0, len(encrypted_file), N_BYTES):
        # decode N_BYTES of encrypted file
        decode = xor(encrypted_file[cursor:cursor+N_BYTES], keystream)
        output.extend(decode)
        # iteratively generate next N_BYTES block of keystream
        keystream = next_keystream(keystream)
    with open(o_file, 'wb') as output_file:
        output_file.write(output)

def get_keystream(e_file=RULE_86_ENC, d_file=RULE_86, o_file=KEYSTREAM):
    """Bitwise XOR the encrypted file to the decrypted file to obtain
    keystream.

    Parameters
    ----------
    e_file : string, optional
        Filename for encrypted file
        Defaults to RULE_86_ENC
    d_file : string, optional
        Filename for decrypted file
        Defaults to RULE_86
    o_file : string, optional
        Filename for output file containing keystream
        Defaults to KEYSTREAM

    Returns
    -------
    None
        Keystream file will be generated

    """
    with open(e_file, "rb") as enc_file:
        encrypted_file = bytearray(enc_file.read())
    with open(d_file, "rb") as dec_file:
        decrypted_file = bytearray(dec_file.read())
    output = xor(encrypted_file, decrypted_file)
    with open(o_file, 'wb') as output_file:
        output_file.write(output)

def main():
    print("Obtaining keystream...")
    get_keystream()
    print(f"Keystream saved as '{KEYSTREAM}'")
    print(f"Decrypting {SUPER_CIPHER_ENC}...")
    decrypt(SUPER_CIPHER_ENC, SUPER_CIPER)
    print(f"'{SUPER_CIPHER_ENC}' saved as '{SUPER_CIPER}'")
    print(f"Decrypting {HINT_GIF_ENC}...")
    decrypt(HINT_GIF_ENC, HINT_GIF)
    print(f"'{HINT_GIF_ENC}' saved as '{HINT_GIF}'")
    print("Recovering seed value...")
    print(f"Seed value: {get_seed()}")

if __name__ == '__main__':
    main()
