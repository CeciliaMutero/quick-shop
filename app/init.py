from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)
# location of my quickshop database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Shish1993%24@localhost/quickshop'
# connecting database to app
db = SQLAlchemy(app)
# Import routes from the routes module
from app import routes
