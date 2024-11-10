"""Regresion tests designed to ensure that end to end Bitcoin blockchain parsing capabilities work
as expected. For more details, see BitcoinGraph white paper"""
import os
import json
from functools import reduce
import unittest
from BlockchainParser.models.BlockchainParser import BlockchainParser


class BlockchainParserTest(unittest.TestCase):
    """Unit test class for Blockchain parsing regression test cases"""

    def test_initial_block_file(self):
        blockchain_parser = BlockchainParser(
            f"{os.getcwd()}/BlockchainParser/tests/blocks", 0, 0)

        blockchain_contents = blockchain_parser.parse_blk_file(0)
        self.assertIsNotNone(blockchain_contents)

    def test_segwit_block_file(self):
        blockchain_parser = BlockchainParser(
            f"{os.getcwd()}/BlockchainParser/tests/blocks", 1, 1)

        blockchain_contents = blockchain_parser.parse_blk_file(1000)
        self.assertIsNotNone(blockchain_contents)

    def test_mempool(self):
        blockchain_parser = BlockchainParser(
            f"{os.getcwd()}/BlockchainParser/tests/blocks", 0, 0, include_mempool=True)

        mempool = blockchain_parser.parse_mempool()
        self.assertIsNotNone(mempool)

    def test_all(self):
        blockchain_parser = BlockchainParser(
            f"{os.getcwd()}/BlockchainParser/tests/blocks", 0, 0, include_mempool=True)
        blockchain_contents = []
        expected_output = {}
        with open(f"{os.getcwd()}/BlockchainParser/tests/regression/expected_output.json", "r") as file:
            expected_output = json.load(file)
        for i in range(0, 4301, 100):
            block_content = blockchain_parser.parse_blk_file(i)
            blockchain_contents.append(block_content)
            if len(block_content) > 0:
                self.assertEqual(
                    expected_output[str(i)]['block_count'], len(block_content))
                self.assertEqual(expected_output[str(i)]['transaction_count'], sum(
                    [block['transaction count'] for block in block_content]))

                tx_id_list = reduce(
                    lambda x, y: x+y, [block['transaction id list'] for block in block_content])

                for tx_id in expected_output[str(i)]['transaction_ids']:
                    self.assertIn(tx_id, tx_id_list)
