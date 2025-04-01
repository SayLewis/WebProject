from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    ingredients = db.relationship('Ingredient', backref='user', lazy=True)
    recipes = db.relationship('Recipe', backref='user', lazy=True)

# Ingredient model (user’s inventory)
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String(20), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Recipe model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True)

# RecipeIngredient model (linked to a recipe)
class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String(20), nullable=True)

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

# Function to create Bob by default
def create_default_bob():
    bob = User.query.filter_by(username='bob').first()
    if not bob:
        bob_user = User(
            username='bob',
            email='bob@example.com',
            password=generate_password_hash('bobpass')
        )
        db.session.add(bob_user)
        db.session.commit()

# Function to initialize DB and create Bob
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        create_default_bob()
