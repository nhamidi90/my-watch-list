import os
from flask import (
    Flask, flash, render_template, 
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
	import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_shows")
def get_shows():
    shows = mongo.db.shows.find()
    return render_template("shows.html", shows=shows)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.user.find_one(
            {"username": request.form.get("username").lower()})
        
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))


        register = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "confirm_password": generate_password_hash(request.form.get("confirm_password"))
        }
        
        password1 = request.form.get("password")
        password2 = request.form.get("confirm_password")

        if password1 != password2:
            flash("Passwords do not match. Please try again")
        else: mongo.db.user.insert_one(register), flash("Registration successful")
        
        session["user"] = request.form.get("email")

    return render_template("register.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        existing_user = mongo.db.user.find_one(
            {"email": request.form.get("email")})
        
        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("email")
                    return redirect(url_for("get_shows"))
            else:
                flash("Incorrect Username or Password")
                return redirect(url_for("sign_in"))

        else:
            flash("Incorrect Username or Password")
            return redirect(url_for("sign_in"))
    return render_template("sign-in.html")


if __name__ == "__main__":
    app.run(host = os.environ.get("IP"),
            port = int(os.environ.get("PORT")), 
            debug = True)
