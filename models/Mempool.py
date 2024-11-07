from block_util import *
from models.Transaction import Transaction

class Mempool:
    def __init__(self, blockchain):
        self.version = uint8(blockchain)
        self.transaction_count = uint8(blockchain)
        self.transaction_list = []
        for _ in range(self.transaction_count):
            transaction = Transaction(blockchain)
            entry_time = uint8(blockchain)
            fee = uint8(blockchain)
            self.transaction_list.append({
                "transaction": transaction,
                "entry_time": entry_time,
                "fee": fee
            })

    def get_object_dict(self):
        return {
            "version": self.version,
            "object": "MEMPOOL",
            "transaction count": self.transaction_count,
            "transaction list": [tx.get_object_dict() for tx in self.transaction_list],
            "transaction id list": [tx.txid for tx in self.transaction_list]
        }