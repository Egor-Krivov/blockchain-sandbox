import unittest

from blockchain import Blockchain


class TestBlockchain(unittest.TestCase):
    def test_wallets(self):
        blockchain = Blockchain()
        blockchain.add_user('alice', '1234')
        blockchain.add_user('bob', '1243')
        blockchain.mine()
        self.assertEqual(blockchain.purse['alice'], blockchain.purse['bob'])
        self.assertEqual(blockchain.purse['bob'], 100)

        blockchain.add_transaction('alice', 'bob', 50, '1231412')
        blockchain.mine()

        self.assertEqual(blockchain.purse['alice'], 50)
        self.assertEqual(blockchain.purse['bob'], 150)
        self.assertEqual(blockchain.purse[blockchain.node_identifier], 3)

        print(blockchain.chain)
