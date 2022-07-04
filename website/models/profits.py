from website import db
from uuid import uuid4

class Profits(db.Model):
    id = db.Column(db.String(64), nullable=False, primary_key=True)
    # all profits has owner (user)
    owner = db.Column(db.String(124), db.ForeignKey('user.email'))
    prod_id = db.Column(db.String(64), db.ForeignKey('product.id'))
    profit = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    branch_id = db.Column(db.String(64), db.ForeignKey('branch.id'))
    currency = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        """initialize obj Profits"""
        self.id = str(uuid4())
        self.owner = kwargs.get('owner')
        self.prod_id = kwargs.get('prod_id')
        self.profit = kwargs.get('profit')
        self.date = kwargs.get('date')
        self.quantity = kwargs.get('quantity')
        self.branch_id = kwargs.get('branch_id')
        self.currency = kwargs.get('currency')