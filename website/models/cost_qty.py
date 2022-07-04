from website import db
from uuid import uuid4

class Cost_qty(db.Model):
    """this table is to calculate the general profits and to
       be able to calculate the profit per movement
    """
    id = db.Column(db.String(64), nullable=False, primary_key=True)
    owner = db.Column(db.String(150), db.ForeignKey('user.email'))
    prod_id = db.Column(db.String(64), db.ForeignKey('product.id'))
    branch_id = db.Column(db.String(64), db.ForeignKey('branch.id'))
    cost = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    qty_sold = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    sold = db.Column(db.Boolean, nullable=False)
    currency = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        """initialize cost_qty objs"""
        self.id = str(uuid4())
        self.owner = kwargs.get('owner')
        self.prod_id = kwargs.get('prod_id')
        self.branch_id = kwargs.get('branch_id')
        self.cost = kwargs.get('cost')
        self.quantity = kwargs.get('quantity')
        self.qty_sold = kwargs.get('qty_sold')
        self.date = kwargs.get('date')
        self.sold = kwargs.get('sold')
        self.currency = kwargs.get('currency')