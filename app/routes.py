from flask import Blueprint

# Define a Blueprint
main = Blueprint('main', __name__)

# Define routes using the Blueprint
@main.route('/')
def home():
    return "Hello, World!"
