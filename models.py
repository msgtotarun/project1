from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class User(db.Model):
    __tablename__="User"
    id=db.Column(db.Integer, primary_key=True)
    Name=db.Column(db.String(30), nullable=False)
    Username=db.Column(db.String(16), nullable=False)
    Email=db.Column(db.String(60), nullable=False)
    Password=db.Column(db.String(16), nullable=False)
    Time_registered=db.Column(db.DateTime, nullable=False )
