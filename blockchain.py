import requests
from time import time
from uuid import uuid4

from money_source import money_source
from crypto_utils import compute_proof_of_work, model_transactions
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
            'timestamp': time(),
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

    @property
    def last_block(self):
        return self.chain[-1]

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: <str> Address of node. Eg. 'http://192.168.0.5:5000'
        :return: None
        """

        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """
        # TODO rewrite

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(last_block)
            print(block)
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not validate_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our Consensus Algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: <bool> True if our chain was replaced, False if not
        """
        # TODO check

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get('http://' + node + '/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False
