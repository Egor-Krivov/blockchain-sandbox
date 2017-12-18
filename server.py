import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request, render_template, make_response
from functools import wraps, update_wrapper
from datetime import datetime

from blockchain import Blockchain

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    print(request)

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.add_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': 'Transaction will be added to Block ' + str(index)}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

# <----------------- Below to do ---------------->

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@app.route('/', methods=['GET', 'POST'])
@nocache
def form():
    return render_template('index.html')

@app.route('/wallet_register', methods=['POST'])
def wallet_register():
    values = request.get_json()
    print('PK:', values.get('publicKey'))
    print('name:', values.get('name'))
    print(values)
    response = {
        'message': 'New wallet have been added',
    }
    return jsonify(response), 201

@app.route('/transaction', methods=['POST'])
def transaction():
    values = request.get_json()
    print(values)
    response = {
        'message': 'fail',
    }
    return jsonify(response), 200

@app.route('/balance', methods=['POST'])
def balance():
    values = request.get_json()
    print(values)
    response = {
        'balance': 100,
    }
    return jsonify(response), 200

@app.route('/transaction_list', methods=['POST'])
def transaction_list():
    values = request.get_json()
    print('transaction_list', values)
    response = {
        '1': {'sender':'egor',
              'recipient': 'ilya',
              'amount': 5,
              'n_blocks': 2},
        '2': {'sender': 'egor',
              'recipient': 'petya',
              'amount': 10,
              'n_blocks': 6}
    }
    return jsonify(response), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
