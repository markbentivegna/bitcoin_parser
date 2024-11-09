import argparse
from models.BlockchainParser import BlockchainParser

parser = argparse.ArgumentParser(
    prog='BitcoinParser',
    description='The most comprehensive open-sourced Python solution for parsing the Bitcoin blockchain'
)

parser.add_argument('blockchain_dir', help='Root directory of the blockchain')
parser.add_argument('blk_file_start', help='Starting raw data block file')
parser.add_argument('blk_file_end', help='Ending raw data block file')
parser.add_argument('-m', '--include_mempool',
                    help='Flag to include pre-validated transactions. Default value is False')
parser.add_argument('-n', '--num_workers',
                    help='Number of parallel workers ot parse the blockchain. Defualt value is 16')
args = parser.parse_args()

blockchain_dir = args.blockchain_dir
blk_file_start = args.blk_file_start
blk_file_end = args.blk_file_end
include_mempool = args.include_mempool
num_workers = args.num_workers

blockchain_parser = BlockchainParser(
    blockchain_dir, blk_file_start, blk_file_end, include_mempool, num_workers)
blockchain_parser.parse_blockchain()
