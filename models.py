from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class register(db.Model):
    __tablename__="register"
    id=db.Column(db.Integer, primary_key=True)
    Name=db.Column(db.String(16), nullable=False)
    Username=db.Column(db.String(16), nullable=False)
    Email=db.Column(db.String(16), nullable=False)
    Password=db.Column(db.String(16), nullable=False)
