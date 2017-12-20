from blockchain import Blockchain

def get_user_transactions(blockchain, username):
    transactions = {}
    chain = blockchain.chain

    index = 1
    chain_length = len(chain) - 1

    for n, block in enumerate(chain):
        for transaction in block['transactions']:
            if transaction['sender'] == username or transaction['recipient'] == username:
                transactions[index] = {
                    'sender': transaction['sender'],
                    'recipient': transaction['recipient'],
                    'amount': transaction['amount'],
                    'n_blocks': chain_length - n
                }
                index += 1

    return transactions