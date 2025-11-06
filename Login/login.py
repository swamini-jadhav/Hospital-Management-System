from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "HMS.sqlite3")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
db = SQLAlchemy(app)



# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

# Routes


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            message = "Login successful!"
        else:
            message = "Invalid username or password"

    return render_template("login.html", message=message)

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if user exists
        if User.query.filter_by(username=username).first():
            message = "Username already exists"
        else:
            # Create user
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            message = "Registration successful!"

    return render_template("register.html", message=message)


if __name__ == "__main__":
    # Create tables if DB does not exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)