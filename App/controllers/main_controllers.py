from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import create_access_token, jwt_required, set_access_cookies, unset_jwt_cookies, current_user
from App.models.models import db, User, Recipe, UserIngredient

bp = Blueprint("main_routes", __name__)

# -----------------------
# Page Routes
# -----------------------

@bp.route("/", methods=["GET"])
def login_page():
    return render_template("login.html")

@bp.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")

@bp.route("/home")
@jwt_required()
def home():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    inventory = UserIngredient.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", recipes=recipes, inventory=inventory)

# -----------------------
# Auth Routes
# -----------------------

@bp.route("/login", methods=["POST"])
def login_action():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        token = create_access_token(identity=str(user.id))  # ✅ serialize by ID
        response = redirect(url_for("main_routes.home"))
        set_access_cookies(response, token)
        flash("Login successful")
        return response
    else:
        flash("Invalid username or password")
        return redirect(url_for("main_routes.login_page"))

@bp.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    response = redirect(url_for("main_routes.login_page"))
    unset_jwt_cookies(response)
    flash("You have been logged out.")
    return response
