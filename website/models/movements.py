from website import db
import datetime
from uuid import uuid4


class Movements(db.Model):
    id = db.Column(db.String(64), nullable=False, primary_key=True)
    # all products have an owner (user)
    owner = db.Column(db.String(124), db.ForeignKey('user.email'))
    prod_id = db.Column(db.String(64), db.ForeignKey('product.id'))
    branch_id = db.Column(db.String(64), db.ForeignKey('branch.id'))
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime)
    in_out = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        """initialize obj products"""
        self.id = str(uuid4())
        self.owner = kwargs.get('owner')
        self.prod_id = kwargs.get('prod_id')
        self.quantity = kwargs.get('quantity')
        if kwargs.get('date') in ['', None]:
            self.date = datetime.datetime.now()
        else:
            self.date = kwargs.get('date')
        self.branch_id = kwargs.get('branch_id')
        self.in_out = kwargs.get('in_out')