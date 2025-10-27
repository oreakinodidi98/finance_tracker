from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#cors = cross origin resource sharing. Allowing frontend and backend to communicate.
import os

# initialize Flask app
app = Flask(__name__)

# configure CORS -> dissable CORS in production for security reasons
CORS(app)

# configure database
# Specify location of the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:FavourofGod1@localhost:5432/finance_tracker')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # To not track modifications of data

# create SQLAlchemy db instance
db = SQLAlchemy(app)