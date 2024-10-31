from app import db

class ShoppingCart(db.Model):
    """
    Model representing items in a user's shopping cart.

    Attributes:
        id (int): The primary key for each shopping cart item.
        user_id (int): Foreign key linking to the user.
        product_id (int): Foreign key linking to the product.
        quantity (int): The quantity of the product in the cart.
    """

    __tablename__ = 'shopping_carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # Define relationships with User and Product
    user = db.relationship('User', back_populates='cart_items')  # Ensure User model has back_populates='cart_items'
    product = db.relationship('Product', back_populates='cart_items')  # Ensure Product model has back_populates='cart_items'

    def __repr__(self):
        return f'<ShoppingCart user_id={self.user_id} product_id={self.product_id} quantity={self.quantity}>'

