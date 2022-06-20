from website import db
from uuid import uuid4


class Inventory(db.Model):
    """Inventory model"""
    id = db.Column(db.String(64), nullable=False, primary_key=True)
    # all products have an owner (user)
    owner = db.Column(db.String(124), db.ForeignKey('user.email'))
    prod_id = db.Column(db.String(64), db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        """initialize obj products"""
        self.id = str(uuid4())
        self.owner = kwargs.get('owner')
        self.prod_id = kwargs.get('prod_id')
        self.branch_id = kwargs.get('branch_id')
        self.quantity = kwargs.get('quantity')