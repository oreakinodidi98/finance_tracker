from config import app, db
from models import User, Category, Goal, Transaction  # Add Transaction import
from datetime import datetime, timedelta
import random

with app.app_context():
    try:
        # Create tables if they don't exist
        db.create_all()
        print("✅ Tables created/verified")
        
        # Check current data
        print(f"Current users: {User.query.count()}")
        print(f"Current categories: {Category.query.count()}")
        print(f"Current goals: {Goal.query.count()}")
        print(f"Current transactions: {Transaction.query.count()}")
        
        # Create test user with all required fields
        existing_user = User.query.filter_by(id=1).first()
        if not existing_user:
            user = User(
                email='john.doe@example.com',
                password='securepass123',
                username='johndoe',
                first_name='John',
                last_name='Doe',
                currency='GBP'  # Matches your default
            )
            db.session.add(user)
            db.session.flush()  # Get the ID
            print(f"✅ Created user: {user.username} (ID: {user.id})")
        else:
            print(f"ℹ️  User already exists: {existing_user.username}")
        
        # Create realistic expense categories
        expense_categories = [
            {'name': 'Groceries', 'type': 'expense', 'description': 'Food shopping and groceries'},
            {'name': 'Shopping', 'type': 'expense', 'description': 'General shopping and retail purchases'},
            {'name': 'Transport', 'type': 'expense', 'description': 'Public transport, fuel, parking'},
            {'name': 'Entertainment', 'type': 'expense', 'description': 'Movies, games, streaming services'},
            {'name': 'Dining Out', 'type': 'expense', 'description': 'Restaurants and takeaways'},
            {'name': 'Utilities', 'type': 'expense', 'description': 'Gas, electricity, water bills'},
            {'name': 'Healthcare', 'type': 'expense', 'description': 'Medical expenses and pharmacy'},
            {'name': 'Education', 'type': 'expense', 'description': 'Books, courses, training'},
            {'name': 'Leisure', 'type': 'expense', 'description': 'Hobbies and leisure activities'},
            {'name': 'Clothing', 'type': 'expense', 'description': 'Clothes and accessories'},
            {'name': 'Home', 'type': 'expense', 'description': 'Home maintenance and improvements'},
            {'name': 'Travel', 'type': 'expense', 'description': 'Holidays and travel expenses'}
        ]
        
        # Create income categories
        income_categories = [
            {'name': 'Salary', 'type': 'income', 'description': 'Monthly salary and wages'},
            {'name': 'Freelance', 'type': 'income', 'description': 'Freelance work and consultancy'},
            {'name': 'Investment', 'type': 'income', 'description': 'Dividends and investment returns'},
            {'name': 'Bonus', 'type': 'income', 'description': 'Work bonuses and incentives'},
            {'name': 'Side Business', 'type': 'income', 'description': 'Income from side business'},
            {'name': 'Gifts', 'type': 'income', 'description': 'Money gifts and cash presents'}
        ]
        
        # Combine all categories
        all_categories = expense_categories + income_categories
        
        created_count = 0
        for cat_data in all_categories:
            # Check if category already exists (by name)
            existing_cat = Category.query.filter_by(name=cat_data['name']).first()
            if not existing_cat:
                category = Category(
                    user_id=1,
                    name=cat_data['name'],
                    type=cat_data['type'],
                    description=cat_data['description']
                )
                db.session.add(category)
                created_count += 1
                print(f"✅ Created category: {cat_data['name']} ({cat_data['type']})")
            else:
                print(f"ℹ️  Category exists: {existing_cat.name}")

        # Commit categories first so we can use their IDs for transactions
        db.session.commit()

        # Create realistic transactions for the past 3 months
        transactions_data = []
        
        # Get category IDs for easier reference
        salary_cat = Category.query.filter_by(name='Salary', user_id=1).first()
        groceries_cat = Category.query.filter_by(name='Groceries', user_id=1).first()
        transport_cat = Category.query.filter_by(name='Transport', user_id=1).first()
        dining_cat = Category.query.filter_by(name='Dining Out', user_id=1).first()
        entertainment_cat = Category.query.filter_by(name='Entertainment', user_id=1).first()
        shopping_cat = Category.query.filter_by(name='Shopping', user_id=1).first()
        utilities_cat = Category.query.filter_by(name='Utilities', user_id=1).first()
        freelance_cat = Category.query.filter_by(name='Freelance', user_id=1).first()
        
        # Monthly salary (income)
        for month_offset in range(3):  # Last 3 months
            salary_date = datetime.now().replace(day=1) - timedelta(days=30 * month_offset)
            transactions_data.append({
                'description': 'Monthly Salary',
                'amount': 3500.00,
                'transaction_type': 'income',
                'category_id': salary_cat.id if salary_cat else 1,
                'transaction_date': salary_date
            })
        
        # Freelance income (occasional)
        transactions_data.extend([
            {
                'description': 'Web Development Project',
                'amount': 800.00,
                'transaction_type': 'income',
                'category_id': freelance_cat.id if freelance_cat else 2,
                'transaction_date': datetime.now() - timedelta(days=45)
            },
            {
                'description': 'Logo Design Work',
                'amount': 300.00,
                'transaction_type': 'income',
                'category_id': freelance_cat.id if freelance_cat else 2,
                'transaction_date': datetime.now() - timedelta(days=20)
            }
        ])
        
        # Regular expenses
        expense_transactions = [
            # Groceries (weekly)
            {'desc': 'Tesco Weekly Shop', 'amount': 85.50, 'cat': groceries_cat, 'days_ago': 3},
            {'desc': 'ASDA Groceries', 'amount': 92.30, 'cat': groceries_cat, 'days_ago': 10},
            {'desc': 'Sainsbury\'s Shop', 'amount': 78.90, 'cat': groceries_cat, 'days_ago': 17},
            {'desc': 'M&S Food Hall', 'amount': 45.60, 'cat': groceries_cat, 'days_ago': 24},
            {'desc': 'Local Market', 'amount': 35.20, 'cat': groceries_cat, 'days_ago': 31},
            {'desc': 'Waitrose Shopping', 'amount': 105.40, 'cat': groceries_cat, 'days_ago': 38},
            
            # Transport
            {'desc': 'Oyster Card Top-up', 'amount': 40.00, 'cat': transport_cat, 'days_ago': 5},
            {'desc': 'Petrol Station', 'amount': 55.80, 'cat': transport_cat, 'days_ago': 12},
            {'desc': 'Train Ticket', 'amount': 28.50, 'cat': transport_cat, 'days_ago': 25},
            {'desc': 'Uber Ride', 'amount': 15.30, 'cat': transport_cat, 'days_ago': 8},
            
            # Dining Out
            {'desc': 'Pizza Express', 'amount': 32.50, 'cat': dining_cat, 'days_ago': 2},
            {'desc': 'Local Pub Lunch', 'amount': 18.90, 'cat': dining_cat, 'days_ago': 7},
            {'desc': 'Chinese Takeaway', 'amount': 22.40, 'cat': dining_cat, 'days_ago': 14},
            {'desc': 'Costa Coffee', 'amount': 8.75, 'cat': dining_cat, 'days_ago': 6},
            {'desc': 'McDonald\'s', 'amount': 12.30, 'cat': dining_cat, 'days_ago': 21},
            
            # Entertainment
            {'desc': 'Netflix Subscription', 'amount': 15.99, 'cat': entertainment_cat, 'days_ago': 1},
            {'desc': 'Cinema Tickets', 'amount': 24.00, 'cat': entertainment_cat, 'days_ago': 9},
            {'desc': 'Spotify Premium', 'amount': 9.99, 'cat': entertainment_cat, 'days_ago': 15},
            {'desc': 'Game Purchase', 'amount': 49.99, 'cat': entertainment_cat, 'days_ago': 35},
            
            # Shopping
            {'desc': 'Amazon Purchase', 'amount': 67.89, 'cat': shopping_cat, 'days_ago': 4},
            {'desc': 'H&M Clothing', 'amount': 45.50, 'cat': shopping_cat, 'days_ago': 18},
            {'desc': 'John Lewis', 'amount': 89.20, 'cat': shopping_cat, 'days_ago': 28},
            {'desc': 'Argos Electronics', 'amount': 125.00, 'cat': shopping_cat, 'days_ago': 42},
            
            # Utilities
            {'desc': 'Electricity Bill', 'amount': 87.50, 'cat': utilities_cat, 'days_ago': 30},
            {'desc': 'Gas Bill', 'amount': 65.30, 'cat': utilities_cat, 'days_ago': 32},
            {'desc': 'Internet Bill', 'amount': 35.00, 'cat': utilities_cat, 'days_ago': 15},
        ]
        
        # Convert expense transactions to proper format
        for exp in expense_transactions:
            transactions_data.append({
                'description': exp['desc'],
                'amount': exp['amount'],
                'transaction_type': 'expense',
                'category_id': exp['cat'].id if exp['cat'] else 1,
                'transaction_date': datetime.now() - timedelta(days=exp['days_ago'])
            })
        
        # Create transactions
        transactions_created = 0
        for trans_data in transactions_data:
            # Check if transaction already exists
            existing_trans = Transaction.query.filter_by(
                description=trans_data['description'],
                user_id=1,
                transaction_date=trans_data['transaction_date']
            ).first()
            
            if not existing_trans:
                transaction = Transaction(
                    user_id=1,
                    description=trans_data['description'],
                    amount=trans_data['amount'],
                    transaction_type=trans_data['transaction_type'],
                    category_id=trans_data['category_id'],
                    transaction_date=trans_data['transaction_date']
                )
                db.session.add(transaction)
                transactions_created += 1
                
                type_emoji = "💰" if trans_data['transaction_type'] == 'income' else "💸"
                print(f"✅ Created transaction: {type_emoji} {trans_data['description']} - £{trans_data['amount']}")
            else:
                print(f"ℹ️  Transaction exists: {existing_trans.description}")

        # Create realistic savings goals
        savings_goals = [
            {
                'name': 'Emergency Fund',
                'description': 'Build up 6 months of expenses for emergencies',
                'target_amount': 10000.00,
                'current_amount': 2500.00,
                'deadline': datetime.now() + timedelta(days=365),
                'priority': 1,
                'status': 'in_progress'
            },
            {
                'name': 'Holiday to Japan',
                'description': 'Save for a 2-week trip to Tokyo and Kyoto',
                'target_amount': 4500.00,
                'current_amount': 800.00,
                'deadline': datetime.now() + timedelta(days=240),
                'priority': 2,
                'status': 'in_progress'
            },
            {
                'name': 'New Laptop',
                'description': 'MacBook Pro for work and personal projects',
                'target_amount': 2500.00,
                'current_amount': 1200.00,
                'deadline': datetime.now() + timedelta(days=90),
                'priority': 2,
                'status': 'in_progress'
            },
            {
                'name': 'House Deposit',
                'description': 'Save for a deposit on first home purchase',
                'target_amount': 50000.00,
                'current_amount': 8500.00,
                'deadline': datetime.now() + timedelta(days=1095),
                'priority': 1,
                'status': 'in_progress'
            },
            {
                'name': 'Car Replacement',
                'description': 'Save to replace old car with a reliable used one',
                'target_amount': 15000.00,
                'current_amount': 3200.00,
                'deadline': datetime.now() + timedelta(days=450),
                'priority': 2,
                'status': 'in_progress'
            },
            {
                'name': 'Wedding Fund',
                'description': 'Save for dream wedding celebration',
                'target_amount': 25000.00,
                'current_amount': 5800.00,
                'deadline': datetime.now() + timedelta(days=600),
                'priority': 1,
                'status': 'in_progress'
            },
            {
                'name': 'Online Course',
                'description': 'Professional development certification course',
                'target_amount': 800.00,
                'current_amount': 800.00,
                'deadline': datetime.now() - timedelta(days=30),
                'priority': 3,
                'status': 'completed'
            },
            {
                'name': 'Home Office Setup',
                'description': 'Ergonomic desk, chair, and lighting for home office',
                'target_amount': 1200.00,
                'current_amount': 450.00,
                'deadline': datetime.now() + timedelta(days=60),
                'priority': 2,
                'status': 'in_progress'
            },
            {
                'name': 'Investment Portfolio',
                'description': 'Initial investment in diversified portfolio',
                'target_amount': 5000.00,
                'current_amount': 1800.00,
                'deadline': datetime.now() + timedelta(days=180),
                'priority': 2,
                'status': 'in_progress'
            },
            {
                'name': 'Christmas Gifts',
                'description': 'Budget for family Christmas presents',
                'target_amount': 600.00,
                'current_amount': 150.00,
                'deadline': datetime(2025, 12, 15),
                'priority': 3,
                'status': 'in_progress'
            }
        ]
        
        goals_created = 0
        for goal_data in savings_goals:
            existing_goal = Goal.query.filter_by(name=goal_data['name'], user_id=1).first()
            if not existing_goal:
                goal = Goal(
                    user_id=1,
                    name=goal_data['name'],
                    description=goal_data['description'],
                    target_amount=goal_data['target_amount'],
                    current_amount=goal_data['current_amount'],
                    deadline=goal_data['deadline'],
                    priority=goal_data['priority'],
                    status=goal_data['status']
                )
                db.session.add(goal)
                goals_created += 1
                
                progress = (goal_data['current_amount'] / goal_data['target_amount']) * 100
                print(f"✅ Created goal: {goal_data['name']} - £{goal_data['current_amount']}/£{goal_data['target_amount']} ({progress:.1f}%)")
            else:
                print(f"ℹ️  Goal exists: {existing_goal.name}")
        
        # Commit all changes
        db.session.commit()
        print(f"\n🎉 Successfully created {created_count} new categories, {transactions_created} new transactions, and {goals_created} new goals!")
        
        # Calculate and display financial summary
        all_transactions = Transaction.query.filter_by(user_id=1).all()
        total_income = sum(float(t.amount) for t in all_transactions if t.transaction_type == 'income')
        total_expenses = sum(float(t.amount) for t in all_transactions if t.transaction_type == 'expense')
        net_balance = total_income - total_expenses
        
        print(f"\n💰 Financial Summary:")
        print(f"   Total Income: £{total_income:.2f}")
        print(f"   Total Expenses: £{total_expenses:.2f}")
        print(f"   Net Balance: £{net_balance:.2f}")
        
        balance_status = "🟢 Positive" if net_balance > 0 else "🔴 Negative" if net_balance < 0 else "🟡 Neutral"
        print(f"   Status: {balance_status}")
        
        # Show final summary
        print(f"\n📊 Final Database Summary:")
        print(f"👥 Total Users: {User.query.count()}")
        print(f"📂 Total Categories: {Category.query.count()}")
        print(f"💳 Total Transactions: {Transaction.query.count()}")
        print(f"🎯 Total Goals: {Goal.query.count()}")
        
        print(f"\n🎯 You can now:")
        print(f"   - View real financial data on your Home page")
        print(f"   - See transactions with User ID: 1")
        print(f"   - Use Category IDs: 1 to {Category.query.count()}")
        print(f"   - Track progress on {Goal.query.count()} savings goals")
        print(f"   - Your total balance will show: £{net_balance:.2f}")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating test data: {e}")
        import traceback
        traceback.print_exc()