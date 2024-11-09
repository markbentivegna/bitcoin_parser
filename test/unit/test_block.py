import os
import sys
sys.path.append(f"{os.getcwd()}")
from models.BlockHeader import BlockHeader
from binascii import a2b_hex
from io import BytesIO
from utils.block_util import *
import unittest

class BlockTest(unittest.TestCase):
    def test_block_header(self):
        block_header_data = '01000000b715cee35e85ebf4ae9cfdf703ee359d76d87efd8ab0ba95a7040000000000009d4c13a700ce40a21e78f8307ee485ec57923a8749026723a6e67729470dacf129d6a44ff71e0b1a09edefe9'
        raw_bytes = a2b_hex(block_header_data)
        block_header = BlockHeader(BytesIO(raw_bytes))

        self.assertEqual(block_header.bits, 436936439)
        self.assertEqual(hash_string(block_header.merkle_hash), 'f1ac0d472977e6a623670249873a9257ec85e47e30f8781ea240ce00a7134c9d')
        self.assertEqual(block_header.nonce, 3924815113)
        self.assertEqual(hash_string(block_header.previous_hash), '00000000000004a795bab08afd7ed8769d35ee03f7fd9caef4eb855ee3ce15b7')
        self.assertEqual(block_header.time, 1336202793)
        self.assertEqual(block_header.version, 1)
        self.assertEqual(len(block_header.get_object_dict()), 6)
        self.assertEqual(block_header.decode_time(block_header.time), '2012-05-05 03:26:33.000000+00:00 (UTC)')
        self.assertEqual(block_header.get_bytes_string(), '01000000b715cee35e85ebf4ae9cfdf703ee359d76d87efd8ab0ba95a7040000000000009d4c13a700ce40a21e78f8307ee485ec57923a8749026723a6e67729470dacf129d6a44ff71e0b1a09edefe9')