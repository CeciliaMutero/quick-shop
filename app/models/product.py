from app import db
from app.models.orderproduct import OrderProduct

class Product(db.Model):
    """
    Model representing a product in the e-commerce store.

    Attributes:
        id (int): The primary key for each product.
        name (str): The name of the product.
        description (str): A text field for product details.
        price (float): The price of the product.
        stock (int): Quantity available in stock.
    """
   # table name for the Product model
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Product name, required
    description = db.Column(db.Text, nullable=True)  # Optional product description
    price = db.Column(db.Float, nullable=False)  # Product price, required
    stock = db.Column(db.Integer, nullable=False, default=0)  # Quantity in stock

    # Relationships
    orders = db.relationship('OrderProduct', backref='product', lazy=True)
    cart_items = db.relationship('ShoppingCart', back_populates='product', cascade="all, delete-orphan")
    
    def __repr__(self):
        """
        Returns a string representation of the Product instance.
        """
        return f'<Product {self.name}>'