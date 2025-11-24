from config import db

# create a db model for User represented by python class
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    currency = db.Column(db.String(10), nullable=False, default='GBP')
    last_login = db.Column(db.DateTime, nullable=True)
    
    # convert user object to json
    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'currency': self.currency,
            'last_login': self.last_login
        }

# create a db model for category represented by python class
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # convert category object to json
    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'type': self.type,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# create a db model for     Transaction represented by python class
class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    transaction_date = db.Column(db.DateTime, nullable=False)

    # convert transaction object to json
    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'description': self.description,
            'amount': float(self.amount) if self.amount else 0, 
            'transaction_type': self.transaction_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None
        }

# create a db model for Budget represented by python class
class Budget(db.Model):
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    period = db.Column(db.String(20), nullable=False)  # e.g., 'monthly', 'weekly', 'yearly'
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    alert_threshold = db.Column(db.Numeric(5, 2), nullable=True, default=80.00)  # e.g., 80.00 for 80%
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # convert budget object to json
    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'amount': self.amount,
            'period': self.period,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'alert_threshold': self.alert_threshold,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# create a db model for Goals represented by python class
class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    target_amount = db.Column(db.Numeric(10, 2), nullable=False)
    current_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    deadline = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.Integer, nullable=True)  # e.g., high, medium, low
    status = db.Column(db.String(20), nullable=False)  # e.g., 'in_progress', 'completed', 'on_hold'
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    # convert goal object to json
    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'target_amount': self.target_amount,
            'current_amount': self.current_amount,
            'deadline': self.deadline,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }