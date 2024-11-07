import sys
import os
sys.path.append(f"{os.getcwd()}")
from models.BlockchainParser import BlockchainParser
import os
# from BlockchainParser import BlockchainParser


def test_initial_block_file():
    blockchain_parser = BlockchainParser(f"{os.getcwd()}/test/blocks", 0, 0)

    blockchain_contents = blockchain_parser.parse_blk_file(0)
    assert blockchain_contents != None
    # assert len(blockchain_contents) == 100

def test_segwit_block_file():
    blockchain_parser = BlockchainParser(f"{os.getcwd()}/test/blocks", 1, 1)

    blockchain_contents = blockchain_parser.parse_blk_file(1000)
    assert blockchain_contents != None

def test_mempool():
    blockchain_parser = BlockchainParser(f"{os.getcwd()}/test/blocks", 0, 0, include_mempool=True)

    mempool = blockchain_parser.parse_mempool()
    assert mempool != None

def test_all():
    blockchain_parser = BlockchainParser(f"{os.getcwd()}/test/blocks", 0, 0, include_mempool=True)
    blockchain_contents = []
    for i in range(0, 4301, 100):
        blockchain_contents.append(blockchain_parser.parse_blk_file(i))
    assert blockchain_contents != None

test_initial_block_file()
test_segwit_block_file()
test_mempool()
test_all()