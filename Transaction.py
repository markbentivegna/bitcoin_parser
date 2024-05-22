from block_util import *
from TransactionInput import TransactionInput
from TransactionOutput import TransactionOutput

class Transaction:
	def __init__(self, blockchain):
		self.version = uint4(blockchain)
		self.input_count = varint(blockchain)
		self.inputs, self.outputs = [], []
		self.sequence = 1
		for _ in range(self.input_count):
			self.inputs.append(TransactionInput(blockchain))
		self.output_count = varint(blockchain)
		if self.output_count > 0:
			for _ in range(self.output_count):
				self.outputs.append(TransactionOutput(blockchain))	
		self.lock_time = uint4(blockchain)
		self.txid = transaction_bytes_to_txid(self.get_bytes_string())

	def get_bytes_string(self):
		return self.get_hex_formatted_string(self.version) \
			+ compact_size(self.input_count) \
			+ self.get_inputs_bytes_string() \
			+ compact_size(self.output_count) \
			+ self.get_outputs_bytes_string() \
			+ self.get_hex_formatted_string(self.lock_time)

	def get_inputs_bytes_string(self):
		return ''.join([input.get_bytes_string() for input in self.inputs])
	
	def get_outputs_bytes_string(self):
		return ''.join([output.get_bytes_string() for output in self.outputs])

	def get_hex_formatted_string(self, value):
		return '{:02x}'.format(value) + '0' * 6

	def get_object_dict(self):
		return {
			"txid": self.txid,
			"version": self.version,
			"sequence": self.sequence,
			"input count": self.input_count,
			"inputs": [tx.get_object_dict() for tx in self.inputs],
			"output count": self.output_count,
			"outputs": [tx.get_object_dict() for tx in self.outputs],
			"lock time": self.lock_time
		}
	
	def to_string(self):
		print(f"")
		print(f"{'='*20}  No. {self.sequence} Transaction {'='*20}")
		print(f"Tx Version:\t {self.version}")
		print(f"Inputs:\t\t {self.input_count}")
		for input in self.inputs:
			print(f"{input.to_string()}")

		print(f"Outputs:\t {self.output_count}")
		for output in self.outputs:
			print(f"{output.to_string()}")
		print(f"Lock Time:\t {self.lock_time}")