"""Unit tests designed to ensure that Bitcoin blockchain parsing helper methods work
as expected. For more details, see BitcoinGraph white paper"""
import unittest
from BlockchainParser.utils import block_util


class BlockUtilityTest(unittest.TestCase):
    """Unit test class for Blockchain helper methods test cases"""

    def test_encode_uint2(self):
        self.assertEqual(b'\x02\x00', block_util.encode_uint2(2))

    def test_encode_uint4(self):
        self.assertEqual(b'\x04\x00\x00\x00', block_util.encode_uint4(4))

    def test_encode_uint8(self):
        self.assertEqual(b'\x08\x00\x00\x00\x00\x00\x00\x00',
                         block_util.encode_uint8(8))

    def test_compact_size(self):
        self.assertEqual('ff00e40b5402000000',
                         block_util.compact_size(10000000000))

    def test_str_to_little_endian(self):
        self.assertEqual('0000000000000000000000000000000000000000000000000000000000000000',
                         block_util.str_to_little_endian(
                             b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))

    def test_hash_string(self):
        self.assertEqual('04ffff001d0104', block_util.hash_string(
            b'\x04\xff\xff\x00\x1d\x01\x04'))

    def test_pubkey_to_address(self):
        self.assertEqual('1HLoD9E4SDFFPDiYfNYnkBLQ85Y51J3Zb1', block_util.pubkey_to_address(
            ("047211a824f55b505228e4c3d5194c1fcfaa15a456abdf37f9b9d97a4040afc073dee6c89064984f0"
             "3385237d92167c13e236446b417ab79a0fcae412ae3316b77")
        ))

    def test_hash_to_address(self):
        self.assertEqual('12higDjoCCNXSA95xZMWUdPvXNmkAduhWv', block_util.hash_to_address(
            '0012ab8dc588ca9d5787dde7eb29569da63c3a238c'))

    def test_segwit_hash_to_address(self):
        self.assertEqual('bc1qpkuy609cpcl7dpvrgkpavgtdqumtcynxp33z0h',
                         block_util.segwit_hash_to_address(
                             "00140db84d3cb80e3fe685834583d6216d0736bc1266"))

    def test_decipher_script(self):
        self.assertEqual(['OP_DUP',
                          'OP_HASH160',
                          'OP_PUSHBYTES_20',
                          '5d1741144b8d677286b8ebe09c6b41e0f63fb9fc',
                          'OP_EQUALVERIFY',
                          'OP_CHECKSIG'],
                         block_util.decipher_script(
                             b'v\xa9\x14]\x17A\x14K\x8dgr\x86\xb8\xeb\xe0\x9ckA\xe0\xf6?\xb9\xfc\x88\xac'
        )
        )

    def test_raw_bytes_to_id(self):
        self.assertEqual(
            '00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048',
            block_util.raw_bytes_to_id(
                ("010000006fe28c0ab6f1b372c1a6a246ae63f74f931e8365e15a089c68d6190000000000982051fd"
                 "1e4ba744bbbe680e1fee14677ba1a3c3540bf7b1cdb606e857233e0e61bc6649ffff001d01e36299"
                 )))

    def test_is_op_return(self):
        self.assertEqual(block_util.is_op_return(
            ['OP_RETURN',
             'OP_PUSHBYTES_32',
             '83288860ff7267946aa81c1aa21db814c0587f0b09fd0807ef66305510bef714']), True)

    def test_is_p2ms(self):
        self.assertEqual(block_util.is_p2ms([
            'OP_2', 'OP_PUSHBYTES_65', '04d81fd572', 'OP_PUSHBYTES_65', '04ec3afff0b2b66',
            'OP_PUSHBYTES_65', '04b49b496684b02', 'OP_3', 'OP_CHECKMULTISIG']), True)

    def test_is_p2pk(self):
        self.assertEqual(block_util.is_p2pk(
            ['OP_PUSHBYTES_33',
             '02f6e69173d7be51c47a1ac699d180745bb1d4255d673b3fa9a9f76d35bde8940f',
             'OP_CHECKSIG']), True)

    def test_is_p2sh(self):
        self.assertEqual(block_util.is_p2sh(
            ['OP_HASH160', 'OP_PUSHBYTES_20',
             'cb93febf21c9652a640b8a10820bb7f0f6274fda', 'OP_EQUAL']), True)

    def test_is_p2pkh(self):
        self.assertEqual(block_util.is_p2pkh(['OP_DUP', 'OP_HASH160', 'OP_PUSHBYTES_20',
                         '10bb6624778ed90d8604b9aad7d9f31027a95fee', 'OP_EQUALVERIFY',
                                              'OP_CHECKSIG']), True)

    def test_is_p2wsh(self):
        self.assertEqual(block_util.is_p2wsh(
            ['OP_0', 'OP_PUSHBYTES_32',
             '7250d91085a77a4568fa4cfd5bebb59f0b9cb3530f8154cd4fab6d28abd548fe']), True)

    def test_is_p2wpkh(self):
        self.assertEqual(block_util.is_p2wpkh(
            ['OP_0', 'OP_PUSHBYTES_20', '0db84d3cb80e3fe685834583d6216d0736bc1266']), True)
