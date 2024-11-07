from block_util import *
from opcodes import *

class TransactionInput:
	def __init__(self, blockchain):
		self.prev_hash = hash32(blockchain)
		self.tx_out_id = uint4(blockchain)
		self.script_length = varint(blockchain)
		self.script_sig = blockchain.read(self.script_length)
		self.seq_no = uint4(blockchain)
		self.script_sig_deciphered = decipher_script(self.script_sig)

	def get_bytes_string(self):
		return str_to_little_endian(self.prev_hash) + hash_string(encode_uint4(self.tx_out_id)) + compact_size(self.script_length) + hash_string(self.script_sig) + hash_string(encode_uint4(self.seq_no))

	def get_object_dict(self):
		return {
			"prev hash": hash_string(self.prev_hash),
			"tx out index": hash_string(encode_uint4(self.tx_out_id)),
			"script length": self.script_length,
			"script signature": hash_string(self.script_sig),
			"script signature deciphered": self.script_sig_deciphered,
			"sequence": self.seq_no
		}