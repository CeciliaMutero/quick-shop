from app import db
from flask_login import UserMixin  # Import UserMixin


class User(UserMixin, db.Model):
    """
    Model representing a registered user.

    Attributes:
        id (int): The primary key for each user.
        username (str): Unique username chosen by the user.
        email (str): Unique email address of the user.
        password (str): Hashed password for secure authentication.
    """

    __tablename__ = 'users'  # Sets the table name for the User model

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username, required
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique email, required
    password = db.Column(db.String(512), nullable=False)  # Hashed password

    # Relationship to associate users with orders
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        """
        Returns a string representation of the User instance.
        """
        return f'<User {self.username}>'
    
    from app.models.order import Order