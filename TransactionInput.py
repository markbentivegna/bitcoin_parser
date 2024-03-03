from block_util import *
from opcodes import *

class TransactionInput:
	def __init__(self, blockchain):
		self.prev_hash = hash32(blockchain)
		self.tx_out_id = uint4(blockchain)
		self.script_length = varint(blockchain)
		self.script_sig = blockchain.read(self.script_length)
		self.seq_no = uint4(blockchain)
	
	def to_string(self):
		print(f"\tTx Out Index:\t {self.decode_out_idx(self.tx_out_id)}")
		print(f"\tScript Length:\t {self.script_length}")
		self.decode_sript_sig(self.script_sig)
		print(f"\tSequence:\t {self.seq_no}")
	
	def decode_sript_sig(self,data):
		hex_string = hash_string(data)
		if 0xffffffff == self.tx_out_id:
			return hex_string
		script_length = int(hex_string[0:2],16)
		script_length *= 2
		script = hex_string[2:2+script_length] 
		print(f"\tScript:\t\t {script}")
		try:
			if SIGHASH_ALL != int(hex_string[script_length:script_length+2],16):
				print(f"\t Script op_code is not SIGHASH_ALL")
				return hex_string
			else: 
				pubkey = hex_string[2+script_length+2:2+script_length+2+66]
				print(f"\tInPubkey:\t {pubkey}")
		except:
			return hex_string
			
	def decode_out_idx(self,idx):
		s = ""
		if(idx == 0xffffffff):
			s = " Coinbase with special index"
			print(f"\tCoinbase Text:\t {hash_string(self.prev_hash)}")
		else: 
			print(f"\tPrev. Tx Hash:\t {hash_string(self.prev_hash)}")
		return "%8x"%idx + s 