from block_util import *
from Transaction import Transaction
from BlockHeader import BlockHeader

class Block:
    def __init__(self, blockchain):
        self.continue_parsing = True
        self.magic_number = 0
        self.block_size = 0
        self.block_header = ""
        self.tx_count = 0
        self.tx_list = []

        if self.has_length(blockchain, 8):
            self.magic_number = uint4(blockchain)
            self.block_size = uint4(blockchain)
        else:
            self.continue_parsing = False
            return
        
        if self.has_length(blockchain, self.block_size):
            self.set_header(blockchain)
            self.tx_count = varint(blockchain)
            self.tx_list = []

            for i in range(self.tx_count):
                tx = Transaction(blockchain)
                tx.sequence = i
                self.tx_list.append(tx)
        else:
            self.continue_parsing = False

    def continue_parsing(self):
        return self.continue_parsing
    
    def get_block_size(self):
        return self.block_size
    
    def has_length(self, blockchain, size):
        current_position = blockchain.tell()
        blockchain.seek(0,2)

        file_size = blockchain.tell()
        blockchain.seek(current_position)

        temp_block_size = file_size - current_position
        print(f"temp_block_size:\t {temp_block_size}")
        if temp_block_size < size:
            return False
        return True
    
    def set_header(self, blockchain):
        self.block_header = BlockHeader(blockchain)

    def get_object_dict(self):
        return {
            "magic number": self.magic_number,
            "block size": self.block_size,
            "block header": self.block_header.get_object_dict(),
            "transaction count": self.tx_count,
            "transaction list": [tx.get_object_dict() for tx in self.tx_list]
        }


    def to_string(self):
        print(f"")
        print(f"Magic Number:\t {self.magic_number}")
        print(f"Block Size:\t {self.block_size}")
        print(f"")
        print(f"{'#'*10} Block Header {'#'*10}")
        print(f"{self.block_header.to_string()}")
        print(f"{'#' * 5} Tx count: {self.tx_count}")
        for tx in self.tx_list:
            print(f"{tx.to_string()}")
        print(f"{'#' * 5} end of all transactions: {self.tx_count}")