"""Unit tests designed to ensure that Bitcoin transaction class and subclasses work
as expected. For more details, see BitcoinGraph white paper"""
from binascii import a2b_hex
from io import BytesIO
import unittest
from BlockchainParser.utils import block_util
from BlockchainParser.models.Transaction import Transaction
from BlockchainParser.models.TransactionInput import TransactionInput
from BlockchainParser.models.TransactionOutput import TransactionOutput
from BlockchainParser.models.TransactionWitness import TransactionWitness


class TransactionTest(unittest.TestCase):
    """Unit test class for transaction class and subclasses test cases"""

    def test_transaction(self):
        tx_data = ("01000000017dc9c2cca6aaf622939e28e14a428d21c7be5ef2893cf575e2735e2b3215497e01"
                   "0000006b483045022100f3d0d3f0c529c19362173db79b1824e33bcc3015d7f069b7ae244401"
                   "14e5039002207eb23d92ca2758b9f6a43b7cbd265fb34c56d60faedaf04d805b928a260422390"
                   "1210309e1b5495082f8aa6df37d8758379df33965596d028165ae8073b6219942febbffffffff"
                   "0120f40e00000000001976a914acf3cb08d55344b6178b37ae58f171c769413fa888ac00000000")
        raw_bytes = a2b_hex(tx_data)
        tx = Transaction(BytesIO(raw_bytes))

        self.assertEqual(tx.is_segwit, False)
        self.assertEqual(tx.lock_time, 0)
        self.assertEqual(tx.input_count, 1)
        self.assertEqual(tx.output_count, 1)
        self.assertEqual(tx.sequence, 1)
        self.assertEqual(
            tx.txid, '68af4c1132b8e115e98060d423bd00f3489650cc6c3698d0cb653d63c87548fb')
        self.assertEqual(tx.version, 1)
        self.assertEqual(tx.witnesses, [])
        self.assertEqual(tx.get_bytes_string(),
                         ("01000000017dc9c2cca6aaf622939e28e14a428d21c7be5ef2893cf575e2735e2b32154"
                          "97e010000006b483045022100f3d0d3f0c529c19362173db79b1824e33bcc3015d7f069"
                          "b7ae24440114e5039002207eb23d92ca2758b9f6a43b7cbd265fb34c56d60faedaf04d8"
                          "05b928a2604223901210309e1b5495082f8aa6df37d8758379df33965596d028165ae80"
                          "73b6219942febbffffffff0120f40e00000000001976a914acf3cb08d55344b6178b37a"
                          "e58f171c769413fa888ac00000000")
                         )
        self.assertEqual(tx.get_inputs_bytes_string(),
                         ("7dc9c2cca6aaf622939e28e14a428d21c7be5ef2893cf575e2735e2b3215497e0100000"
                          "06b483045022100f3d0d3f0c529c19362173db79b1824e33bcc3015d7f069b7ae244401"
                          "14e5039002207eb23d92ca2758b9f6a43b7cbd265fb34c56d60faedaf04d805b928a260"
                          "4223901210309e1b5495082f8aa6df37d8758379df33965596d028165ae8073b6219942"
                          "febbffffffff")
                         )
        self.assertEqual(tx.get_outputs_bytes_string(
        ), '20f40e00000000001976a914acf3cb08d55344b6178b37ae58f171c769413fa888ac')
        self.assertEqual(tx.get_witnesses_bytes_string(), '')
        self.assertEqual(len(tx.get_object_dict()), 10)

    def test_transaction_input(self):
        tx_input_data = ("9945a5a440f2d3712ff095cb1efefada1cc52e139defedb92a313daed49d5678010000"
                         "006a473044022031b6a6b79c666d5568a9ac7c116cacf277e11521aebc6794e2b415ef"
                         "8c87c899022001fe272499ea32e6e1f6e45eb656973fbb55252f7acc64e1e1ac70837d"
                         "5b7d9f0121023dec241e4851d1ec1513a48800552bae7be155c6542629636bcaa672ee"
                         "e971dcffffffff")
        raw_bytes = a2b_hex(tx_input_data)
        tx_input = TransactionInput(BytesIO(raw_bytes))

        self.assertEqual(block_util.hash_string(tx_input.prev_hash),
                         '78569dd4ae3d312ab9edef9d132ec51cdafafe1ecb95f02f71d3f240a4a54599')
        self.assertEqual(tx_input.tx_out_id, 1)
        self.assertEqual(tx_input.script_length, 106)
        self.assertEqual(block_util.hash_string(tx_input.script_sig),
                         ("473044022031b6a6b79c666d5568a9ac7c116cacf277e11521aebc6794e2b415ef8c87c"
                          "899022001fe272499ea32e6e1f6e45eb656973fbb55252f7acc64e1e1ac70837d5b7d9f"
                          "0121023dec241e4851d1ec1513a48800552bae7be155c6542629636bcaa672eee971dc"))
        self.assertEqual(tx_input.seq_no, 4294967295)
        self.assertEqual(tx_input.get_bytes_string(),
                         ("9945a5a440f2d3712ff095cb1efefada1cc52e139def"
                         "edb92a313daed49d5678010000006a473044022031b6a6b79c666d5568a9ac7c116cacf2"
                          "77e11521aebc6794e2b415ef8c87c899022001fe272499ea32e6e1f6e45eb656973fbb5"
                          "5252f7acc64e1e1ac70837d5b7d9f0121023dec241e4851d1ec1513a48800552bae7be1"
                          "55c6542629636bcaa672eee971dcffffffff"))
        self.assertEqual(len(tx_input.get_object_dict()), 6)

    def test_transaction_output(self):
        tx_output_data = 'a70200000000000017a9148ce773d254dc5df886b95848880e0b40f105643287'
        raw_bytes = a2b_hex(tx_output_data)
        tx_output = TransactionOutput(BytesIO(raw_bytes))
        self.assertEqual(tx_output.address,
                         '3EY3nzkz2y1BpW7oNQud4ZsL9hTTAUckKm')
        self.assertEqual(tx_output.amount, 679)
        self.assertEqual(tx_output.pubkey,
                         '8ce773d254dc5df886b95848880e0b40f1056432')
        self.assertEqual(block_util.hash_string(
            tx_output.pubkey_script), 'a9148ce773d254dc5df886b95848880e0b40f105643287')
        self.assertEqual(block_util.decipher_script(tx_output.pubkey_script), [
                         'OP_HASH160', 'OP_PUSHBYTES_20',
                         '8ce773d254dc5df886b95848880e0b40f1056432', 'OP_EQUAL'])
        self.assertEqual(tx_output.script_length, 23)
        self.assertEqual(tx_output.script_type, 'P2SH')
        self.assertEqual(len(tx_output.get_object_dict()), 7)
        self.assertEqual(tx_output.get_bytes_string(
        ), 'a70200000000000017a9148ce773d254dc5df886b95848880e0b40f105643287')

    def test_transaction_witness(self):
        tx_witness_data = ("024730440220537f470c1a18dc1a9d233c0b6af1d2ce18a07f3b244e4d9d54e0e60c34"
                           "c55e67022058169cd11ac42374cda217d6e28143abd0e79549f7b84acc6542817466dc"
                           "9b3001210301c1768b48843933bd7f0e8782716e8439fc44723d3745feefde2d57b761"
                           "f503")
        raw_bytes = a2b_hex(tx_witness_data)
        tx_witness = TransactionWitness(BytesIO(raw_bytes))

        self.assertEqual(len(tx_witness.items), 2)
        self.assertEqual(tx_witness.items_deciphered,
                         [
                             ['OP_PUSHBYTES_48',
                              ("440220537f470c1a18dc1a9d233c0b6af1d2ce18a07f3b244e4d9d54e0e60c34c5"
                               "5e67022058169cd11ac42374cda217"),
                              'OP_RETURN_214',
                              'OP_RETURN_226', 'OP_RIGHT', 'OP_PUSHBYTES_67',
                              "abd0e79549f7b84acc6542817466dc9b3001"],
                             ['OP_PUSHBYTES_3', '01c176', 'OP_1ADD',
                              'OP_PUSHBYTES_72',
                                 "843933bd7f0e8782716e8439fc44723d3745feefde2d57b761f503"
                              ]])
        self.assertEqual(tx_witness.script_lengths, [71, 33])
        self.assertEqual(tx_witness.stack_count, 2)
