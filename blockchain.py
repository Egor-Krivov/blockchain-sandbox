import requests
from time import time
from uuid import uuid4

from money_source import money_source
from crypto_utils import compute_proof_of_work, model_transactions, verify_block_hash
from urllib.parse import urlparse
from log import logging

starting_balance = 100


class Blockchain:
    def __init__(self):
        # Generate a globally unique address for this node
        self.node_identifier = str(uuid4()).replace('-', '')

        # Purse keeps money of all users at the latest block, not including current transactions
        self.purse = {self.node_identifier: 0, money_source: 0}
        # Public keys of all users
        self.signatures = {self.node_identifier: '0', money_source: '0'}

        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # Create the genesis block
        self.mine(previous_hash=1)

    def add_user(self, name, public_key):
        if name not in self.signatures:
            self.signatures[name] = public_key
            self.purse[name] = 0
            self.add_transaction(money_source, name, starting_balance, self.signatures[money_source])
            return True
        else:
            return False

    def mine(self, previous_hash=None):
        """Create a new Block in the Blockchain"""

        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin.
        self.add_transaction("0", self.node_identifier, 1, self.signatures[money_source])

        valid_transactions, new_purse = model_transactions(self.current_transactions, self.purse, self.signatures)
        if len(valid_transactions) != len(self.current_transactions):
            logging.debug('Some transactions were rejected!')

        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(time()),
            'transactions': valid_transactions,
            'previous_hash': previous_hash or self.chain[-1]['hash']
        }

        block['hash'], block['nonce'] = compute_proof_of_work(block)

        self.purse = new_purse
        self.current_transactions = []
        self.chain.append(block)

    def add_transaction(self, sender, recipient, amount, signature):
        """Creates a new transaction to go into the next mined Block"""
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'signature': signature
        })
    