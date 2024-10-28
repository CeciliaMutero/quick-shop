from app import db
from models.orderproduct import OrderProduct


class Order(db.model):
    """
    Model representing an order placed by a user.

    Attributes:
        id (int): The primary key for each order.
        user_id (int): Foreign key linking to the User who placed the order.
        total_price (float): Total cost of the order.
        status (str): Status of the order (e.g., 'pending', 'completed').
    """

    __tablename__ = 'orders'  # Sets the table name for the Order model

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    total_price = db.Column(db.Float, nullable=False)  # Total price of the order
    status = db.Column(db.String(20), default='pending')  # Order status

    # Relationship to link orders with products via OrderProduct
    products = db.relationship('OrderProduct', backref='order', lazy=True)

    def __repr__(self):
        """
        Returns a string representation of the Order instance.
        """
        return f'<Order {self.id} - User {self.user_id}>'
    __tablename__ = 'orders'  # Sets the table name for the Order model

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User
    total_price = db.Column(db.Float, nullable=False)  # Total price of the order
    status = db.Column(db.String(20), default='pending')  # Order status

    # Relationship to link orders with products via OrderProduct
    products = db.relationship('OrderProduct', backref='order', lazy=True)

    def __repr__(self):
        """
        Returns a string representation of the Order instance.
        """
        return f'<Order {self.id} - User {self.user_id}>'