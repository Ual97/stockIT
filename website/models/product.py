from website import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # all products have an owner (user)
    owner = db.Column(db.String(150), db.ForeignKey('user.email'))
    name = db.Column(db.String(150), nullable=False)
    branch = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer)
    price = db.Column(db.Integer)
    expiry = db.Column(db.Date)
    qty_reserved = db.Column(db.Integer)
    qr_barcode = db.Column(db.Integer)

    def __init__(self, **kwargs):
        """initialize obj products"""
        self.owner = kwargs.get('owner')
        self.name = kwargs.get('name')
        self.branch = kwargs.get('branch')
        self.quantity = kwargs.get('quantity')
        self.cost = kwargs.get('cost')
        self.price = kwargs.get('price')
        self.expiry = kwargs.get('expiry')
        self.qty_reserved = kwargs.get('qty_reserved')
        self.qr_barcode = kwargs.get('qr_barcode')

