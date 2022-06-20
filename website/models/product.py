from website import db
from uuid import uuid4


class Product(db.Model):
    id = db.Column(db.String(64), nullable=False, primary_key=True)
    # all products have an owner (user)
    owner = db.Column(db.String(124), db.ForeignKey('user.email'))
    name = db.Column(db.String(124))
    qr_barcode = db.Column(db.String(24))
    description = db.Column(db.String(256))

    def __init__(self, **kwargs):
        """initialize obj products"""
        self.id = str(uuid4())
        self.owner = kwargs.get('owner')
        self.name = kwargs.get('name')
        self.qr_barcode = kwargs.get('qr_barcode')
        self.description = kwargs.get('description')