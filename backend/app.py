from flask import Flask, request, jsonify
from config import app, db
from models import User, Category, Transaction, Budget, Goal
from datetime import datetime

# Routes to register and login users


# routes to create, read, update, delete categories
@app.route('/categories', methods=['POST'])
## get a list of all categories
def get_categories():
    categories = Category.query.all()
    json_categories = map(lambda x: x.to_json(), categories)
    return jsonify({"categories": list(json_categories)}), 200



# routes to create, read, update, delete transactions

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    json_transactions = map(lambda x: x.to_json(), transactions)
    return jsonify({"transactions": list(json_transactions)}), 200

@app.route('/create_transaction', methods=['POST'])
def create_transaction():

    # Add debugging
    print("Received request data:", request.json)
    
    if not request.json:
        return jsonify({'error': 'Request must contain JSON data'}), 400
    
    description = request.json.get('description')
    amount = request.json.get('amount')
    transaction_type = request.json.get('transaction_type')
    transaction_date = request.json.get('transaction_date')
    category_id = request.json.get('category_id')

    print(f"Parsed data: desc={description}, amount={amount}, type={transaction_type}, date={transaction_date}, cat_id={category_id}")
    
    if not amount or not transaction_type:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not transaction_date:
        return jsonify({'error': 'Missing required field: transaction_date'}), 400
    
    
    try:
        # Convert date string to datetime object
        if isinstance(transaction_date, str):
            # Parse date string to datetime object
            parsed_date = datetime.strptime(transaction_date, '%Y-%m-%d')
        else:
            parsed_date = transaction_date
        
        print(f"Parsed date: {parsed_date}")

        new_transaction = Transaction(
            #user_id=request.json.get('user_id'),
            #category_id=request.json.get('category_id'),
            user_id=1,  # For now, hardcode user_id as 1
            category_id=category_id or 1,  # Default category_id if not provided
            description=description or 'No description',
            amount=amount,
            transaction_type=transaction_type,
            transaction_date=parsed_date
        )
        
        print("Created transaction object:", new_transaction.__dict__)
        db.session.add(new_transaction)
        db.session.commit()
        print("Transaction saved successfully")
        return jsonify({'message': 'Transaction created successfully', 'transaction': new_transaction.to_json()}), 201
    except Exception as e:
        print(f"Exception: {e}")
        print(f"Exception type: {type(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except ValueError as ve:
        print(f"ValueError: {ve}")
        db.session.rollback()
        return jsonify({'error': f'Invalid data format: {str(ve)}'}), 400

   

@app.route('/update_transaction/<int:transaction_id>', methods=['PATCH'])
def update_transaction(transaction_id):
    # looks in transaction table for the transaction with the given id
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        # if not found, return 404 error
        return jsonify({'error': 'Transaction not found'}), 404

    description = request.json.get('description', transaction.description)
    amount = request.json.get('amount', transaction.amount)
    transaction_type = request.json.get('transaction_type', transaction.transaction_type)

    if not amount or not transaction_type:
        return jsonify({'error': 'Missing required fields'}), 400

    transaction.description = description
    transaction.amount = amount
    transaction.transaction_type = transaction_type

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    return jsonify({"transaction updated": transaction.to_json()}), 200

@app.route('/delete_transaction/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404

    try:
        db.session.delete(transaction)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    return jsonify({'message': 'Transaction deleted successfully'}), 200

# routes to get summary reports and analytics

# routes to get budgeting features

# routes to create savings goals and track progress

# run flask app
if __name__ == '__main__':
    # initiate db
    with app.app_context():
        # create all tables in the database
        db.create_all()
    app.run(debug=True)

