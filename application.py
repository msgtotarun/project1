import os
import csv
import time
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
import requests
import json
active = 'active'
data = []
app = Flask(__name__)
if __name__ == '__main__':
    app.run()

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

user = ''


@app.route("/")
def index():
    if 'Username' in session:
        user = session.get('Username')
        return redirect(url_for('userHome', user=user))
    return redirect(url_for('login'))


@app.route("/home/<user>")
def userHome(user):
    if 'Username' in session:
        return render_template('index.html', user=user)
    return redirect(url_for('login'))


@app.route("/register")
def register():
    if 'Username' in session:
        flash("user already exist", 'warning')
        return redirect(url_for('index'))
    return render_template('register.html', register=active)


@app.route("/login")
def login():
    if 'Username' in session:
        flash("user already exist", 'warning')
        return redirect(url_for('index'))
    return render_template('login.html', login=active)


@app.route("/admin/<user>")
def admin(user):
    id = db.query(User).filter_by(Username=user).first()
    if(id.id == 1):
        data = db.query(User).order_by(User.Time_registered)
        return render_template('admin.html', user=user, data=data.all())
    flash('please login with admin account', 'warning')
    return redirect(url_for('userHome', user=user))


@ app.route("/registration", methods=["POST"])
def registration():
    if 'Username' in session:
        rowName = ['Name', 'Username', 'Email',
                   'Password', 'RPassword', 'check']
        row = []
        for i in rowName:
            s = request.form.get(i)
            # print(s)
            if(s == None):
                flash("please fill all details", 'warning')
                return render_template('register.html', register=active)
            else:
                row.append(s)
        if(row[3] != row[4]):
            flash(" your password missmatch", 'warning')
            return render_template('register.html', register=active)
        Uname = db.query(User).filter_by(Username=row[1]).first()
        email = db.query(User).filter_by(Email=row[2]).first()
        print(Uname)
        if(Uname != None and Uname.Username == row[1]):
            flash('username already exist', 'warning')
            return render_template('register.html', register=active)
        elif(email != None and email.Email == row[2]):
            flash('Email already exist', 'warning')
            return render_template('register.html', register=active)

        user = User(Name=row[0], Username=row[1], Email=row[2],
                    Password=row[3], Time_registered=time.ctime(time.time()))
        try:
            db.add(user)
            db.commit()
            flash(f"HI {row[0]} account created sucessfully", 'success')
        except:
            # e = sys.exc_info()
            # print(e)
            flash("please fill all details or error occured", 'danger')
        finally:
            db.remove()
            db.close()
        return render_template('register.html', register=active)

    flash("user already exist", 'warning')
    return redirect(url_for('index'))


@ app.route("/logout")
def logout():
    session.pop('Username', None)
    return redirect(url_for('index'))


@ app.route("/loginNow", methods=["POST"])
def loginNow():
    rowName = ['Username', 'Password']
    row = []
    for i in rowName:
        s = request.form.get(i)
        # print(s)
        if(s == ''):
            flash("please fill all details", 'warning')
            return render_template('login.html', login=active)
        else:
            row.append(s)
    row.append(request.form.get('check'))
    # print(row)
    Username = db.query(User).filter_by(Username=row[0]).first()
    # print(Uname)
    # print(Uname.Password)
    # print(row[1])
    # print(Uname.Password == row[1])
    if(Username != None and Username.Password == row[1]):
        flash("login success", "success")
        session[rowName[0]] = row[0]
        return redirect(url_for('userHome', user=row[0]))
    else:
        flash("account does not exist register now", "danger")
        return redirect(url_for('register'))


@ app.route("/search/<user>", methods=["POST"])
def search(user):
    if user is session["Username"]:
        flash('please login first', 'warning')
        return redirect(url_for('index'))

    else:
        res = request.form.get("data")
        res = '%'+res+'%'
        result = db.query(books).filter(or_(books.title.ilike(
            res), books.author.ilike(res), books.isbn.ilike(res))).all()
        return render_template("index.html", result=result, user=user)


@ app.route("/bookDetails/<user>/<isbn>", methods=["POST", "GET"])
def bookDetails(user, isbn):
    # if user is session["Username"]:
        data = requests.get("https://www.goodreads.com/book/review_counts.json",
                            params={"key": "QBSkzdFzmInWGWMpZCDycg", "isbns": isbn})
        book = db.query(books).filter_by(isbn=isbn).first()
        parsed = json.loads(data.text)

        # print(parsed)
        res = {}
        for i in parsed:
            print(parsed[i])
            for j in (parsed[i]):
                # print(f'j,{j}')
                res = j
        allreviews = db.query(review).filter_by(isbn=isbn).all()
        if request.method == "POST":
            print('pst')
            rating = request.form.get("rating")
            reviews = request.form.get("review")
            timestamp = time.ctime(time.time())
            reviewtable = review(isbn=isbn, review=reviews, rating=rating,
                                 time_stamp=timestamp, title=book.title, username=user)
            db.add(reviewtable)
            db.commit()

            # Get all the reviews for the given book.
            allreviews = review.query.filter_by(isbn=isbn).all()
            return render_template("bookDetails.html", res=res, book=data, review=allreviews, property="none", message="You reviewed this book!!", user=user)
        else:
            # database query to check if the user had given review to that paticular book.
            rev = db.query(review).filter(review.isbn.like(
                isbn), review.username.like(user)).first()
            # print(rev)

            # Get all the reviews for the given book.
            allreviews = db.query(review).filter_by(isbn=isbn).all()

            # if review was not given then dispaly the book page with review button
            if rev is None:
                return render_template("bookDetails.html", book=book, res=res, review=allreviews, user=user)
            return render_template("bookDetails.html", book=book, message="You reviewed this book!!", review=allreviews, res=res, property="none", user=user)
    # else:
    #     flash('please login first', 'warning')
    #     return redirect(url_for('index'))
