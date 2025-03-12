from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from models import db, Admin

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        admin = Admin.query.filter_by(username=username).first()
        if admin:
            login_user(admin)
            return redirect(url_for("admin.dashboard"))
    return render_template("admin_login.html")

@admin_bp.route("/dashboard")
def dashboard():
    return render_template("admin_dashboard.html")

@admin_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("admin.admin_login"))
