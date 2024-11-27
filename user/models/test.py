from models import db

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_ticket = db.Column(db.String(255), unique=False, nullable=True)
    test_description = db.Column(db.String(255), unique=False, nullable=True)
    test_executed_by = db.Column(db.String(255), unique=False, nullable=True)
    test_report_file = db.Column(db.String(255), unique=False, nullable=True)
    def __repr__(self):
        return f'<User {self.email}>'