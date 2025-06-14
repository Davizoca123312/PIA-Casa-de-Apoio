import os
from flask import Flask
from app.routes.main_routes import main_routes
from app.routes.admin_routes import admin_routes
from app.models.user_model import db
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ['SECRET_KEY']  # Agora obrigatório

db.init_app(app)
app.register_blueprint(main_routes)
app.register_blueprint(admin_routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)