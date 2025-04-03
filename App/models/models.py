from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# -----------------------
# User model
# -----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    ingredients = db.relationship('UserIngredient', backref='user', lazy=True)
    recipes = db.relationship('Recipe', backref='user', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def missing_ingredients_for(self, recipe):
        # Compares user inventory vs recipe requirements
        owned = {item.name.lower() for item in self.ingredients}
        required = {ri.name.lower() for ri in recipe.ingredients}
        return required - owned
    
    def initialize_default_user():
     existing = User.query.filter_by(username="bob").first()
     if not existing:
        bob = User(username="bob", email="bob@mail.com", password="bobpass")
        db.session.add(bob)
        db.session.commit()
        print("✅ User 'bob' created.")
     else:
        print("🟢 User 'bob' already exists.")


    def __repr__(self):
        return f'<User {self.username}>'

# -----------------------
# Ingredient the user owns
# -----------------------
class UserIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String(20), nullable=True)

    def __init__(self, user_id, name, quantity=None, unit=None):
        self.user_id = user_id
        self.name = name.lower()
        self.quantity = quantity
        self.unit = unit

    def __repr__(self):
        return f'<Inventory: {self.name} ({self.quantity} {self.unit})>'

# -----------------------
# Recipe model
# -----------------------
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text)
    category = db.Column(db.String(50))

    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True)

    def __init__(self, user_id, title, instructions, category=None):
        self.user_id = user_id
        self.title = title
        self.instructions = instructions
        self.category = category or "Uncategorized"

    def __repr__(self):
        return f'<Recipe: {self.title}>'

# -----------------------
# Ingredient used in a recipe
# -----------------------
class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String(20), nullable=True)

    def __init__(self, recipe_id, name, quantity=None, unit=None):
        self.recipe_id = recipe_id
        self.name = name.lower()
        self.quantity = quantity
        self.unit = unit

    def __repr__(self):
        return f'<RecipeIngredient: {self.name} ({self.quantity} {self.unit})>'

def initialize_default_user():
    from App.models.models import db, User  # local import to avoid circular issues

    existing = User.query.filter_by(username="bob").first()
    if not existing:
        bob = User(username="bob", email="bob@mail.com", password="bobpass")
        db.session.add(bob)
        db.session.commit()
        print("✅ User 'bob' created.")
    else:
        print("🟢 User 'bob' already exists.")
