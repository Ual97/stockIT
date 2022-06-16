from website import db
import datetime

class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # all products have an owner (user)
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    name = db.Column(db.String(124))
    branch = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    cost = db.Column(db.Integer)
    price = db.Column(db.Integer)
    expiry = db.Column(db.Date)
    qr_barcode = db.Column(db.String(24))

    def __init__(self, **kwargs):
        """initialize obj products"""
        self.prod_id = kwargs.get('prod_id')
        self.date = datetime.datetime.now()
        self.name = kwargs.get('name')
        self.branch = kwargs.get('branch')
        self.quantity = kwargs.get('quantity')
        self.cost = kwargs.get('cost')
        self.price = kwargs.get('price')
        self.expiry = kwargs.get('expiry')
        self.qr_barcode = kwargs.get('qr_barcode')

