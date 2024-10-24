from app import app
@app.route('/')
def home():
    """Route for the homepage that returns a welcome message."""
    return "Hello, Flask!"