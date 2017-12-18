import hashlib

from money_source import money_source
from log import logging

difficulty_bits = 10
target = 2 ** (256 - difficulty_bits)
max_nonce = 2 ** 32


# Functions used by the blockchain
def compute_proof_of_work(block):
    """Find proof of work for a given block"""
    return compute_proof_of_work_from_header(compute_block_header(block))


def model_transactions(transactions, starting_purse: dict, signatures) -> ([dict], dict):
    """Model all transactions starting from the starting_purse.
    Checks for negative balance and wrong signatures.
    Returns all valid transactions and final purse.
    """
    purse = starting_purse.copy()
    verified_transactions = []
    for transaction in transactions:
        logging.debug('Processing transaction ' + str(transaction))
        sender, recipient, amount = transaction['sender'], transaction['recipient'], transaction['amount']
        if not verify_transaction_signature(transaction, signatures[sender]):
            logging.debug('Signature was wrong')
        elif sender not in purse or recipient not in purse:
            logging.debug('Unknown parties')
        elif amount <= 0 or sender == recipient or (sender != money_source and purse[sender] - amount < 0):
            logging.debug('Impossible operation')
        else:
            logging.debug('Processing transaction')
            if sender != money_source:
                purse[sender] -= amount
            purse[recipient] += amount
            verified_transactions.append(transaction)
    return transactions, purse


def verify_transaction_signature(transaction, signature):
    if transaction['sender'] == money_source:
        return True
    # TODO normal signing
    return True


def verify_block_hash(block):
    block_hash = compute_block_hash(block)
    return block_hash == block['hash'] and verify_block_hash_difficulty(block_hash)


# Crypto functions for blocks
def compute_block_hash(block):
    return compute_block_hash_from_header_and_nonce(compute_block_header(block), block['nonce'])


def compute_block_header(block):
    # block_string = json.dumps(block, sort_keys=True).encode()
    # return hashlib.sha256(block_string).hexdigest()
    # TODO rewrite
    return '10'


def compute_transaction_hash(transaction):
    transaction_header = transaction['sender'] + transaction['receiver'] + str(transaction['amount'])
    return hashlib.sha256(transaction_header.encode('utf-8').hexdigest())


# Crypto functions for block header
def compute_proof_of_work_from_header(block_header):
    for nonce in range(max_nonce):
        block_hash = compute_block_hash_from_header_and_nonce(block_header, nonce)

        if verify_block_hash_difficulty(block_hash):
            return block_hash, nonce


def compute_block_hash_from_header_and_nonce(block_header, nonce):
    return hashlib.sha256(str(block_header).encode('utf-8') + str(nonce).encode('utf-8')).hexdigest()


def verify_block_hash_difficulty(block_hash):
    return int(block_hash, 16) < target