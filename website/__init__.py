from flask import Flask
from flask_mysqldb import MySQL

db = MySQL()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'wooooa, secret'

    # mysql connection config
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '123'
    app.config['MYSQL_DB'] = 'DB'
    db.init_app(app)

    # import blueprints
    from .views import views
    from .auth import auth
    # registering blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app