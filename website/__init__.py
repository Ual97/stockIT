from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_login  import LoginManager 
from flask_mail import Mail 
 
mail = Mail() 
db = SQLAlchemy() 
DB_NAME = 'stockITdb' 

def create_app():

    app = Flask(__name__) 
    app.config['SECRET_KEY'] = 'bxf1))xff;[xd9@#xcbxe2N$xc2!' 
    app.config['UPLOAD_FOLDER'] = 'files' 

    # sqlalchemy connection config 

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:12345678@localhost/{DB_NAME}' 
    db.init_app(app) 

    # import blueprints 

    from .views import views 
    from .routes.user import usr 
    from .routes.movements import movements
    from .routes.product import product
    from .routes.branch import subsidiary
    from .routes.inventory import inventory 
    from .routes.csv import csv_v

    # registering blueprints 

    app.register_blueprint(views, url_prefix='/') 
    app.register_blueprint(usr, url_prefix='/') 
    app.register_blueprint(movements, url_prefix='/')
    app.register_blueprint(product, url_prefix='/')
    app.register_blueprint(subsidiary, url_prefix='/') 
    app.register_blueprint(csv_v, url_prefix='/')
    app.register_blueprint(inventory, url_prefix='/')

    # create tables from models 

    db.create_all(app=app) 

    # initializing mail sending 

    app.config['MAIL_SERVER']='smtp.sl4.tech' 
    app.config['MAIL_PORT'] = 25 
    app.config['MAIL_USERNAME'] = 'admin@sl4.tech' 
    app.config['MAIL_PASSWORD'] = 'csvp#(X2'

    # app.config['MAIL_USE_TLS'] = True 

    # app.config['MAIL_USE_SSL'] = False 

    mail.init_app(app) 
    login_manager = LoginManager() 
    login_manager.login_view = 'usr.login' 
    login_manager.init_app(app) 

    from .models.user import User 
    @login_manager.user_loader #how the users are loaded 
    def load_user(id): 

        return User.query.get(id) 

    return app 