import os
import random
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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        coming_soon = {
            "title": request.form.get("title"),
            "image": request.form.get("img_url"),
            "year": request.form.get("year"),
            "videoLink": request.form.get("video-link"),
        }

        mongo.db.coming.insert_one(coming_soon)
        flash("Your drama was added successfully")
        return redirect(url_for("index"))
    all_shows = list(mongo.db.shows.find())

    filtered_shows = []

    for show in all_shows:
        if show.get('rating'):
            if show.get('rating') >= 7:
                filtered_shows.append(show)

    random.shuffle(filtered_shows)
    shows = filtered_shows[:10]

    watching_shows = []

    for show in all_shows:
        if show.get('status') == "Currently watching":
            watching_shows.append(show)

    random.shuffle(watching_shows)
    watching = watching_shows[:10]

    upcoming = list(mongo.db.coming.find())
    return render_template("index.html", shows=shows, upcoming=upcoming,
                           watching=watching)


@ app.route("/add_upcoming", methods=["GET", "POST"])
def add_upcoming():
    if request.method == "POST":
        upcoming_show = {
            "title": request.form.get("title"),
            "image": request.form.get("img_url"),
            "year": request.form.get("year"),
            "number_of_episodes": int(0),
            "status": request.form.get("status"),
            "episodes_watched": int(0),
            "rating": None,
            "notes": request.form.get("notes"),
            "created_by": session["user"]
        }
        mongo.db.shows.insert_one(upcoming_show)
        flash("Your drama was added successfully")
        return redirect(url_for("index"))


@app.route("/edit_upcoming/<coming_id>", methods=["GET", "POST"])
def edit_upcoming(coming_id):
    if request.method == "POST":
        rating_str = request.form.get("rating")

        rating = None if rating_str is None or rating_str == "null" else int(
            rating_str
        )
        drama = {
            "title": request.form.get("title"),
            "image": request.form.get("img_url"),
            "year": request.form.get("year"),
            "number_of_episodes": request.form.get("number_of_episodes"),
            "status": request.form.get("status"),
            "episodes_watched": request.form.get("episodes_watched"),
            "rating": rating,
            "notes": request.form.get("notes"),
            "created_by": session["user"]
        }
        upcoming = mongo.db.coming.replace_one(
            {"_id": ObjectId(coming_id)},
            drama
        )
        flash("Your drama was updated successfully")
        return redirect(url_for("index", upcoming=upcoming))


@app.route("/add_new_drama", methods=["GET", "POST"])
def add_new_drama():
    if request.method == "POST":
        rating_str = request.form.get("rating")
        rating = None if rating_str is None or rating_str == "null" else int(
            rating_str
        )
        new_drama = {
            "title": request.form.get("title"),
            "image": request.form.get("img_url"),
            "year": request.form.get("year"),
            "number_of_episodes": request.form.get("number_of_episodes"),
            "status": request.form.get("status"),
            "episodes_watched": request.form.get("episodes_watched"),
            "rating": rating,
            "notes": request.form.get("notes"),
            "created_by": session["user"]
        }
        mongo.db.shows.insert_one(new_drama)
        flash("Your drama was added successfully")
        return redirect(url_for("index"))


@app.route("/delete_upcoming/<coming_id>")
def delete_upcoming(coming_id):
    mongo.db.coming.delete_one({"_id": ObjectId(coming_id)})
    flash("Successfully deleted")
    return redirect(url_for("index"))


@app.route("/get_shows")
def get_shows():
    shows = list(mongo.db.shows.find())
    return render_template("shows.html", shows=shows)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    shows = list(mongo.db.shows.find({"$text": {"$search": query}}))
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
            "confirm_password": generate_password_hash(
                request.form.get("confirm_password")
            )
        }

        password1 = request.form.get("password")
        password2 = request.form.get("confirm_password")

        if password1 != password2:
            flash("Passwords do not match. Please try again")
        else:
            mongo.db.user.insert_one(register),
            flash("Registration successful! Welcome!")
        session["user"] = request.form.get("username")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        existing_user = mongo.db.user.find_one(
            {"email": request.form.get("email")})

        if existing_user:
            if check_password_hash(
                                  existing_user["password"], request.form.get(
                                    "password")):
                session['user'] = existing_user['username']
                return redirect(
                    url_for("index", username=session["user"])
                )
            else:
                flash("Incorrect Email or Password")
                return redirect(url_for("sign_in"))

        else:
            flash("Incorrect Email or Password")
            return redirect(url_for("sign_in"))
    return render_template("sign-in.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    shows = list(mongo.db.shows.find())
    username = mongo.db.user.find_one(
        {"username": session["user"]}
    )['username']
    email = mongo.db.user.find_one({"username": session["user"]})['email']
    password = mongo.db.user.find_one(
        {"username": session["user"]}
    )['password']

    if session["user"]:

        if request.method == "POST":
            existing_user = mongo.db.user.find_one(
                {"username": request.form.get("username").lower()})

            if existing_user:

                update_profile = {
                    "username": request.form.get("username").lower(),
                    "email": request.form.get("email"),
                    "password": generate_password_hash(
                        request.form.get("password")
                    ),
                    "confirm_password": generate_password_hash(
                        request.form.get("confirm_password")
                    )
                }

            password1 = request.form.get("password")
            password2 = request.form.get("confirm_password")

            if (password1 != password2):
                flash("Passwords do not match. Please try again")
            else:
                mongo.db.user.replace_one(
                    {"username": session["user"]},
                    update_profile
                ), flash("Profile updated")

        return render_template("profile.html", username=username, email=email,
                               password=password, shows=shows)

    return redirect(url_for('profile', username=username))


@app.route("/sign_out")
def sign_out():
    session.clear()
    return redirect(url_for("sign_in"))


@app.route("/delete_user")
def delete_user():
    mongo.db.user.delete_one({"username": session["user"]})
    session.clear()
    return redirect(url_for("register"))


@app.route("/add_drama", methods=["GET", "POST"])
def add_drama():
    if request.method == "POST":
        rating_str = request.form.get("rating")
        rating = None if rating_str is None or rating_str == "null" else int(
            rating_str
        )
        drama = {
            "title": request.form.get("title"),
            "image": request.form.get("img_url"),
            "year": request.form.get("year"),
            "number_of_episodes": request.form.get("number_of_episodes"),
            "status": request.form.get("status"),
            "episodes_watched": request.form.get("episodes_watched"),
            "rating": rating,
            "notes": request.form.get("notes"),
            "created_by": session["user"]
        }
        mongo.db.shows.insert_one(drama)
        flash("Your drama was added successfully")
        return redirect(url_for("get_shows"))
    status = list(mongo.db.status.find())
    return render_template("add_drama.html", status=status)


@app.route("/edit_drama/<show_id>", methods=["GET", "POST"])
def edit_drama(show_id):
    if request.method == "POST":
        rating_str = request.form.get("rating")
        rating = None if rating_str is None or rating_str == "null" else int(
            rating_str
        )
        drama = {
            "title": request.form.get("title"),
            "image": request.form.get("img_url"),
            "year": request.form.get("year"),
            "number_of_episodes": request.form.get("number_of_episodes"),
            "status": request.form.get("status"),
            "episodes_watched": request.form.get("episodes_watched"),
            "rating": rating,
            "notes": request.form.get("notes"),
            "created_by": session["user"]
        }
        mongo.db.shows.replace_one({"_id": ObjectId(show_id)}, drama)
        flash("Your drama was updated successfully")
        return redirect(url_for("get_shows"))
    show = mongo.db.shows.find_one({"_id": ObjectId(show_id)})
    status = list(mongo.db.status.find())
    return render_template("edit_drama.html", show=show, status=status)


@app.route("/delete_drama/<show_id>")
def delete_drama(show_id):
    mongo.db.shows.delete_one({"_id": ObjectId(show_id)})
    flash("Drama deleted")
    return redirect(url_for("get_shows"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
