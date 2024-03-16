import struct
import base58
import hashlib
import subprocess
import json

def uint1(stream):
    return ord(stream.read(1))

def uint2(stream):
    return struct.unpack('H', stream.read(2))[0]

def uint4(stream):
    return struct.unpack('I', stream.read(4))[0]

def uint8(stream):
    return struct.unpack('Q', stream.read(8))[0]

def hash32(stream):
    return stream.read(32)[::-1]

def time(stream):
    time = uint4(stream)
    return time

def varint(stream):
    size = uint1(stream)

    if size < 0xfd:
        return size
    if size == 0xfd:
        return uint2(stream)
    if size == 0xfe:
        return uint4(stream)
    if size == 0xff:
        return uint8(stream)
    return -1

def hash_string(byte_buffer):
    try:
        return "".join('{:02x}'.format(b) for b in byte_buffer)
    except:
        pass

def pubkey_to_address(hex_string):
    sha = hashlib.sha256()
    rip = hashlib.new('ripemd160')
    sha.update(bytearray.fromhex(hex_string))
    rip.update( sha.digest())
    return hash_to_address(f"00{rip.hexdigest()}")

def hash_to_address(key_hash):
    sha = hashlib.sha256()
    sha.update(bytearray.fromhex(key_hash))
    checksum = sha.digest()
    sha = hashlib.sha256()
    sha.update(checksum)
    checksum = sha.hexdigest()[0:8]

    return base58.b58encode( bytes(bytearray.fromhex(key_hash + checksum)) ).decode('utf-8')

def decode_script(hex_string):
    DATADIR = "/mnt/raid1_ssd_4tb/datasets/bitcoin/bitcoin-25.0/.bitcoin/"
    result = subprocess.run(["bitcoin-cli", f"-datadir={DATADIR}", "decodescript", hex_string], capture_output=True)
    return json.loads(result.stdout)