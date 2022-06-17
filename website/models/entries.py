from website import db
import datetime

class Movements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # all products have an owner (user)
    owner = db.Column(db.String(124), db.ForeignKey('user.email'))
    prod_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime)
    in_out = db.Column(db.Boolean)
    
    def __init__(self, **kwargs):
        """initialize obj products"""
        self.owner = kwargs.get('owner')
        self.prod_id = kwargs.get('prod_id')
        self.name = kwargs.get('name')
        self.quantity = kwargs.get('quantity')
        self.date = datetime.datetime.now()
        self.branch_id = kwargs.get('branch_id')
        self.in_out = kwargs.get('in_out')