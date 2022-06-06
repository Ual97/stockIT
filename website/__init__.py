from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login  import LoginManager
from flask_cors import CORS

db = SQLAlchemy()
DB_NAME = 'DB'

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'wooooa, secret'
    #CORS(app)


    # sqlalchemy connection config
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:12345678@localhost/{DB_NAME}'
    db.init_app(app)

    # import blueprints
    from .views import views
    from .routes.user import usr
    from .routes.product import inventory
    from .routes.sucursal import subsidiary
    # registering blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(usr, url_prefix='/')
    app.register_blueprint(inventory, url_prefix='/')
    app.register_blueprint(subsidiary, url_prefix='/')

    # create tables from models
    from .models.user import User
    
    db.create_all(app=app)

    login_manager = LoginManager()
    login_manager.login_view = 'usr.login'
    login_manager.init_app(app)

    @login_manager.user_loader #how the users are loaded
    def load_user(id):
        return User.query.get(id)

    return app