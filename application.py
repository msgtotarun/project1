import os
import csv
import time
from flask import Flask, render_template, request, redirect, flash, url_for, session
import sys
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
import requests
import json
from flask.json import jsonify
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
    if 'Username' not in session:
        rowName = ['Name', 'Username', 'Email',
                   'Password', 'RPassword', 'check']
        row = []
        for i in rowName:
            s = request.form.get(i)
            row.append(s)
            print(s)
        Uname = db.query(User).filter_by(Username=row[1]).first()
        email = db.query(User).filter_by(Email=row[2]).first()
        if(Uname != None and Uname.Username == row[1]):
            flash('username already exist,please login', 'warning')
            return redirect(url_for('index'))
        elif(email != None and email.Email == row[2]):
            flash('Email already exist,please login', 'warning')
            return redirect(url_for('index'))

        user = User(Name=row[0], Username=row[1], Email=row[2],
                    Password=row[3], Time_registered=time.ctime(time.time()))
        try:
            db.add(user)
            db.commit()
            flash(f"HI {row[0]} account created sucessfully", 'success')
        except:
            # e = sys.exc_info()
            # print(e)
            flash("error occured", 'danger')
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


@app.route("/api/search/", methods=["POST"])
def search_api():

    if request.method == "POST":
        var = request.json

        res = var["search"]
        res = "%" + res + "%"

        result = db.query(books).filter(or_(books.title.ilike(res), books.author.ilike(res), books.isbn.ilike(res))
                                        ).all()

        if result is None:
            return jsonify({"error": "Book not found"}), 400

        book_ISBN = []
        book_TITLE = []
        book_AUTHOR = []
        book_YEAR = []

        for eachresult in result:
            book_ISBN.append(eachresult.isbn)
            book_TITLE.append(eachresult.title)
            book_AUTHOR.append(eachresult.author)
            book_YEAR.append(eachresult.year)

        dict = {
            "isbn": book_ISBN,
            "title": book_TITLE,
            "author": book_AUTHOR,
            "year": book_YEAR,
        }
        print("returning")
        print(dict)
        return jsonify(dict), 200
    return "<h1>Come again</h1>"


@app.route("/api/book/", methods=["POST"])
def book_api():

    if request.method == "POST":
        var = request.json
        res = var["isbn"]
        isbn = res

        book = db.query(books).filter_by(isbn=isbn).first()
        res = requests.get(
            "https://www.goodreads.com/book/review_counts.json",
            params={"key": "2VIV9mRWiAq0OuKcOPiA", "isbns": isbn},
        )

        # Parsing the data
        data = res.text
        parsed = json.loads(data)
        print(parsed)
        res = {}
        for i in parsed:
            for j in parsed[i]:
                res = j

        allreviews = db.query(review).filter_by(isbn=isbn).all()
        rew = []
        time = []
        usr = []
        for rev in allreviews:
            rew.append(rev.review)
            time.append(rev.time_stamp)
            usr.append(rev.username)

        if book is None:
            return jsonify({"error": "Book not found"}), 400

        dict = {
            "isbn": isbn,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "average_rating": res["average_rating"],
            "average_reviewcount": res["reviews_count"],
            "review": rew,
            "time_stamp": time,
            "username": usr,
        }
        return jsonify(dict), 200


@app.route("/api/submit_review/<user>", methods=["POST"])
def review_api(user):
    if request.method == "POST":

        var = request.json
        # print("-------------------", var)
        isbn = var["isbn"]
        username = user
        rating = var["rating"]
        reviews = var["reviews"]
        print(isbn, username, rating, reviews)

        # if "username" and "isbn" in request.args:
        #     username = request.args["username"]
        #     isbn = request.args["isbn"]
        #     rating = request.args["rating"]
        #     reviews = request.args["review"]
        # else:
        #     return "Error: no isbn/username/rating/review/ field provided"

        # check if the paticular user given review before
        rev_From_db = db.query(review).filter(
            review.isbn.like(isbn), review.username.like(username)
        ).first()
        print("first", str(rev_From_db))

        # if the user doesnt give the review for that book
        if rev_From_db is None:

            try:
                # bring the book details
                book = db.query(books).filter_by(isbn=isbn).first()
                print("book", str(book))
            except:
                message = "Enter valid ISBN"
                return jsonify(message), 404

            timestamp = time.ctime(time.time())
            title = book.title
            user = review(
                isbn=isbn,
                review=reviews,
                rating=rating,
                time_stamp=timestamp,
                title=title,
                username=username,
            )
            db.add(user)
            db.commit()

            allreviews = db.query(review).filter_by(isbn=isbn).all()
            rew = []
            timeStamp = []
            usr = []
            for rev in allreviews:
                rew.append(rev.review)
                timeStamp.append(rev.time_stamp)
                usr.append(rev.username)

            dict = {
                "isbn": isbn,
                "review": rew,
                "time_stamp": timeStamp,
                "username": usr,
                "message": "You reviewed this book.",
            }

            return jsonify(dict), 200
        else:
            dict = {"message": "You already reviewed this book."}
            return jsonify(dict), 200


