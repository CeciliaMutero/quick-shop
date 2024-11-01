from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.forms import RegistrationForm, LoginForm, AddToCartForm
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
    # Fetch all products without filtering by 'is_featured'
    products = Product.query.limit(5).all()  # Adjust limit as needed
    return render_template('home.html', products=products)


@main.route('/about')
def about():
    """About page route for the application."""
    return render_template('about.html')

# Contact Us route
@main.route('/contact')
def contact():
    """Render the Contact Us page."""
    return render_template('contact.html')


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
    sort_by = request.args.get('sort', 'name')
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)

    # Filtering products based on search query
    products_query = Product.query
    if search_query:
        products_query = products_query.filter(Product.name.ilike(f'%{search_query}%'))

    # Sorting products
    if sort_by == 'name':
        products_query = products_query.order_by(Product.name.asc())
    elif sort_by == 'price':
        products_query = products_query.order_by(Product.price.asc())
    else:
        products_query = products_query

    # Paginate results
    products = products_query.paginate(page=page, per_page=10)
    return render_template('product_list.html', products=products, sort_by=sort_by, search_query=search_query)


# Product detail route - view details of a specific product
from flask import render_template, request
from .forms import AddToCartForm  # Adjust this import based on your structure
from app.models.product import Product  # Import your Product model

@main.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    """
    Render the product detail page for a specific product and handle
    the addition of the product to the shopping cart.

    Parameters:
    product_id (int): The ID of the product to display.

    Returns:
    render_template: Renders the 'product_detail.html' template
    with the product information and the add-to-cart form. If the
    form is submitted and valid, it adds the product to the cart.

    This route handles both GET and POST requests. On a GET request,
    it displays the product details along with a form for adding
    the product to the cart. On a POST request, it processes the form
    submission to add the specified quantity of the product to the cart.
    """
    
    product = Product.query.get_or_404(product_id)  # Fetch the product or return a 404 if not found
    form = AddToCartForm()  # Create an instance of your form
    
    if form.validate_on_submit():
        # Handle the form submission, e.g., add the product to the cart
        product_id = form.product_id.data
        quantity = form.quantity.data
        # Add logic to add the product to the cart
        # Redirect or render a success message, etc.

    return render_template('product_detail.html', product=product, form=form)  # Pass the form to the template


@main.route('/products/search', methods=['GET'])
def search_products():
    query = request.args.get('query', '')
    products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    return render_template('product_list.html', products=products, query=query)

@main.route('/products/category/<int:category_id>')
def products_by_category(category_id):
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template('product_list.html', products=products)


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

@main.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    """
    Route to update the quantity of an item in the shopping cart.

    Parameters:
    item_id (int): The ID of the shopping cart item to update.

    Returns:
    Redirect to the cart view with success or error message.
    """
    quantity = request.form.get('quantity', type=int)

    # Find the cart item by the item_id
    cart_item = ShoppingCart.query.filter_by(user_id=current_user.id, id=item_id).first()

    if cart_item:
        if quantity is not None and quantity > 0:
            cart_item.quantity = quantity  # Update the quantity
            db.session.commit()
            flash('Cart updated successfully!', 'success')
        else:
            flash('Invalid quantity. Please enter a valid number.', 'danger')
    else:
        flash('Item not found in cart.', 'danger')

    return redirect(url_for('main.view_cart'))  # Redirect back to the cart view


@main.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        # Get shipping details from the form
        shipping_address = request.form.get('shipping_address')
        # Redirect to payment if all information is provided
        return redirect(url_for('main.payment'))
    return render_template('checkout.html')
