from flask import render_template, request, redirect, url_for
from app import app, db
from models import User

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        message = "Login successful!" if user else "Invalid username or password"
    return render_template("login.html", message=message)

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            message = "Username already exists"
        else:
            new_user = User(name=name, username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            message = "Registration successful!"

    return render_template("register.html", message=message)
