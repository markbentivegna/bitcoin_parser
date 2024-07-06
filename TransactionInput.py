from block_util import *
from opcodes import *

class TransactionInput:
	def __init__(self, blockchain):
		self.prev_hash = hash32(blockchain)
		self.tx_out_id = uint4(blockchain)
		self.script_length = varint(blockchain)
		self.script_sig = blockchain.read(self.script_length)
		self.seq_no = uint4(blockchain)
		self.pubkey = None
		self.address = None
		self.decode_script_sig(self.script_sig)

	def get_bytes_string(self):
		return str_to_little_endian(self.prev_hash) + hash_string(encode_uint4(self.tx_out_id)) + compact_size(self.script_length) + hash_string(self.script_sig) + hash_string(encode_uint4(self.seq_no))

	def get_object_dict(self):
		return {
			"prev hash": hash_string(self.prev_hash),
			"tx out index": hash_string(encode_uint4(self.tx_out_id)),
			"script length": self.script_length,
			"script": self.script,
			"pubkey": self.pubkey,
			"sequence": self.seq_no,
			"address": self.address
		}

	def to_string(self):
		print(f"\tTx Out Index:\t {hash_string(encode_uint4(self.tx_out_id))}")
		print(f"\tScript Length:\t {self.script_length}")
		self.decode_script_sig(self.script_sig)
		print(f"\tSequence:\t {self.seq_no}")
	
	def decode_script_sig(self,data):
		hex_string = hash_string(data)
		if 0xffffffff == self.tx_out_id:
			self.script = None
			return hex_string
		try:
			script_length = int(hex_string[0:2],16)
		except:
			script_length = 0
		script_length *= 2
		self.script = hex_string[2:2+script_length] 
		try:
			if SIGHASH_ALL != int(hex_string[script_length:script_length+2],16):
				return hex_string
			else: 
				self.pubkey = hex_string[2+script_length+2:2+script_length+2+66]
		except:
			return hex_string
