from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
import os

login_manager = LoginManager()

# Create an instance of SQLAlchemy
db = SQLAlchemy()
migrate = Migrate()  # Initialize Migrate

def create_app():
    """
    Creates and configures the Flask application.
    
    This function initializes the Flask app, sets up the database configuration,
    and imports models. It returns the configured app object.

    Returns:
        Flask app: The configured Flask application instance.
    """
    # Initialize the Flask application
    app = Flask(__name__)

    # Configure the location of the quickshop database
    app.config['SECRET_KEY'] = os.urandom(24)  # Generates a random secret key for security
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Shish1993%24@localhost/quickshop'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect the database to the app
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Migrate with the app and db

    # Set the login view for Flask-Login
    login_manager.login_view = 'main.login'  # Define where to redirect for login
    login_manager.init_app(app)  # Initialize with the app

    # Import and register models
    with app.app_context():
        from app.models.product import Product  # Import product model
        from app.models.order import Order  # Import order model
        from app.models.user import User  # Import user model
        from app.models.orderproduct import OrderProduct  # Import orderproduct model
        from app.models.shopping_cart import ShoppingCart
        db.create_all()  # Create all database tables

    @login_manager.user_loader
    def load_user(user_id):
        """
        Load a user from the database using the user ID.

        Args:
            user_id (int): The ID of the user to load.

        Returns:
            User: The user instance, or None if not found.
        """
        from .models.user import User
        return User.query.get(int(user_id))

    # Initialize Flask-Admin
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')
    admin.add_view(ModelView(Product, db.session))  # Add Product model to admin

    # Import and register the Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Return the app, which is now ready for use
    return app
