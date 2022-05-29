from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login  import LoginManager

db = SQLAlchemy()
DB_NAME = 'stockITdb'

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'wooooa, secret'

    # sqlalchemy connection config
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:123@localhost/{DB_NAME}'
    db.init_app(app)

    # import blueprints
    from .views import views
    from .auth import auth
    # registering blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # create tables from models
    from . import models    
    db.create_all(app=app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader #how the users are loaded
    def load_user(id):
        return models.User.query.get(id)

    return app