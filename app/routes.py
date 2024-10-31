from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.orderproduct import OrderProduct
from app.models.shopping_cart import ShoppingCart
from werkzeug.security import generate_password_hash, check_password_hash


# Define a Blueprint
main = Blueprint('main', __name__)


# Home route
@main.route('/')
def home():
    """Home route for the application."""
    return "Hello, World!"


# Registration route
@main.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route to handle user registration.
    If the form is valid, create a new user with hashed password and add them to the database.

    Returns:
        Redirect to login on successful registration, or re-render registration form on failure.
    """
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
    """
    Route to handle user login.
    If the form is valid and credentials are correct, logs in the user.

    Returns:
        Redirect to home page on successful login, or re-render login form on failure.
    """
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
    """
    Route to handle user logout.

    Returns:
        Redirect to home page after logout.
    """
    logout_user()  # Log out the user
    flash('You have been logged out.', 'success')  # Show logout success message
    return redirect(url_for('main.home'))  # Redirect to the home page


# Products route - list all products
@main.route('/products')
def product_list():
    """
    Route to display a list of products.
    Supports sorting by name or price, with pagination.

    Returns:
        Rendered product list template with sorted and paginated product data.
    """
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
    """
    Route to display details for a specific product.

    Args:
        product_id (int): The ID of the product to display.

    Returns:
        Rendered product detail template for the specified product.
    """
    product = Product.query.get_or_404(product_id)  # Retrieve a single product by ID or 404 if not found
    return render_template('product_detail.html', product=product)


# Orders route
@main.route('/orders')
@login_required
def manage_orders():
    """
    Route to display orders for the currently logged-in user.

    Returns:
        Rendered orders template with user-specific order data.
    """
    # Fetch orders for the logged-in user, including related products
    user_orders = Order.query.filter_by(user_id=current_user.id).all()

    # Render the orders template, passing in the user's orders
    return render_template('orders.html', orders=user_orders)


# Shopping Cart Routes
@main.route('/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    """
    Route to add a product to the shopping cart.
    If the item is already in the cart, updates the quantity. Otherwise, adds a new item.

    Returns:
        JSON response with success message and updated cart item data.
    """
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    cart_item = ShoppingCart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = ShoppingCart(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({"message": "Item added to cart", "cart_item": {"product_id": product_id, "quantity": cart_item.quantity}}), 200


@main.route('/cart/remove', methods=['DELETE'])
@login_required
def remove_from_cart():
    """
    Route to remove an item from the shopping cart based on product ID.

    Returns:
        JSON response with success message if item is removed, error if item not found in cart.
    """
    data = request.get_json()
    product_id = data.get('product_id')

    cart_item = ShoppingCart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not cart_item:
        return jsonify({"error": "Item not in cart"}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Item removed from cart"}), 200


@main.route('/cart')
@login_required
def view_cart():
    """
    Route to display the current user's shopping cart contents, including total price.

    Returns:
        Rendered cart template with list of items in cart and total price.
    """
    cart_items = ShoppingCart.query.filter_by(user_id=current_user.id).all()
    cart_details = []
    total_price = 0

    for item in cart_items:
        product = Product.query.get(item.product_id)
        item_total = product.price * item.quantity
        cart_details.append({
            "product_id": item.product_id,
            "product_name": product.name,
            "price_per_unit": product.price,
            "quantity": item.quantity,
            "item_total": item_total
        })
        total_price += item_total

    return render_template('cart.html', cart_items=cart_details, total_price=total_price)

@main.route('/add-to-cart', methods=['GET', 'POST'])
@login_required
def add_to_cart_page():
    """
    Renders a form for users to add a product to their cart.
    On a POST request, processes the form to add the specified product and quantity.
    """
    if request.method == 'POST':
        # Get form data
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity', 1)
        
        # Convert quantity to integer, and handle potential conversion error
        try:
            quantity = int(quantity)
        except ValueError:
            flash("Invalid quantity. Please enter a number.", 'danger')
            return redirect(url_for('main.add_to_cart_page'))

        # Validate product ID
        product = Product.query.get(product_id)
        if not product:
            flash('Product not found', 'danger')
            return redirect(url_for('main.add_to_cart_page'))

        # Add or update item in the cart
        cart_item = ShoppingCart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity  # Update quantity if item exists
        else:
            cart_item = ShoppingCart(user_id=current_user.id, product_id=product_id, quantity=quantity)
            db.session.add(cart_item)  # Add new item if not in cart
        
        # Commit changes to the database
        db.session.commit()
        flash('Item added to cart!', 'success')
        return redirect(url_for('main.view_cart'))

    # Render the add-to-cart form if request method is GET
    return render_template('add_to_cart.html')