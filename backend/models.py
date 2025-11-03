# backend/models.py
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy instance (not yet tied to app)
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(120), nullable=False)
    lname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    confirmPassword = db.Column(db.String(300), nullable=False)
    registered = db.Column(db.Boolean, default=False) 

    def __repr__(self):
        return f"<User {self.email}>"
