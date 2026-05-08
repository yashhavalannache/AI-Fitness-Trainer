from models import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    age = db.Column(db.Integer, nullable=False)

    height = db.Column(db.Float, nullable=False)

    weight = db.Column(db.Float, nullable=False)

    goal = db.Column(db.String(100), nullable=False)

    level = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(100), nullable=False)

    profile_pic = db.Column(db.String(200), default=None)

    def __repr__(self):
        return f'<User {self.name}>'