from block_util import *
from opcodes import *

class TransactionWitness:
    def __init__(self, blockchain):
        self.stack_count = varint(blockchain)
        self.script_lengths, self.items = [], []
        for _ in range(self.stack_count):
            script_length = varint(blockchain)
            stack_data = blockchain.read(script_length)
            self.script_lengths.append(script_length)
            self.items.append(stack_data)

    def to_string(self):
        print(f"\Stack Count:\t {self.stack_count}")
        for i in range(self.stack_count):
            print(f"\tScript Length:\t {self.script_lengths[i]}")
            print(f"\tStack Item:\t {self.items[i]}")

    def get_object_dict(self):
        return {
            "stack_count": self.stack_count,
			"script_lengths": self.script_lengths,
			"stack_items": self.items
		}
    
    
    def get_bytes_string(self):
        bytes_string = compact_size(self.stack_count)
        for i in range(self.stack_count):
            bytes_string += compact_size(self.script_lengths[i])
            bytes_string += hash_string(self.items[i])
        return bytes_string
