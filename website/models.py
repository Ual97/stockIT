from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """ model for user in database """
    email = db.Column(db.String(150), primary_key=True)
    password = db.Column(db.String(150))
    usrname = db.Column(db.String(150))
    # stores a list of the user's products
    products = db.relationship('Product')
    # stores a list of the user's sucursales
    products = db.relationship('Sucursal')

    def get_id(self):
        return self.email

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # all products have an owner (user)
    owner = db.Column(db.String(150), db.ForeignKey('user.email'))
    name = db.Column(db.String(150), nullable=False)
    sucursal = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer)
    price = db.Column(db.Integer)
    expiry = db.Column(db.Date)
    qty_reserved = db.Column(db.Integer)
    qr_barcode = db.Column(db.Integer)

class Sucursal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    # all sucursales have an owner (user)
    owner = db.Column(db.String(150), db.ForeignKey('user.email'))