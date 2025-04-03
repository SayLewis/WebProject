from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from App.models.models import db
from App.controllers.main_controller import bp as main_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cook_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-sauce'
app.config['JWT_SECRET_KEY'] = 'secret-cook-jwt'
app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

db.init_app(app)
CORS(app)
JWTManager(app)

app.register_blueprint(main_routes)
