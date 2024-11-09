import os
import sys
sys.path.append(f"{os.getcwd()}")
from models.Mempool import Mempool
from binascii import a2b_hex
from io import BytesIO
from utils.block_util import *
import unittest

class MempoolTest(unittest.TestCase):
    def test_mempool(self):
        mempool_data = '0100000000000000010000000000000001000000017dc9c2cca6aaf622939e28e14a428d21c7be5ef2893cf575e2735e2b3215497e010000006b483045022100f3d0d3f0c529c19362173db79b1824e33bcc3015d7f069b7ae24440114e5039002207eb23d92ca2758b9f6a43b7cbd265fb34c56d60faedaf04d805b928a2604223901210309e1b5495082f8aa6df37d8758379df33965596d028165ae8073b6219942febbffffffff0120f40e00000000001976a914acf3cb08d55344b6178b37ae58f171c769413fa888ac0000000001000000000000000100000000000000'
        raw_bytes = a2b_hex(mempool_data)
        mempool = Mempool(BytesIO(raw_bytes))

        self.assertEqual(mempool.transaction_count, 1)
        self.assertEqual(len(mempool.transaction_list), 1)
        self.assertEqual(mempool.transaction_list[0]['entry_time'], 1)
        self.assertEqual(mempool.transaction_list[0]['fee'], 1)
