
QuickShop: Your One-Stop Online Shopping Experience
Project Overview
QuickShop is an e-commerce platform built with Python’s Flask framework, designed to offer a streamlined shopping experience with essential e-commerce functionality. This Minimum Viable Product (MVP) includes product browsing, user authentication, shopping cart management, and a secure checkout process. Future versions will build upon this foundation to add more advanced features and scalability.

Table of Contents
Features
Tech Stack
Learning Objectives
Project Structure
Setup Instructions
Schedule and Milestones
Challenges Faced
Future Improvements
Features
Product Browsing: View a variety of products with sorting and pagination.
User Registration and Login: Secure account creation and login with session management.
Shopping Cart: Add, update, or remove items and view total price.
Order Checkout: Secure checkout with payment integration using Stripe.
Order Confirmation: Receive order confirmation via email after purchase.
Tech Stack
Frontend: HTML, CSS, JavaScript (Bootstrap for UI components)
Backend: Python, Flask (micro-framework)
Database: MySQL for managing product, user, and order data
Templating Engine: Jinja2 for dynamic HTML rendering
Hosting: AWS EC2 for the app, AWS RDS or ClearDB for the MySQL database
Third-Party Integrations:
Payment Gateway: Stripe for handling secure payments
Email Service: SendGrid for email notifications
Asset Storage: AWS S3 for managing product images and other assets
Learning Objectives
Develop Web Applications: Build a functional app with Flask.
Implement Secure Authentication: Manage user sessions and authentication flows.
Database Integration: Structure and interact with MySQL databases effectively.
API and Payment Integration: Integrate external services such as Stripe and SendGrid.
Responsive Design: Create a responsive layout for an optimal experience across devices.
Project Structure
csharp
Copy code
QuickShop/
├── app/
│   ├── static/         # Static files (CSS, JS, images)
│   ├── templates/      # HTML templates
│   ├── routes/         # Route handlers
│   ├── models/         # Database models
│   ├── forms/          # Form validation
│   └── utils/          # Utility functions
├── migrations/         # Database migrations
├── tests/              # Test cases
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
└── README.md           # Project README
Setup Instructions
Clone the Repository:

bash
Copy code
git clone https://github.com/CeciliaMutero/quick-shop.git
cd QuickShop
Set up a Virtual Environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
Install Requirements:

bash
Copy code
pip install -r requirements.txt
Set up the Database:

Ensure MySQL is installed and running.
Create a MySQL database:
sql
Copy code
CREATE DATABASE quickshop_db;
Update config.py with your MySQL credentials.
Run Migrations:

bash
Copy code
flask db upgrade
Set up Environment Variables:

Create a .env file and add keys for Stripe, SendGrid, and other sensitive information.
Run the Application:

bash
Copy code
flask run
Access the app at http://127.0.0.1:5000.

Schedule and Milestones
Week 1
Project Setup: Initialize Flask structure, database, and GitHub repo.
User Authentication: Implement user registration, login, and session management.
Product Pages: Create product listing and detail views, with MySQL integration.
Week 2
Shopping Cart: Build functionality to add items to the cart, update quantities, and view the cart.
Checkout & Payments: Implement a checkout page and integrate Stripe.
Order Confirmation & Testing: Finalize email confirmation and conduct full app testing.
Deployment: Deploy on chosen hosting service, configure database, and finalize production settings.
Challenges Faced
Time Constraints: Limited development time required strict prioritization and task management.
Database Integration: Designing a robust schema for handling products, users, and orders.
Secure Payments: Implementing a seamless and secure payment flow using Stripe.
Responsive Design: Ensuring the application is optimized for both desktop and mobile experiences.
Future Improvements
Wishlist and Order History: Allow users to save products for later and view past orders.
Enhanced Product Filtering: Add advanced filters for product categories, price ranges, etc.
Admin Dashboard: Create an admin interface for managing products, orders, and user accounts.
User Reviews: Enable product ratings and reviews from authenticated users.
