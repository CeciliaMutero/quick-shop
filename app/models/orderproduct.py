from app import db


class OrderProduct(db.Model):
    """
    Model representing the relationship between orders and products, 
    with a quantity for each product in the order.

    Attributes:
        id (int): The primary key for each OrderProduct association.
        order_id (int): Foreign key linking to the Order.
        product_id (int): Foreign key linking to the Product.
        quantity (int): The quantity of the product in the associated order.
    """

    __tablename__ = 'order_products'  # Sets the table name for the OrderProduct model

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)  # Foreign key to Order
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Foreign key to Product
    quantity = db.Column(db.Integer, nullable=False)  # Quantity of product in the order

    def __repr__(self):
        """
        Returns a string representation of the OrderProduct instance.
        """
        return f'<OrderProduct Order {self.order_id} - Product {self.product_id}>'