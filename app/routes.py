from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User, Product, Order, OrderItem
from app import login_manager
import os
import secrets
from app.utils import send_order_confirmation, send_password_reset_email
from app.utils import send_password_reset_email, send_reset_email
from app.utils import generate_reset_token, verify_reset_token, send_reset_email
from app.utils import send_reset_email  # Create a utility function to send emails
from itsdangerous import URLSafeTimedSerializer



main = Blueprint('main', __name__)



@login_manager.user_loader
def load_user(user_id):
    # yahaan par aapko apne user model ko query karna hai
    # aur user object ko return karna hai
    return User.query.get(int(user_id))
    
@main.route("/")
def home():
    products = Product.query.all()
    return render_template("customer/home.html", products=products)

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = bcrypt.generate_password_hash(request.form["password"]).decode('utf-8')
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for('main.login'))
    return render_template("auth/register.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.home'))
        flash("Invalid credentials", "danger")
    return render_template("auth/login.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))
    
    
@main.route("/vendor/dashboard")
@login_required
def vendor_dashboard():
    if current_user.role != "vendor":
        flash("Access Denied!", "danger")
        return redirect(url_for('main.home'))
    
    products = Product.query.filter_by(user_id=current_user.id).all()
    return render_template("vendor/dashboard.html", products=products)

@main.route("/vendor/add_product", methods=["GET", "POST"])
@login_required
def add_product():
    if current_user.role != "vendor":
        return redirect(url_for('main.home'))
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = float(request.form["price"])
        stock = int(request.form["stock"])
        category = request.form["category"]
        image = request.files["image"]
        product = Product(name=name, description=description, price=price, stock=stock, category=category, image=image.filename, user_id=current_user.id)
        db.session.add(product)
        db.session.commit()
        image.save(os.path.join(current_app.config["UPLOAD_FOLDER"], image.filename))
        flash("Product added successfully!", "success")
        return redirect(url_for('main.vendor_dashboard'))
    return render_template("vendor/add_product.html")
    
cart = {}

@main.route("/cart")
@login_required
def view_cart():
    return render_template("customer/cart.html", cart=cart)


@main.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):
    if not current_user.is_authenticated:
        flash("Please login first", "danger")
        return redirect(url_for('main.login'))
    product = Product.query.get(product_id)
    if product:
        if product_id in cart:
            cart[product_id]['quantity'] += 1
        else:
            cart[product_id] = {'name': product.name, 'price': product.price, 'quantity': 1}
    return redirect(url_for('main.view_cart'))

@main.route("/checkout", methods=["GET", "POST"])
def checkout():
    if not current_user.is_authenticated:
        flash("Please login first", "danger")
        return redirect(url_for('main.login'))

    if request.method == "POST":
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())
        order = Order(user_id=current_user.id, total_price=total_price)
        db.session.add(order)
        db.session.commit()

        # Prepare order details for email
        order_summary = f"Order ID: {order.id}\nTotal Price: ${total_price:.2f}\nItems:\n"
        for item in cart.values():
            order_summary += f"- {item['name']} (x{item['quantity']}): ${item['price'] * item['quantity']:.2f}\n"

        # Send confirmation email
        send_order_confirmation(current_user.email, order_summary)

        cart.clear()
        flash("Order placed successfully! A confirmation email has been sent.", "success")
        return redirect(url_for('main.order_history'))

    return render_template("customer/checkout.html", cart=cart)

    
@main.route("/orders")
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template("customer/orders.html", orders=orders)
    
@main.route("/admin/dashboard")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return redirect(url_for('main.home'))
    
    users = User.query.all()
    orders = Order.query.all()
    return render_template("admin/dashboard.html", users=users, orders=orders)

@main.route("/admin/manage_orders")
@login_required
def manage_orders():
    if current_user.role != "admin":
        return redirect(url_for('main.home'))
    
    orders = Order.query.all()
    return render_template("admin/manage_orders.html", orders=orders)

@main.route("/admin/update_order/<int:order_id>/<string:status>")
@login_required
def update_order(order_id, status):
    if current_user.role != "admin":
        return redirect(url_for('main.home'))

    order = Order.query.get(order_id)
    if order:
        order.status = status
        db.session.commit()
        flash(f"Order updated to {status}!", "success")
    return redirect(url_for('main.manage_orders'))
    
    
    
@main.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    if current_user.role != "vendor":
        flash("Access Denied!", "danger")
        return redirect(url_for('main.home'))
    
    product = Product.query.get(product_id)
    if product is None:
        flash("Product not found!", "danger")
        return redirect(url_for('main.vendor_dashboard'))
    
    if product.user_id != current_user.id:
        flash("You are not authorized to edit this product!", "danger")
        return redirect(url_for('main.vendor_dashboard'))
    
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        price = float(request.form["price"])
        stock = int(request.form["stock"])
        category = request.form["category"]
        
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        product.category = category
        
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('main.vendor_dashboard'))
    
    return render_template("vendor/edit_product.html", product=product)

@main.route("/delete_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def delete_product(product_id):
    if current_user.role != "vendor":
        flash("Access Denied!", "danger")
        return redirect(url_for('main.home'))
    
    product = Product.query.get(product_id)
    if product is None:
        flash("Product not found!", "danger")
        return redirect(url_for('main.vendor_dashboard'))
    
    if product.user_id != current_user.id:
        flash("You are not authorized to delete this product!", "danger")
        return redirect(url_for('main.vendor_dashboard'))
    
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for('main.vendor_dashboard'))



@main.route("/reset-password", methods=["GET", "POST"])
def reset_password_request():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_reset_token(user.email)
            send_reset_email(user.email, token)
            flash("Password reset link has been sent to your email.", "info")
        else:
            flash("No account found with this email.", "danger")
        return redirect(url_for("main.login"))
    return render_template("auth/reset_password_request.html")
    
    
    
@main.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash("Invalid or expired token!", "danger")
        return redirect(url_for("main.reset_password_request"))
    user = User.query.filter_by(email=email).first()
    if request.method == "POST":
        new_password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if new_password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("main.reset_password", token=token))
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        db.session.commit()
        flash("Password updated successfully! Please log in.", "success")
        return redirect(url_for("main.login"))
    return render_template("auth/reset_password.html")
    
    
    
    