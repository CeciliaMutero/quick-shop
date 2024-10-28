from app import db
class Produc"""
    Model representing a product in the e-commerce store.

    Attributes:
        id (int): The primary key for each product.
        name (str): The name of the product.
        description (str): A text field for product details.
        price (float): The price of the product.
        stock (int): Quantity available in stock.
    """t(db.model):

    __tablename__ = 'product'