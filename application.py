import os
import csv
import time
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from bookImport import *
active = 'active'
data = []
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
# with app.app_context():
#     main()
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

if not engine.dialect.has_table(engine, "Books"):
    User.__table__.create(bind=engine, checkfirst=True)
f = open("./static/books.csv")
reader = csv.reader(f)
next(reader)
for isbn, title, author, year in reader:
    book = books(isbn=isbn, title=title, author=author, year=year)
    db.add(book)
    print(
        f"added{book.title} with number {book.isbn} written by {book.author} published in the year {book.year}")
print('sessoin before commited')
db.commit()
print('sessoin commited')


@app.route("/")
def index():
    if 'Username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))


@app.route("/home/<user>")
def userHome(user):
  #  print(user in session)
    if user in session:
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


@app.route("/admin")
def admin():
    data = db.query(User).order_by(User.Time_registered)
    return render_template('admin.html', data=data.all())


@app.route("/registration", methods=["POST"])
def registration():
    # Get table information
    # If table don't exist, Create.
    if not engine.dialect.has_table(engine, "USERS"):
        User.__table__.create(bind=engine, checkfirst=True)
    rowName = ['Name', 'Username', 'Email', 'Password', 'RPassword', 'check']
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
    # print(Uname)
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


@app.route("/logout/<Username>")
def logout(Username):
    session.pop(Username, None)
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
        session[row[0]] = Username
        return redirect(url_for('userHome', user=row[0]))
    else:
        flash("account does not exist register now", "danger")
        return redirect(url_for('register'))
