from App.app import app
from App.models.models import db, initialize_default_user

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        initialize_default_user()
    app.run(debug=True)
