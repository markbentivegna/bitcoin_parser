import sys
from block_util import *
from Block import Block
from BlockHeader import BlockHeader

block_number = 0xFF
filename = "blk00012.dat"

with open(filename, 'rb') as blockchain:
    print(f"Parsing blockchain head")
    continue_parsing = True
    counter = 0
    # blockchain.seek(0,2)
    while continue_parsing:
        block = Block(blockchain)
        continue_parsing = block.continue_parsing
        if continue_parsing:
            block.to_string()
        counter += 1
        print(f"{'#'*20} Block counter number: {counter} {'#'*20}")
        if counter >= block_number and block_number != 0xFF:
            continue_parsing = False

    print(f"End of file")
    print(f"Parsed {counter} blocks")