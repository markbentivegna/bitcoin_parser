from datetime import datetime 
from utils.block_util import *
from models.Block import Block, Transaction
from joblib import Parallel, delayed
import pandas as pd
from pymongo import MongoClient

def parse_blk_file(i):
    block_number = 0xFF
    dataset_dir = f"/mnt/raid10/bitcoin_blocks"
    # parsed_output_dir = f"parsed_blocks/"

    # txid_list = []
    client = MongoClient('localhost', 27017)
    file_number = "{:05}".format(i)
    # filename = f"{dataset_dir}/blk{file_number}.dat"
    filename = f"{dataset_dir}/mempool.dat"
    # output_file = f"output/custom_txids{i}.csv"
    # input_file = f"output/inputs/custom_txids{i}.csv"
    # if not os.path.isfile(output_file):
    if True:
        current_block_objects = []
        start_time = datetime.now()
        try:
            with open(filename, 'rb') as blockchain:
                print(f"Parsing blockchain head at file {filename.split('blocks/')[1]}")
                continue_parsing = True
                counter = 0
                
                #TEST SECTION FOR MEMPOOL PARSING
                while continue_parsing:
                    version = uint8(blockchain)
                    transaction_count = uint8(blockchain)
                    transaction_list = []
                    for i in range(transaction_count):
                        tx = Transaction(blockchain)
                        entry_time = uint8(blockchain)
                        fee = uint8(blockchain)
                        transaction_list.append({
                            "transaction": tx,
                            "entry_time": entry_time,
                            "fee": fee
                        })
                        if i % 5000 == 0:
                            print(f'Parsing transaction: {i}')
                    print(f"version: {version}, transaction_count: {transaction_count}")
                    continue_parsing = False
                print("completed parsing mempool.dat???")
                while continue_parsing:
                    block = Block(blockchain)
                    continue_parsing = block.continue_parsing
                    if continue_parsing:
                        current_block_objects.append(block.get_object_dict())
                    counter += 1
                    # if counter % 1000 == 0:
                    #     print(f"{'#'*20} Block counter number: {counter} - parsed {sum([len(block['transaction list']) for block in current_block_objects])} transactions {'#'*20}")
                    if counter >= block_number and block_number != 0xFF:
                        continue_parsing = False
                print(f"End of file")
                print(f"Parsed {counter} blocks")
        except Exception as e:
            print(e)
            print(f"Error at file {filename}")
            pass
        print(f"{'#'*20} Parsed {sum([len(block['transaction list']) for block in current_block_objects])} transactions {'#'*20}")
        end_time = datetime.now()
        print(f"Function execute took {end_time - start_time} seconds to parse transactions for file {filename}")
        tx_lists = [block['transaction list'] for block in current_block_objects]
        start_time = datetime.now()
        for tx_list in tx_lists:
            try:
                for elem in tx_list:
                    print(elem)
                    # client['graphlab']['bitcoin'].replace_one({'_id': elem['txid']}, replacement={'_id' if k == 'txid' else k:v for k,v in elem.items()}, upsert=True)
            except Exception as e:
                print(e)
                print(f"error at file {filename}")
                pass
      
        # block_list = [{k: v for k, v in d.items() if k != 'transaction list'} for d in current_block_objects]
        
        # try:
        #     client["graphlab"]["bitcoin_test"].update_many(block_list,ordered=False, upsert=True, bypass_document_validation=True)
        # except:
        #     pass
        # transaction_list = block['transaction_list']
        # for block in current_block_objects:
        #     for tx in block['transaction list']:
        #         try:
        #             client["graphlab"]["bitcoin_test"].insert_many(block['transaction list'])
        #         except:
        #             pass
        end_time = datetime.now()
        print(f"Function execute took {end_time - start_time} seconds to write transactions to DB for file {filename}")
            # for input in tx['inputs']:
            #         input_list.append((tx['txid'], input['prev hash'], input['tx out index']))
        #         for output in tx['outputs']:
        #             txid_list.append((tx['txid'], output['address']))
        # pd.DataFrame(txid_list, columns=['txid', 'address']).to_csv(output_file)
        # pd.DataFrame(input_list, columns=['txid', 'prev_hash', 'tx_out_index']).to_csv(input_file)

# Parallel(JOBS, prefer='processes')(
#     delayed(parse_blk_file)(i) for i in range(2000, 4400)
# )
# for i in range(1):
#     parse_blk_file(i)
parse_blk_file(0)