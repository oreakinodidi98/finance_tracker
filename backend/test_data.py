from config import app, db
from models import User, Category

with app.app_context():
    try:
        # Create tables if they don't exist
        db.create_all()
        print("✅ Tables created/verified")
        
        # Check current data
        print(f"Current users: {User.query.count()}")
        print(f"Current categories: {Category.query.count()}")
        
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
        
        # Commit all changes
        db.session.commit()
        print(f"\n🎉 Successfully created {created_count} new categories!")
        
        # Show final summary
        print(f"\n📊 Final Database Summary:")
        print(f"👥 Total Users: {User.query.count()}")
        print(f"📂 Total Categories: {Category.query.count()}")
        
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
            
        print(f"\n🎯 You can now create transactions using:")
        print(f"   - User ID: 1")
        print(f"   - Category IDs: 1 to {Category.query.count()}")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating test data: {e}")
        import traceback
        traceback.print_exc()