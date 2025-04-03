from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies, jwt_required, current_user
from App.models.models import db, User, Recipe, UserIngredient, RecipeIngredient
from sqlalchemy.exc import IntegrityError

bp = Blueprint("main_routes", __name__)

@bp.route("/")
def login_page():
    return render_template("login.html")

@bp.route("/signup", methods=["GET", "POST"])
def signup_page():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        try:
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            token = create_access_token(identity=user)
            response = redirect(url_for("main_routes.home"))
            set_access_cookies(response, token)
            return response
        except IntegrityError:
            db.session.rollback()
            flash("Username or email exists already.")
            return redirect(url_for("main_routes.signup_page"))
    return render_template("signup.html")

@bp.route("/login", methods=["POST"])
def login_action():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=user)
        response = redirect(url_for("main_routes.home"))
        set_access_cookies(response, token)
        return response
    else:
        flash("Invalid credentials")
        return redirect(url_for("main_routes.login_page"))

@bp.route("/logout")
@jwt_required()
def logout_action():
    response = redirect(url_for("main_routes.login_page"))
    unset_jwt_cookies(response)
    return response

@bp.route("/home")
@jwt_required()
def home():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    inventory = UserIngredient.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", recipes=recipes, inventory=inventory)
