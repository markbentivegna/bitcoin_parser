from block_util import *
from opcodes import *

class TransactionOutput:
	def __init__(self, blockchain):
		self.value = uint8(blockchain)
		self.script_length = varint(blockchain)
		self.pubkey = blockchain.read(self.script_length)
		
	def get_object(self):
		return {
			"value": self.value,
			"script length": self.script_length,
			"script pubkey": self.decode_script_pubkey(self.pubkey),
			"transaction type": self.transaction_type,
			"address": self.address,
			"hex string": hash_string(self.pubkey)
		}
	
	def to_string(self):
		print(f"\tValue:\t\t {self.value} Satoshi")
		print(f"\tScript Len:\t {self.script_length}")
		print(f"\tScriptPubkey:\t {self.decode_script_pubkey(self.pubkey)}")
		
	def decode_script_pubkey(self,data):	
		hex_string = hash_string(data)
		op_idx = int(hex_string[0:2],16)
		try: 
			self.op_code1 = OPCODE_NAMES[op_idx]
		except KeyError:
			try:
				op_idx = int(hex_string[-2:],16)
				self.op_code1 = OPCODE_NAMES[op_idx]
			except:
				return hex_string
		if self.op_code1 == "OP_CHECKSIG":
			self.transaction_type = "PUBKEY"
			print(f"\tOPCODE:\t {self.op_code1}")
			print(f"\tPubkey:\t {hex_string[2:-2]}")
			self.address = pubkey_to_address(hex_string[2:-2])
			print(f"\tAddress:\t {self.address}")
			return hex_string
		if self.op_code1 == "OP_DUP":  #P2PKHA pay to pubkey hash mode
			self.transaction_type = "P2PKHA"
			key_length = int(hex_string[4:6],16) 
			op_codeTail2nd = OPCODE_NAMES[int(hex_string[6+key_length*2:6+key_length*2+2],16)]
			op_codeTailLast = OPCODE_NAMES[int(hex_string[6+key_length*2+2:6+key_length*2+4],16)]
			print("\tPubkey OP_CODE:\t " + self.op_code1 + " " + OPCODE_NAMES[int(hex_string[2:4],16)] + " " + "Bytes:%d " % key_length + "tail_op_code:" +  op_codeTail2nd + " " + op_codeTailLast)
			print("\tPubkeyHash:\t       %s" % hex_string[6:6+key_length*2])
			self.address = hash_to_address(f"00{hex_string[6:6+key_length*2]}")
			print(f"\tAddress:\t {self.address}")
			return hex_string
		elif self.op_code1 == "OP_HASH160": #P2SHA pay to script hash 
			self.transaction_type = "P2SHA"
			key_length = int(hex_string[2:4],16) 
			op_code_tail = OPCODE_NAMES[int(hex_string[4+key_length*2:4+key_length*2+2],16)]
			print(" \tPubkey OP_CODE:\t " + self.op_code1 + "Bytes:%d " % key_length +\
					"tail_op_code:" +  op_code_tail + " ")
			print("\tPure Pubkey:\t     %s" % hex_string[4:4+key_length*2])
			self.address = hash_to_address(f"05{hex_string[4:4+key_length*2]}")
			print(f"\tAddress:\t {self.address}")
			return hex_string
		else:
			try:
				decoded_script = decode_script(hex_string)
				self.transaction_type = decoded_script['segwit']['type']
				print(f"\tTranaction Type: {self.transaction_type}")
				self.address = decoded_script['segwit']['address']
				print(f"\tAddress:\t {self.address}")
			except:
				self.address = None
				self.transaction_type = decoded_script["type"]
			return hex_string