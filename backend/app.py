from flask import Flask, request, jsonify
from config import app, db
from models import User, Category, Transaction, Budget, Goal
from datetime import datetime
import asyncio
from dotenv import load_dotenv
# Routes to register and login users

# Load environment variables from .env file
load_dotenv()
# routes to create, read, update, delete categories
@app.route('/categories', methods=['GET'])
## get a list of all categories
def get_categories():
    categories = Category.query.all()
    json_categories = map(lambda x: x.to_json(), categories)
    return jsonify({"categories": list(json_categories)}), 200

@app.route('/categories/stats', methods=['GET'])
def get_category_stats():
    """Get category statistics with spending information"""
    try:
        from sqlalchemy import func
        from datetime import timedelta
        
        # Get query parameters
        period = request.args.get('period', '30')  # Default last 30 days
        user_id = request.args.get('user_id', 1)  # Default user_id 1
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=int(period))
        
        # Get all categories with their spending stats
        category_stats = db.session.query(
            Category.id,
            Category.name,
            Category.type,
            Category.description,
            func.coalesce(func.sum(Transaction.amount), 0).label('total_spent'),
            func.count(Transaction.id).label('transaction_count'),
            func.coalesce(func.avg(Transaction.amount), 0).label('avg_transaction')
        ).outerjoin(
            Transaction,
            (Transaction.category_id == Category.id) & 
            (Transaction.user_id == user_id) &
            (Transaction.transaction_date >= start_date)
        ).filter(
            Category.user_id == user_id
        ).group_by(
            Category.id, Category.name, Category.type, Category.description
        ).all()
        
        # Get recent transactions per category
        recent_transactions = {}
        for stat in category_stats:
            recent = Transaction.query.filter(
                Transaction.category_id == stat.id,
                Transaction.user_id == user_id,
                Transaction.transaction_date >= start_date
            ).order_by(
                Transaction.transaction_date.desc()
            ).limit(3).all()
            
            recent_transactions[stat.id] = [t.to_json() for t in recent]
        
        # Format response
        categories_data = []
        for stat in category_stats:
            categories_data.append({
                'id': stat.id,
                'name': stat.name,
                'type': stat.type,
                'description': stat.description,
                'total_spent': float(stat.total_spent) if stat.total_spent else 0,
                'transaction_count': stat.transaction_count,
                'avg_transaction': float(stat.avg_transaction) if stat.avg_transaction else 0,
                'recent_transactions': recent_transactions.get(stat.id, [])
            })
        
        return jsonify({
            'categories': categories_data,
            'period_days': int(period)
        }), 200
        
    except Exception as e:
        print(f"❌ Error in category stats endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/categories/seed', methods=['POST'])
def seed_categories():
    """Create default categories if they don't exist"""
    try:
        user_id = request.json.get('user_id', 1) if request.json else 1
        
        # Check if user exists, if not create a default user
        user = User.query.get(user_id)
        if not user:
            # Create a default test user
            default_user = User(
                id=1,
                email='demo@financetracker.com',
                password='demo123',  # In production, this should be hashed
                username='demo',
                first_name='Demo',
                last_name='User',
                currency='GBP'
            )
            db.session.add(default_user)
            db.session.commit()
            print(f"✅ Created default user with ID: {user_id}")
        
        default_categories = [
            {'name': 'Groceries', 'type': 'expense', 'description': 'Food and household items'},
            {'name': 'Transportation', 'type': 'expense', 'description': 'Gas, public transit, parking'},
            {'name': 'Utilities', 'type': 'expense', 'description': 'Electric, water, internet, phone'},
            {'name': 'Rent/Mortgage', 'type': 'expense', 'description': 'Monthly housing payment'},
            {'name': 'Healthcare', 'type': 'expense', 'description': 'Medical, dental, prescriptions'},
            {'name': 'Entertainment', 'type': 'expense', 'description': 'Movies, games, hobbies'},
            {'name': 'Dining Out', 'type': 'expense', 'description': 'Restaurants and takeout'},
            {'name': 'Shopping', 'type': 'expense', 'description': 'Clothing, electronics, misc'},
            {'name': 'Insurance', 'type': 'expense', 'description': 'Health, car, home insurance'},
            {'name': 'Education', 'type': 'expense', 'description': 'Tuition, books, courses'},
            {'name': 'Salary', 'type': 'income', 'description': 'Monthly salary/wages'},
            {'name': 'Freelance', 'type': 'income', 'description': 'Side gig earnings'},
            {'name': 'Investments', 'type': 'income', 'description': 'Dividends, interest'},
            {'name': 'Other Income', 'type': 'income', 'description': 'Miscellaneous income'},
        ]
        
        created_count = 0
        for cat_data in default_categories:
            # Check if category already exists
            existing = Category.query.filter_by(
                name=cat_data['name'],
                user_id=user_id
            ).first()
            
            if not existing:
                new_category = Category(
                    user_id=user_id,
                    name=cat_data['name'],
                    type=cat_data['type'],
                    description=cat_data['description']
                )
                db.session.add(new_category)
                created_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': f'Successfully created {created_count} categories',
            'created_count': created_count
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding categories: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/categories/create', methods=['POST'])
def create_category():
    """Create a new custom category"""
    try:
        if not request.json:
            return jsonify({'error': 'Request must contain JSON data'}), 400
        
        name = request.json.get('name')
        category_type = request.json.get('type')
        description = request.json.get('description', '')
        user_id = request.json.get('user_id', 1)
        
        if not name or not category_type:
            return jsonify({'error': 'Name and type are required'}), 400
        
        if category_type not in ['income', 'expense']:
            return jsonify({'error': 'Type must be either "income" or "expense"'}), 400
        
        # Check if category with same name already exists for this user
        existing = Category.query.filter_by(
            name=name,
            user_id=user_id
        ).first()
        
        if existing:
            return jsonify({'error': f'Category "{name}" already exists'}), 400
        
        new_category = Category(
            user_id=user_id,
            name=name,
            type=category_type,
            description=description
        )
        
        db.session.add(new_category)
        db.session.commit()
        
        return jsonify({
            'message': 'Category created successfully',
            'category': new_category.to_json()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating category: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/categories/delete/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a category"""
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': 'Category not found'}), 404
        
        # Check if category has transactions
        transaction_count = Transaction.query.filter_by(category_id=category_id).count()
        if transaction_count > 0:
            return jsonify({
                'error': f'Cannot delete category with {transaction_count} existing transactions. Please reassign or delete those transactions first.'
            }), 400
        
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({'message': 'Category deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error deleting category: {e}")
        return jsonify({'error': str(e)}), 500



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

        # Validate category exists
        if category_id:
            category = Category.query.get(category_id)
            if not category:
                return jsonify({'error': f'Category with id {category_id} does not exist'}), 400
        else:
            # Use default category or create one if none exists
            category_id = 1

        new_transaction = Transaction(
            user_id=1,  # For now, hardcode user_id as 1
            category_id=category_id,
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
    except ValueError as ve:
        print(f"ValueError: {ve}")
        db.session.rollback()
        return jsonify({'error': f'Invalid data format: {str(ve)}'}), 400
    except Exception as e:
        print(f"Exception: {e}")
        print(f"Exception type: {type(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

   

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

# routes to create savings goals and track progress

@app.route('/goals', methods=['GET'])
def get_goals():
    goals = Goal.query.all()
    json_goals = map(lambda x: x.to_json(), goals)
    return jsonify({"goals": list(json_goals)}), 200

@app.route('/create_goal', methods=['POST'])
def create_goal():

    # Add debugging
    print("Received request data:", request.json)
    
    if not request.json:
        return jsonify({'error': 'Request must contain JSON data'}), 400
    
    name = request.json.get('name')
    description = request.json.get('description')
    target_amount = request.json.get('target_amount')
    current_amount = request.json.get('current_amount')
    deadline = request.json.get('deadline')
    priority = request.json.get('priority')
    status = request.json.get('status')
    created_at=request.json.get('created_at')
    updated_at=request.json.get('updated_at')

    print(f"Parsed data: name={name}, desc={description}, target_amount={target_amount}, current_amount={current_amount}, deadline={deadline}, priority={priority}, status={status}, created_at={created_at}, updated_at={updated_at}")

    if not name or not target_amount or not current_amount or not deadline or not priority or not status:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not created_at:
        return jsonify({'error': 'Missing required field: created_at'}), 400
    
    
    try:
        # Convert date string to datetime object
        if isinstance(created_at, str):
            # Parse date string to datetime object
            parsed_date = datetime.strptime(created_at, '%Y-%m-%d')
        else:
            parsed_date = created_at

        print(f"Parsed date: {parsed_date}")

        new_goal = Goal(
            #user_id=request.json.get('user_id'),
            #category_id=request.json.get('category_id'),
            user_id=1,  # For now, hardcode user_id as 1
            name=name or 'no Name',  # Default name if not provided
            description=description or 'No description',
            target_amount=target_amount,
            current_amount=current_amount,
            deadline=deadline,
            priority=priority,
            status=status,
            created_at=parsed_date,
            updated_at=parsed_date
        )
        
        print("Created goal object:", new_goal.__dict__)
        db.session.add(new_goal)
        db.session.commit()
        print("Goal saved successfully")
        return jsonify({'message': 'Goal created successfully', 'goal': new_goal.to_json()}), 201
    except Exception as e:
        print(f"Exception: {e}")
        print(f"Exception type: {type(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except ValueError as ve:
        print(f"ValueError: {ve}")
        db.session.rollback()
        return jsonify({'error': f'Invalid data format: {str(ve)}'}), 400

@app.route('/update_goal/<int:goal_id>', methods=['PATCH'])
def update_goal(goal_id):
    # looks in goal table for the goal with the given id
    goal = Goal.query.get(goal_id)
    if not goal:
        # if not found, return 404 error
        return jsonify({'error': 'Savings Goal not found'}), 404

    name = request.json.get('name', goal.name)
    description = request.json.get('description', goal.description)
    target_amount = request.json.get('target_amount', goal.target_amount)
    current_amount = request.json.get('current_amount', goal.current_amount)
    deadline = request.json.get('deadline', goal.deadline)
    priority = request.json.get('priority', goal.priority)
    status = request.json.get('status', goal.status)

    if not target_amount or not current_amount or not deadline or not priority or not status:
        return jsonify({'error': 'Missing required fields'}), 400

    goal.name = name
    goal.description = description
    goal.target_amount = target_amount
    goal.current_amount = current_amount
    goal.deadline = deadline
    goal.priority = priority
    goal.status = status

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    return jsonify({"Savings Goal updated": goal.to_json()}), 200

@app.route('/delete_goal/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return jsonify({'error': 'Savings Goal not found'}), 404

    try:
        db.session.delete(goal)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    return jsonify({'message': 'Savings Goal deleted successfully'}), 200
# routes to get summary reports and analytics

@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Get spending analytics and insights"""
    try:
        from sqlalchemy import func, extract
        from datetime import timedelta
        
        # Get query parameters for filtering
        period = request.args.get('period', '30')  # Default last 30 days
        user_id = request.args.get('user_id', 1)  # Default user_id 1
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=int(period))
        
        # 1. Total spending and income
        total_expenses = db.session.query(
            func.sum(Transaction.amount)
        ).filter(
            Transaction.transaction_type == 'expense',
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start_date
        ).scalar() or 0
        
        total_income = db.session.query(
            func.sum(Transaction.amount)
        ).filter(
            Transaction.transaction_type == 'income',
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start_date
        ).scalar() or 0
        
        # 2. Spending by category
        spending_by_category = db.session.query(
            Category.name,
            Category.type,
            func.sum(Transaction.amount).label('total')
        ).join(
            Transaction, Transaction.category_id == Category.id
        ).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start_date
        ).group_by(
            Category.name, Category.type
        ).all()
        
        category_data = [
            {
                'category': cat.name,
                'type': cat.type,
                'amount': float(cat.total) if cat.total else 0
            }
            for cat in spending_by_category
        ]
        
        # 3. Daily spending trend (last 30 days)
        daily_spending = db.session.query(
            func.date(Transaction.transaction_date).label('date'),
            Transaction.transaction_type,
            func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start_date
        ).group_by(
            func.date(Transaction.transaction_date),
            Transaction.transaction_type
        ).order_by(
            func.date(Transaction.transaction_date)
        ).all()
        
        trend_data = {}
        for record in daily_spending:
            date_str = record.date.strftime('%Y-%m-%d')
            if date_str not in trend_data:
                trend_data[date_str] = {'date': date_str, 'income': 0, 'expense': 0}
            
            if record.transaction_type == 'income':
                trend_data[date_str]['income'] = float(record.total) if record.total else 0
            else:
                trend_data[date_str]['expense'] = float(record.total) if record.total else 0
        
        # 4. Transaction statistics
        transaction_count = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start_date
        ).count()
        
        avg_transaction = db.session.query(
            func.avg(Transaction.amount)
        ).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_date >= start_date
        ).scalar() or 0
        
        # 5. Top spending categories (top 5)
        top_categories = db.session.query(
            Category.name,
            func.sum(Transaction.amount).label('total')
        ).join(
            Transaction, Transaction.category_id == Category.id
        ).filter(
            Transaction.user_id == user_id,
            Transaction.transaction_type == 'expense',
            Transaction.transaction_date >= start_date
        ).group_by(
            Category.name
        ).order_by(
            func.sum(Transaction.amount).desc()
        ).limit(5).all()
        
        top_categories_data = [
            {'category': cat.name, 'amount': float(cat.total) if cat.total else 0}
            for cat in top_categories
        ]
        
        return jsonify({
            'summary': {
                'total_expenses': float(total_expenses) if total_expenses else 0,
                'total_income': float(total_income) if total_income else 0,
                'net_savings': float(total_income - total_expenses) if (total_income and total_expenses) else 0,
                'transaction_count': transaction_count,
                'avg_transaction': float(avg_transaction) if avg_transaction else 0,
                'period_days': int(period)
            },
            'spending_by_category': category_data,
            'daily_trend': list(trend_data.values()),
            'top_categories': top_categories_data
        }), 200
        
    except Exception as e:
        print(f"❌ Error in analytics endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# routes to get budgeting features

# routes for chatbot

@app.route('/chat', methods=['POST'])
def chat_with_rag():
    """Handle chat requests and integrate with RAG agent"""
    try:
        if not request.json:
            return jsonify({'error': 'Request must contain JSON data'}), 400
        
        user_message = request.json.get('message')
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        print(f"🔄 Received chat message: {user_message}")
        
        # Import the RAG agent function
        try:
            from agent import agent
            
            if agent is None:
                print("⚠️ RAG agent is None, falling back to simple responses")
                raise ImportError("Agent not initialized")
            
            print("✅ RAG agent imported successfully, processing...")
            
            # Run the RAG agent asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            agent_response = loop.run_until_complete(agent.run(user_message))
            loop.close()
            
            print(f"🔍 Agent response type: {type(agent_response)}")
            print(f"🔍 Agent response object: {agent_response}")
            
            # Extract the actual text from the AgentRunResponse object
            if hasattr(agent_response, 'content'):
                response_text = agent_response.content
            elif hasattr(agent_response, 'text'):
                response_text = agent_response.text
            elif hasattr(agent_response, 'message'):
                response_text = agent_response.message
            elif hasattr(agent_response, 'result'):
                response_text = agent_response.result
            elif hasattr(agent_response, 'output'):
                response_text = agent_response.output
            else:
                # Try to convert to string as fallback
                response_text = str(agent_response)
            
            print(f"✅ Extracted response text: {response_text[:100]}...")
            
            return jsonify({
                'response': response_text,
                'source': 'rag_agent'
            }), 200
            
        except ImportError as e:
            print(f"❌ RAG agent import failed: {e}")
            # Fallback to simple rule-based responses
            response = generate_simple_response(user_message)
            return jsonify({
                'response': response,
                'source': 'fallback'
            }), 200
        except Exception as e:
            print(f"❌ RAG agent execution failed: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to simple rule-based responses
            response = generate_simple_response(user_message)
            return jsonify({
                'response': response,
                'source': 'fallback'
            }), 200
            
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500

def generate_simple_response(message):
    """Fallback function for simple responses when RAG is not available"""
    message = message.lower()
    
    if 'budget' in message:
        return "For budgeting, try the 50/30/20 rule: 50% needs, 30% wants, 20% savings. Track your expenses regularly!"
    elif 'save' in message:
        return "Start with an emergency fund covering 3-6 months of expenses. Then automate your savings!"
    elif 'expense' in message:
        return "Categorize your expenses into needs vs wants. Use this app's transaction feature to track them!"
    elif 'investment' in message:
        return "Consider low-cost index funds for long-term investing. Always do your research first!"
    else:
        return "I can help with budgeting, saving, expenses, and basic financial advice. What would you like to know?"

# Add this route for health checks

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Docker"""
    try:
        # Test database connection
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

# run flask app
if __name__ == '__main__':
    # initiate db
    with app.app_context():
        # create all tables in the database
        db.create_all()
    app.run(debug=True)

