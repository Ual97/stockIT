from website import db


class Product(db.Model):
    owner = db.Column(db.String(124), db.ForeignKey('user.email'))
    name = db.Column(db.String(124))
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(150), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, db.ForeignKey('product.cost'))
    price = db.Column(db.Integer, db.ForeignKey('product.price'))
    expiry = db.Column(db.Date)
    qr_barcode = db.Column(db.String(24))

    def __init__(self, **kwargs):
        """initialize obj products"""
        self.owner = kwargs.get('owner')
        self.name = kwargs.get('name')
        self.branch = kwargs.get('branch')
        self.quantity = kwargs.get('quantity')
        self.cost = kwargs.get('cost')
        self.price = kwargs.get('price')
        self.expiry = kwargs.get('expiry')
        self.qr_barcode = kwargs.get('qr_barcode')
