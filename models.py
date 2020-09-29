from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(30), nullable=False)
    Username = db.Column(db.String(16), nullable=False)
    Email = db.Column(db.String(60), nullable=False)
    Password = db.Column(db.String(16), nullable=False)
    Time_registered = db.Column(db.DateTime, nullable=False)


class books(db.Model):
    __tablename__ = "Books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)


class review(db.Model):
    __tablename__ = "reviews"
    isbn = db.Column(db.String, nullable=False, primary_key=True)
    title = db.Column(db.String, nullable=False)
    rating = db.Column(db.String, nullable=False)
    review = db.Column(db.String, nullable=False)
    time_stamp = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, primary_key=True)
