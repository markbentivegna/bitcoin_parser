from block_util import *
from opcodes import *

class TransactionInput:
	def __init__(self, blockchain):
		self.prev_hash = hash32(blockchain)
		self.tx_out_id = uint4(blockchain)
		self.script_length = varint(blockchain)
		self.script_sig = blockchain.read(self.script_length)
		self.seq_no = uint4(blockchain)
	
	def get_object(self):
		return {
			"prev hash": hash_string(self.prev_hash),
			"tx out index": self.decode_out_idx(self.tx_out_id),
			"script length": self.script_length,
			"script": self.script,
			"pubkey": self.pubkey,
			"sequence": self.seq_no,
			"address": self.address,
			"transaction_type": self.transaction_type
		}

	def to_string(self):
		print(f"\tTx Out Index:\t {self.decode_out_idx(self.tx_out_id)}")
		print(f"\tScript Length:\t {self.script_length}")
		self.decode_script_sig(self.script_sig)
		print(f"\tSequence:\t {self.seq_no}")
	
	def decode_script_sig(self,data):
		hex_string = hash_string(data)
		if 0xffffffff == self.tx_out_id:
			self.script = None
			self.pubkey = None
			self.address = None
			self.transaction_type = 'nonstandard'
			return hex_string
		script_length = int(hex_string[0:2],16)
		script_length *= 2
		self.script = hex_string[2:2+script_length] 
		print(f"\tScript:\t\t {self.script}")
		try:
			decoded_script = decode_script(hex_string)
			self.transaction_type = decoded_script['segwit']['type']
			print(f"\tTranaction Type: {self.transaction_type}")
			self.address = decoded_script['segwit']['address']
			print(f"\tAddress:\t {self.address}")
			if SIGHASH_ALL != int(hex_string[script_length:script_length+2],16):
				print(f"\t Script op_code is not SIGHASH_ALL")
				self.pubkey = None
				return hex_string
			else: 
				self.pubkey = hex_string[2+script_length+2:2+script_length+2+66]
				print(f"\tInPubkey:\t {self.pubkey}")
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