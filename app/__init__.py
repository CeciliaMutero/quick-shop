from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create an instance of SQLAlchemy
db = SQLAlchemy()

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Shish1993%24@localhost/quickshop'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Connect the database to the app
    db.init_app(app)

    # Import and register models
    with app.app_context():
        from .models import product  # Import product model
        db.create_all()  # Create all database tables

    # Import and register the Blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Return the app, which is now ready for use
    return app
