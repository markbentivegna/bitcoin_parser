from datetime import datetime 
from block_util import *
from Block import Block
from joblib import Parallel, delayed
import pandas as pd
from pymongo import MongoClient
import itertools
import os

block_number = 0xFF
dataset_dir = f"/mnt/raid1_ssd_4tb/datasets/bitcoin/bitcoin-25.0/.bitcoin/blocks"
parsed_output_dir = f"parsed_blocks/"
JOBS = 16

txid_list = []
client = MongoClient('localhost', 27017)

def parse_blk_file(i):
    file_number = "{:05}".format(i)
    filename = f"{dataset_dir}/blk{file_number}.dat"
    output_file = f"output/custom_txids{i}.csv"
    # input_file = f"output/inputs/custom_txids{i}.csv"
    # if not os.path.isfile(output_file):
    if True:
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
                    current_block_objects.append(block.get_object_dict())
                counter += 1
                if counter % 1000 == 0:
                    print(f"{'#'*20} Block counter number: {counter} - parsed {sum([len(block['transaction list']) for block in current_block_objects])} transactions {'#'*20}")
                if counter >= block_number and block_number != 0xFF:
                    continue_parsing = False
            print(f"End of file")
            print(f"Parsed {counter} blocks")
        print(f"{'#'*20} Parsed {sum([len(block['transaction list']) for block in current_block_objects])} transactions {'#'*20}")
        end_time = datetime.now()
        print(f"Function execute took {end_time - start_time} seconds")
        tx_lists = [block['transaction list'] for block in current_block_objects]
        for tx_list in tx_lists:
            try:
                client['graphlab']['bitcoin'].insert_many([{'_id' if k == 'txid' else k:v for k,v in elem.items()} for elem in tx_list], ordered=False, bypass_document_validation=True)
            except:
                pass
        block_list = [{k: v for k, v in d.items() if k != 'transaction list'} for d in current_block_objects]
        
        try:
            client["graphlab"]["bitcoin"].insert_many(block_list,ordered=False, bypass_document_validation=True)
        except:
            pass
        # transaction_list = block['transaction_list']
        # for block in current_block_objects:
        #     for tx in block['transaction list']:
                # client["graphlab"]["bitcoin"].insert_many(block['transaction_list'])
            # for input in tx['inputs']:
            #         input_list.append((tx['txid'], input['prev hash'], input['tx out index']))
        #         for output in tx['outputs']:
        #             txid_list.append((tx['txid'], output['address']))
        # pd.DataFrame(txid_list, columns=['txid', 'address']).to_csv(output_file)
        # pd.DataFrame(input_list, columns=['txid', 'prev_hash', 'tx_out_index']).to_csv(input_file)

# Parallel(JOBS, prefer='processes')(
#     delayed(parse_blk_file)(i) for i in range(3750,4000)
# )
for i in range(100):
    parse_blk_file(i)