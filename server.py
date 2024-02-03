from flask import Flask, jsonify, request
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Simulated account balance data
with open('users.json') as f:
    account_balance = json.load(f)

@app.route('/account/balance', methods=['GET'])
def get_account_balance():
    return jsonify(account_balance)

@app.route('/account/send', methods=['POST'])
def send_money():
    try:
        data = request.get_json()
        sender = data.get('user')
        recipient = data.get('recipient')
        amount = data.get('amount')
        
        sender_found = False
        recipient_found = False
        sender_index = None
        recipient_index = None

        # Search for sender and recipient in the list
        for index, user in enumerate(account_balance['users']):
            if user['name'] == sender:
                sender_found = True
                sender_index = index
            if user['name'] == recipient:
                recipient_found = True
                recipient_index = index
        
        # Process the transaction if both are found and sender has enough money
        if sender_found and recipient_found and account_balance['users'][sender_index]['money'] >= int(amount):
            account_balance['users'][sender_index]['money'] -= int(amount)
            account_balance['users'][recipient_index]['money'] += int(amount)
            return jsonify({'message': f'Successfully sent {amount} from {sender} to {recipient}.'})
        else:
            return jsonify({'message': 'Insufficient balance or user not found.'}), 400

    except Exception as e:
        print("An error occurred: ", e)
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/account/add', methods=['POST'])
def add_money():
    data = request.get_json()
    user = data.get('user')
    amount = data.get('amount')

    if user in account_balance:
        account_balance[user] += amount
        return jsonify({'message': f'Successfully added {amount} to {user}.'})
    else:
        return jsonify({'message': 'User not found.'}), 400
    
@app.route('/account/create_or_update', methods=['POST'])
def create_or_update_user():
    data = request.get_json()
    user = data.get('user')
    amount = data.get('amount')

    if user not in account_balance:  # If user does not exist, add them.
        account_balance[user] = amount
        message = f'User {user} created with balance {amount}.'
    else:  # If user exists, update their balance.
        account_balance[user] += amount
        message = f'Balance for {user} updated to {amount}.'

    # Note: We're not writing changes back to the 'users.json' file

    return jsonify({'message': message})

if __name__ == '__main__':
    app.run()
