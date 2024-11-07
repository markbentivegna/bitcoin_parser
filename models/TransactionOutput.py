from block_util import *
from opcodes import *

class TransactionOutput:
	def __init__(self, blockchain):
		self.amount = uint8(blockchain)
		self.script_length = varint(blockchain)
		self.pubkey_script = blockchain.read(self.script_length)
		self.pubkey_script_deciphered = decipher_script(self.pubkey_script)
		self.decode_script()
		
	def get_bytes_string(self):
		return hash_string(encode_uint8(self.amount)) + compact_size(self.script_length) + hash_string(self.pubkey_script)

	def get_object_dict(self):
		return {
			"amount": self.amount,
			"script length": self.script_length,
			"script pubkey": hash_string(self.pubkey_script),
			"script pubkey deciphered": self.pubkey_script_deciphered,
			"pubkey": self.pubkey,
			"script type": self.script_type,
			"address": self.address
		}
	
	
	def decode_script(self):
		try:
			if is_p2pk(self.pubkey_script_deciphered):
				self.pubkey = self.pubkey_script_deciphered[1]
				self.address = pubkey_to_address(self.pubkey)
				self.script_type = "P2PK"
			elif is_p2pkh(self.pubkey_script_deciphered):
				self.pubkey = self.pubkey_script_deciphered[3]
				self.address = hash_to_address(f"00{self.pubkey}")
				self.script_type = "P2PKH"
			elif is_p2ms(self.pubkey_script_deciphered):
				#TODO: Add support for multisig public keys
				self.pubkey = None
				self.address = None
				self.script_type = "MULTISIG"
			elif is_p2sh(self.pubkey_script_deciphered):
				self.pubkey = self.pubkey_script_deciphered[2]
				self.address = hash_to_address(f"05{self.pubkey}")
				self.script_type = "P2SH"
			elif is_op_return(self.pubkey_script_deciphered):
				self.pubkey = self.pubkey_script_deciphered[2]
				self.address = None
				self.script_type = "OP_RETURN"
			elif is_p2wpkh(self.pubkey_script_deciphered):
				self.pubkey = self.pubkey_script_deciphered[2]
				self.address = segwit_hash_to_address(f"0014{self.pubkey}")
				self.script_type = "P2WPKH"
			elif is_p2wsh(self.pubkey_script_deciphered):
				self.pubkey = self.pubkey_script_deciphered[2]
				self.address = segwit_hash_to_address(f"0020{self.pubkey}")
				self.script_type = "P2WSH"
			else:
				self.pubkey = None
				self.address = None
				self.script_type = "NONSTANDARD"
		except:
			self.pubkey = None
			self.address = None
			self.script_type = "NONSTANDARD"