from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app import db
from app.forms import RegistrationForm, LoginForm
from app.models.user import User

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
        # Create a new user instance
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)  # Make sure to hash the password
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
        if user and user.password == form.password.data:  # Check if user exists and password matches
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