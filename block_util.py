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

def encode_uint2(value):
    return struct.pack('H', value)

def encode_uint4(value):
    return struct.pack('I', value)

def encode_uint8(value):
    return struct.pack('Q', value)

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

def compact_size(value):
    if value <= 252:
        return hash_string(struct.pack('B', value))
    if value > 252 and value <= 65535:
        return f"fd{hash_string(encode_uint2(value))}"
    if value > 65535 and value <= 4294967295:
        return f"fe{hash_string(encode_uint4(value))}"
    else:
        return f"ff{hash_string(encode_uint8(value))}"

def str_to_little_endian(value):
    big = bytearray(value)
    big.reverse()
    return ''.join(f"{n:02X}" for n in big).lower()

def hash_string(byte_buffer):
    return "".join('{:02x}'.format(b) for b in byte_buffer)
    
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

# def decode_script(hex_string):
#     DATADIR = "/mnt/raid1_ssd_4tb/datasets/bitcoin/bitcoin-25.0/.bitcoin/"
#     result = subprocess.run(["bitcoin-cli", f"-datadir={DATADIR}", "decodescript", hex_string], capture_output=True)
#     return json.loads(result.stdout)

def raw_bytes_to_id(byte_buffer):
    sha = hashlib.sha256()
    sha.update(bytearray.fromhex(byte_buffer))
    checksum = sha.digest()
    sha = hashlib.sha256()
    sha.update(checksum)
    return hash_string(bytearray.fromhex(sha.hexdigest())[::-1])