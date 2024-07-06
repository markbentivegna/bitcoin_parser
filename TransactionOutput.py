from block_util import *
from opcodes import *

class TransactionOutput:
	def __init__(self, blockchain):
		self.amount = uint8(blockchain)
		self.script_length = varint(blockchain)
		self.pubkey = blockchain.read(self.script_length)
		self.decode_script_pubkey(self.pubkey)
		
	def get_bytes_string(self):
		return hash_string(encode_uint8(self.amount)) + compact_size(self.script_length) + hash_string(self.pubkey)

	def get_object_dict(self):
		return {
			"amount": self.amount,
			"script length": self.script_length,
			"script pubkey": hash_string(self.pubkey),
			"transaction type": self.transaction_type,
			"address": self.address
		}
	
	def to_string(self):
		print(f"\tAmount:\t\t {self.amount} Satoshi")
		print(f"\tScript Len:\t {self.script_length}")
		print(f"\tScriptPubkey:\t {self.decode_script_pubkey(self.pubkey)}")
		
	def decode_script_pubkey(self,data):
		try:	
			hex_string = hash_string(data)
			op_idx = int(hex_string[0:2],16)
			if op_idx not in OPCODE_NAMES:
				op_idx = int(hex_string[-2:],16)
			self.op_code1 = OPCODE_NAMES[op_idx]
			if self.op_code1 == "OP_CHECKSIG":
				self.transaction_type = "PUBKEY"
				self.address = pubkey_to_address(hex_string[2:-2])
				return hex_string
			elif self.op_code1 == "OP_DUP":  #P2PKHA pay to pubkey hash mode
				self.transaction_type = "P2PKHA"
				key_length = int(hex_string[4:6],16) 
				self.address = hash_to_address(f"00{hex_string[6:6+key_length*2]}")
				return hex_string
			elif self.op_code1 == "OP_HASH160": #P2SHA pay to script hash 
				self.transaction_type = "P2SHA"
				key_length = int(hex_string[2:4],16) 
				self.address = hash_to_address(f"05{hex_string[4:4+key_length*2]}")
				return hex_string
			# elif self.op_code1 == "OP_0":
			# 	print('SEGWIT')
			else:
				self.transaction_type = 'NONSTANDARD'
				self.address = None
				return hex_string
		except:
			self.transaction_type = 'NONSTANDARD'
			self.address = None
			return ""