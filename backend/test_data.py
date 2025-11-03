from config import app, db
from models import User, Category, Goal
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
        
        # Create realistic savings goals
        savings_goals = [
            {
                'name': 'Emergency Fund',
                'description': 'Build up 6 months of expenses for emergencies',
                'target_amount': 10000.00,
                'current_amount': 2500.00,
                'deadline': datetime.now() + timedelta(days=365),  # 1 year from now
                'priority': 1,  # High priority
                'status': 'in_progress'
            },
            {
                'name': 'Holiday to Japan',
                'description': 'Save for a 2-week trip to Tokyo and Kyoto',
                'target_amount': 4500.00,
                'current_amount': 800.00,
                'deadline': datetime.now() + timedelta(days=240),  # 8 months from now
                'priority': 2,  # Medium priority
                'status': 'in_progress'
            },
            {
                'name': 'New Laptop',
                'description': 'MacBook Pro for work and personal projects',
                'target_amount': 2500.00,
                'current_amount': 1200.00,
                'deadline': datetime.now() + timedelta(days=90),  # 3 months from now
                'priority': 2,  # Medium priority
                'status': 'in_progress'
            },
            {
                'name': 'House Deposit',
                'description': 'Save for a deposit on first home purchase',
                'target_amount': 50000.00,
                'current_amount': 8500.00,
                'deadline': datetime.now() + timedelta(days=1095),  # 3 years from now
                'priority': 1,  # High priority
                'status': 'in_progress'
            },
            {
                'name': 'Car Replacement',
                'description': 'Save to replace old car with a reliable used one',
                'target_amount': 15000.00,
                'current_amount': 3200.00,
                'deadline': datetime.now() + timedelta(days=450),  # 15 months from now
                'priority': 2,  # Medium priority
                'status': 'in_progress'
            },
            {
                'name': 'Wedding Fund',
                'description': 'Save for dream wedding celebration',
                'target_amount': 25000.00,
                'current_amount': 5800.00,
                'deadline': datetime.now() + timedelta(days=600),  # 20 months from now
                'priority': 1,  # High priority
                'status': 'in_progress'
            },
            {
                'name': 'Online Course',
                'description': 'Professional development certification course',
                'target_amount': 800.00,
                'current_amount': 800.00,  # Already completed!
                'deadline': datetime.now() - timedelta(days=30),  # Completed last month
                'priority': 3,  # Low priority
                'status': 'completed'
            },
            {
                'name': 'Home Office Setup',
                'description': 'Ergonomic desk, chair, and lighting for home office',
                'target_amount': 1200.00,
                'current_amount': 450.00,
                'deadline': datetime.now() + timedelta(days=60),  # 2 months from now
                'priority': 2,  # Medium priority
                'status': 'in_progress'
            },
            {
                'name': 'Investment Portfolio',
                'description': 'Initial investment in diversified portfolio',
                'target_amount': 5000.00,
                'current_amount': 1800.00,
                'deadline': datetime.now() + timedelta(days=180),  # 6 months from now
                'priority': 2,  # Medium priority
                'status': 'in_progress'
            },
            {
                'name': 'Christmas Gifts',
                'description': 'Budget for family Christmas presents',
                'target_amount': 600.00,
                'current_amount': 150.00,
                'deadline': datetime(2025, 12, 15),  # Christmas 2025
                'priority': 3,  # Low priority
                'status': 'in_progress'
            }
        ]
        
        goals_created = 0
        for goal_data in savings_goals:
            # Check if goal already exists (by name and user_id)
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
                
                # Calculate progress percentage
                progress = (goal_data['current_amount'] / goal_data['target_amount']) * 100
                print(f"✅ Created goal: {goal_data['name']} - £{goal_data['current_amount']}/£{goal_data['target_amount']} ({progress:.1f}%)")
            else:
                print(f"ℹ️  Goal exists: {existing_goal.name}")
        
        # Commit all changes
        db.session.commit()
        print(f"\n🎉 Successfully created {created_count} new categories and {goals_created} new goals!")
        
        # Show final summary
        print(f"\n📊 Final Database Summary:")
        print(f"👥 Total Users: {User.query.count()}")
        print(f"📂 Total Categories: {Category.query.count()}")
        print(f"🎯 Total Goals: {Goal.query.count()}")
        
        # List all users
        print(f"\n👥 Users:")
        for user in User.query.all():
            print(f"  • ID: {user.id} | {user.first_name} {user.last_name} (@{user.username}) | {user.email}")
            
        # List categories by type
        print(f"\n💸 Expense Categories:")
        expense_cats = Category.query.filter_by(type='expense').all()
        for cat in expense_cats:
            print(f"  • ID: {cat.id} | {cat.name}")
            
        print(f"\n💰 Income Categories:")
        income_cats = Category.query.filter_by(type='income').all()
        for cat in income_cats:
            print(f"  • ID: {cat.id} | {cat.name}")
            
        # List savings goals with progress
        print(f"\n🎯 Savings Goals:")
        goals = Goal.query.filter_by(user_id=1).order_by(Goal.priority, Goal.deadline).all()
        for goal in goals:
            progress = (float(goal.current_amount) / float(goal.target_amount)) * 100
            status_emoji = "✅" if goal.status == "completed" else "🔄" if goal.status == "in_progress" else "⏸️"
            priority_text = {1: "🔥 High", 2: "🟡 Medium", 3: "🟢 Low"}.get(goal.priority, "❓ Unknown")
            
            days_left = (goal.deadline - datetime.now()).days
            deadline_text = f"({days_left} days)" if days_left > 0 else "(Overdue)" if days_left < 0 else "(Today)"
            
            print(f"  • ID: {goal.id} | {status_emoji} {goal.name}")
            print(f"    Progress: £{goal.current_amount}/£{goal.target_amount} ({progress:.1f}%)")
            print(f"    Priority: {priority_text} | Deadline: {goal.deadline.strftime('%Y-%m-%d')} {deadline_text}")
            print(f"    Description: {goal.description}")
            print()
            
        print(f"🎯 You can now:")
        print(f"   - Create transactions with User ID: 1")
        print(f"   - Use Category IDs: 1 to {Category.query.count()}")
        print(f"   - Track progress on {Goal.query.count()} savings goals")
        print(f"   - View goals on your Goals page!")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating test data: {e}")
        import traceback
        traceback.print_exc()