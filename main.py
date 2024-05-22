from datetime import datetime 
from block_util import *
from Block import Block
import pandas as pd

block_number = 0xFF
dataset_dir = f"/mnt/raid1_ssd_4tb/datasets/bitcoin/bitcoin-25.0/.bitcoin/blocks"
parsed_output_dir = f"parsed_blocks/"

txid_list = []

for i in range(1):
    file_number = "{:05}".format(i)
    filename = f"{dataset_dir}/blk{file_number}.dat"
    current_block_objects = []
    start_time = datetime.now() 
    with open(filename, 'rb') as blockchain:
        print(f"Parsing blockchain head at file {filename.split('blocks/')[1]}")
        continue_parsing = True
        counter = 0
        while continue_parsing:
            block = Block(blockchain)
            continue_parsing = block.continue_parsing
            if continue_parsing:
                # block.to_string()
                current_block_objects.append(block.get_object())
            counter += 1
            print(f"{'#'*20} Block counter number: {counter} {'#'*20}")
            if counter >= block_number and block_number != 0xFF:
                continue_parsing = False
        print(f"End of file")
        print(f"Parsed {counter} blocks")
    end_time = datetime.now()
    print(f"Function execute took {end_time - start_time} seconds")
    