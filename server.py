from uuid import uuid4
from flask import Flask, jsonify, request, render_template, make_response
from functools import wraps, update_wrapper
from datetime import datetime

from blockchain import Blockchain
from server_utils import get_user_transactions

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


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

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount', 'sign']
    if not all(k in values for k in required):
        response = {'message': 'Missing values'}
        return jsonify(response), 400

    if values['recipient'] not in blockchain.signatures:
        response = {'message': 'No such recipient'}
        return jsonify(response), 404

    # Create a new Transaction
    blockchain.add_transaction(values['sender'], values['recipient'], int(values['amount']), values['sign'])
    print('Transaction: {} --> {} {}'.format(values['sender'], values['recipient'], values['amount']))
    blockchain.mine()

    response = {'message': 'Transaction is added'}
    return jsonify(response), 201

"""
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200
"""
"""
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
"""

@app.route('/', methods=['GET', 'POST'])
@nocache
def form():
    return render_template('index.html')


@app.route('/user/registration', methods=['POST'])
def user_registration():
    values = request.get_json()

    required = ['name', 'publicKey']
    if not all(k in values for k in required):
        response = {'message': 'Missing values'}
        return jsonify(response), 400

    name = values.get('name')
    key = values.get('publicKey')
    if blockchain.add_user(name, key):
        print('User {} is added.'.format(name))

        response = {
            'message': 'New user have been added'
        }
        return jsonify(response), 201
    else:
        print('User {} already exists.'.format(name))

        response = {
            'message': 'Such name already exists'
        }
        return jsonify(response), 401


@app.route('/user/balance', methods=['POST'])
def balance():
    values = request.get_json()
    name = values.get('name')

    required = ['name']
    if not all(k in values for k in required):
        response = {'message': 'Missing values'}
        return jsonify(response), 400

    if name not in blockchain.signatures:
        response = {'message': 'No such name'}
        return jsonify(response), 401

    response = {
        'balance': blockchain.purse[name],
    }
    return jsonify(response), 200


@app.route('/user/transactions', methods=['POST'])
def transactions():
    values = request.get_json()
    response = get_user_transactions(blockchain, values['name'])
    print(blockchain.chain)
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
