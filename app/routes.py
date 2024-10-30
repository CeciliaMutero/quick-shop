from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models.user import User
from app.models.product import Product
from app.models.order import Order 
from app.models.orderproduct import OrderProduct
from werkzeug.security import generate_password_hash, check_password_hash

# Define a Blueprint
main = Blueprint('main', __name__)

# Home route
@main.route('/')
def home():
    return "Hello, World!"

# Registration route
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
        
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'danger')
            return redirect(url_for('main.register'))  # Redirect back to registration
        # Hash the password before saving to the database
        hashed_password = generate_password_hash(form.password.data)
        # Create a new user instance
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # Make sure to hash the password
        db.session.add(user)  # Add user to the database session
        db.session.commit()  # Commit the session to save the user to the database
        flash('Your account has been created!', 'success')  # Show success message
        return redirect(url_for('main.login'))  # Redirect to the login page after registration
    return render_template('register.html', form=form)  # Render the registration template with the form

# Login route
@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Find user by email
        if user and check_password_hash(user.password, form.password.data):  # Check if user exists and password matches
            login_user(user)  # Log in the user
            flash('Login successful!', 'success')  # Show success message
            return redirect(url_for('main.home'))  # Redirect to the home page after login
        else:
            flash('Login unsuccessful. Please check your email and password', 'danger')  # Show error message
    return render_template('login.html', form=form)  # Render the login template with the form

# Logout route
@main.route('/logout')
@login_required  # Require the user to be logged in to access this route
def logout():
    logout_user()  # Log out the user
    flash('You have been logged out.', 'success')  # Show logout success message
    return redirect(url_for('main.home'))  # Redirect to the home page

# Products route - list all products
@main.route('/products')
def product_list():
    # Get sorting parameter from query string
    sort_by = request.args.get('sort', 'name')  # Default to 'name' if no sort is provided

    # Apply sorting based on sort_by parameter
    if sort_by == 'name':
        products_query = Product.query.order_by(Product.name.asc())
    elif sort_by == 'price':
        products_query = Product.query.order_by(Product.price.asc())
    else:
        products_query = Product.query  # Default query if no valid sort option

    # Pagination
    page = request.args.get('page', 1, type=int)
    products = products_query.paginate(page=page, per_page=10)

    return render_template('product_list.html', products=products, sort_by=sort_by)

# Product detail route - view details of a specific product
@main.route('/products/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)  # Retrieve a single product by ID or 404 if not found
    return render_template('product_detail.html', product=product)

# Orders route
@main.route('/orders')
@login_required
def manage_orders():
    # Fetch orders for the logged-in user, including related products
    user_orders = Order.query.filter_by(user_id=current_user.id).all()

    # Render the orders template, passing in the user's orders
    return render_template('orders.html', orders=user_orders)
