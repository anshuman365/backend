from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_user, logout_user
from models import db, Student

student_bp = Blueprint("student", __name__)

@student_bp.route("/login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        email = request.form["email"]
        student = Student.query.filter_by(email=email).first()
        if student:
            login_user(student)
            return redirect(url_for("student.wait_page"))
    return render_template("student_login.html")

@student_bp.route("/wait")
def wait_page():
    return render_template("wait.html")

@student_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("student.student_login"))
