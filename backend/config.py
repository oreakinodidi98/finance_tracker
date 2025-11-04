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

# Use Docker-compatible fallback URL
fallback_url = 'postgresql://postgres:FavourofGod1@db:5432/finance_tracker'
database_url = os.getenv('DATABASE_URL', fallback_url)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # To not track modifications of data

# Debug output
print(f"DATABASE_URL from env: {os.getenv('DATABASE_URL')}")
print(f"Using database URL: {database_url}")

# create SQLAlchemy db instance
db = SQLAlchemy(app)