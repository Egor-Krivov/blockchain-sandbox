import unittest

from crypto_utils import compute_proof_of_work_from_header, compute_block_hash_from_header_and_nonce, \
    verify_block_hash_difficulty


def verify_block_header_and_nounce(block_header, nonce):
    return verify_block_hash_difficulty(compute_block_hash_from_header_and_nonce(block_header, nonce))


class TestProofOfWork(unittest.TestCase):
    def test_header_functions(self):
        block_header = 'Test header'
        block_hash, nonce = compute_proof_of_work_from_header(block_header)
        self.assertSequenceEqual(block_hash, compute_block_hash_from_header_and_nonce(block_header, nonce))
        self.assertTrue(verify_block_header_and_nounce(block_header, nonce))
