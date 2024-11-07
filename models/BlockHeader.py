from block_util import *
from datetime import datetime

class BlockHeader:
    def __init__(self, blockchain):
        self.version = uint4(blockchain)
        self.previous_hash = hash32(blockchain)
        self.merkle_hash = hash32(blockchain)
        self.time = uint4(blockchain)
        self.bits = uint4(blockchain)
        self.nonce = uint4(blockchain)

    def get_object_dict(self):
        return {
            "version": self.version,
            "previous hash": hash_string(self.previous_hash),
            "merkle root": hash_string(self.merkle_hash),
            "timestamp": self.decode_time(self.time),
            "difficulty": self.bits,
            "nonce": self.nonce
        }

    def decode_time(self, time):
        utc_time = datetime.fromtimestamp(time)
        return utc_time.strftime("%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)")
    
    def get_bytes_string(self):
        return hash_string(encode_uint4(self.version)) \
			+  hash_string(self.previous_hash[::-1]) \
            +  hash_string(self.merkle_hash[::-1]) \
            +  hash_string(encode_uint4(self.time)) \
            + hash_string(encode_uint4(self.bits)) \
            + hash_string(encode_uint4(self.nonce))