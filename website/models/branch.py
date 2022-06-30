from website import db
from uuid import uuid4

class Branch(db.Model):
    id = db.Column(db.String(64), nullable=False, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    # all sucursales have an owner (user)
    owner = db.Column(db.String(150), db.ForeignKey('user.email'))

    def __init__(self, **kwargs):
        """initialize obj sucursales"""
        self.id = str(uuid4())
        self.name = kwargs.get('name')
        self.owner = kwargs.get('owner')