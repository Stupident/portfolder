from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .config import secret_key

db = SQLAlchemy()
DB_NAME = "portfolder.db"
basedir = path.abspath(path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, DB_NAME)

    db.init_app(app)

    from .views import views, page_not_found
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    app.register_error_handler(404, page_not_found)

    from .models import User

    create_database(app)

    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists(path.join(basedir, DB_NAME)):
        with app.app_context():
            db.create_all()
        print('Created database')
