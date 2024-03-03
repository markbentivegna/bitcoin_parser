from block_util import *
from opcodes import *

class TransactionOutput:
	def __init__(self, blockchain):
		self.value = uint8(blockchain)
		self.script_length = varint(blockchain)
		self.pubkey = blockchain.read(self.script_length)
		
	def to_string(self):
		print(f"\tValue:\t\t {self.value} Satoshi")
		print(f"\tScript Len:\t {self.script_length}")
		print(f"\tScriptPubkey:\t {self.decode_script_pubkey(self.pubkey)}")
		
	def decode_script_pubkey(self,data):	
		hex_string = hash_string(data)
		op_idx = int(hex_string[0:2],16)
		try: 
			op_code1 = OPCODE_NAMES[op_idx]
		except KeyError: #Obselete pay to pubkey directly 
			print(f" \tOP_CODE {op_idx} is probably obselete pay to address")
			# key_length = op_idx
			# op_codeTail = OPCODE_NAMES[int(hex_string[2+key_length*2:2+key_length*2+2],16)]
			# print(" \tPubkey OP_CODE:\t " "None " + "Bytes:%d " % key_length + "tail_op_code:" +  op_codeTail + " ")
			# print("\tPure Pubkey:\t   %s" % hex_string[2:2+key_length*2])
			return hex_string
		if op_code1 == "OP_DUP":  #P2PKHA pay to pubkey hash mode
	 		# op_code2 = OPCODE_NAMES[int(hex_string[2:4],16)]
			key_length = int(hex_string[4:6],16) 
			op_codeTail2nd = OPCODE_NAMES[int(hex_string[6+key_length*2:6+key_length*2+2],16)]
			op_codeTailLast = OPCODE_NAMES[int(hex_string[6+key_length*2+2:6+key_length*2+4],16)]
			print(" \tPubkey OP_CODE:\t " + op_code1 + " " + OPCODE_NAMES[int(hex_string[2:4],16)] + " " + "Bytes:%d " % key_length + "tail_op_code:" +  op_codeTail2nd + " " + op_codeTailLast)
			print("\tPubkeyHash:\t       %s" % hex_string[6:6+key_length*2])
			return hex_string
		elif op_code1 == "OP_HASH160": #P2SHA pay to script hash 
			key_length = int(hex_string[2:4],16) 
			op_code_tail = OPCODE_NAMES[int(hex_string[4+key_length*2:4+key_length*2+2],16)]
			print(" \tPubkey OP_CODE:\t " + op_code1 + "Bytes:%d " % key_length +\
					"tail_op_code:" +  op_code_tail + " ")
			print("\tPure Pubkey:\t     %s" % hex_string[4:4+key_length*2])
			return hex_string