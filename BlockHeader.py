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

    def get_object(self):
        return {
            "version": self.version,
            "previous hash": hash_string(self.previous_hash),
            "merkle root": hash_string(self.merkle_hash),
            "timestamp": self.decode_time(self.time),
            "difficulty": self.bits,
            "nonce": self.nonce
        }

    def to_string(self):
        print(f"Version:\t {self.version}")
        print(f"Previous Hash:\t {hash_string(self.previous_hash)}")
        print(f"Merkle Root\t: {hash_string(self.merkle_hash)}")
        print(f"Timestamp:\t {self.decode_time(self.time)}")
        print(f"Difficulty:\t {self.bits}")
        print(f"Nonce:\t\t {self.nonce}")

    def decode_time(self, time):
        utc_time = datetime.fromtimestamp(time)
        return utc_time.strftime("%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)")