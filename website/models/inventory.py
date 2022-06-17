from website import db


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124))
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    branch_id = db.Column(db.String(124), db.ForeignKey('branch.id'))
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer)
    price = db.Column(db.Integer)
    qr_barcode = db.Column(db.String(24))
    description = db.Column(db.String(124))
    qr_barcode = db.Column(db.String(24))

    def __init__(self, **kwargs):
        """initialize obj products"""
        self.name = kwargs.get('name')
        self.prod_id = kwargs.get('prod_id')
        self.branch_id = kwargs.get('branch_id')
        self.quantity = kwargs.get('quantity')
        self.cost = kwargs.get('cost')
        self.price = kwargs.get('price')
        self.description = kwargs.get('description')
        self.qr_barcode = kwargs.get('qr_barcode')