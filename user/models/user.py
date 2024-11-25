from models import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=False, nullable=False)
    last_name = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), unique=False, nullable=False)
    role = db.Column(db.String(200), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'