from block_util import *
from TransactionInput import TransactionInput
from TransactionOutput import TransactionOutput

class Transaction:
	def __init__(self, blockchain):
		self.version = uint4(blockchain)
		self.input_count = varint(blockchain)
		self.inputs = []
		self.sequence = 1
		for _ in range(self.input_count):
			input = TransactionInput(blockchain)
			self.inputs.append(input)
		self.outCount = varint(blockchain)
		self.outputs = []
		if self.outCount > 0:
			for i in range(0, self.outCount):
				output = TransactionOutput(blockchain)
				self.outputs.append(output)	
		self.lockTime = uint4(blockchain)

	def get_object(self):
		return {
			"version": self.version,
			"sequence": self.sequence,
			"input count": self.input_count,
			"inputs": [tx.get_object() for tx in self.inputs],
			"output count": self.outCount,
			"outputs": [tx.get_object() for tx in self.outputs],
			"lock time": self.lockTime
		}
	
	def to_string(self):
		print(f"")
		print(f"{'='*20}  No. {self.sequence} Transaction {'='*20}")
		print(f"Tx Version:\t {self.version}")
		print(f"Inputs:\t\t {self.input_count}")
		for input in self.inputs:
			print(f"{input.to_string()}")

		print(f"Outputs:\t {self.outCount}")
		for output in self.outputs:
			print(f"{output.to_string()}")
		print(f"Lock Time:\t {self.lockTime}")