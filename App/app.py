from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from App.models.models import db, User
from App.controllers.main_controllers import bp as main_routes

app = Flask(__name__)

# -----------------------
# Configuration
# -----------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cook_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-sauce'
app.config['JWT_SECRET_KEY'] = 'secret-cook-jwt'

app.config["JWT_TOKEN_LOCATION"] = ["cookies", "headers"]
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

# -----------------------
# Initialize Extensions
# -----------------------
db.init_app(app)
CORS(app)
jwt = JWTManager(app)

# -----------------------
# JWT Configuration
# -----------------------
@jwt.user_identity_loader
def user_identity_lookup(user_id):
    return user_id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)

# -----------------------
# Routes
# -----------------------
app.register_blueprint(main_routes)
