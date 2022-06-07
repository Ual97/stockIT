from website import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """ model for user in database """
    email = db.Column(db.String(150), primary_key=True)
    password = db.Column(db.String(150))
    usrname = db.Column(db.String(150))
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    # stores a list of the user's products
    products = db.relationship('Product')
    # stores a list of the user's sucursales
    products = db.relationship('Sucursal')

    def __init__(self, **kwargs):
        """initialize user objs"""
        self.email = kwargs.get('email')
        self.password = kwargs.get('password1')
        self.usrname = kwargs.get('usrname')

    def get_id(self):
        return self.email