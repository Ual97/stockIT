from website import db


class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    # all sucursales have an owner (user)
    owner = db.Column(db.String(150), db.ForeignKey('user.email'))

    def __init__(self, **kwargs):
        """initialize obj sucursales"""
        self.name = kwargs.get('name')
        self.owner = kwargs.get('owner')