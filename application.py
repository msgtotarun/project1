import os
import time
from flask import Flask, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
from sqlalchemy.exc import SQLAlchemyError
from flask.helpers import flash
active = 'active'
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html", home=active)


@app.route("/register")
def register():
    return render_template('register.html', register=active)


@app.route("/login")
def login():
    return render_template('login.html', login=active)


@app.route("/admin")
def admin():
    data = []
    data = db.query(User).order_by(User.Time_registered)
    return render_template('admin.html', data=data.all())


@app.route("/registration", methods=["POST"])
def registration():
    # Get table information
    # If table don't exist, Create.
    if not engine.dialect.has_table(engine, "USERS"):
        User.__table__.create(bind=engine, checkfirst=True)

    rowName = ['Name', 'Username', 'Email', 'Password']
    row = []
    for i in rowName:
        row.append(request.form.get(i))
    print(row)
    user = User(Name=row[0], Username=row[1], Email=row[2],
                Password=row[3], Time_registered=time.ctime(time.time()))

    try:
        db.add(user)
        db.commit()
        flash('account created sucessfully')
        # return Name+" ,"+Email+","+Time_registered
        return render_template("msg.html", msg='Hi '+row[0]+", Your account is sucessfully created")
    except:
        return render_template("msg.html", msg="please fill all details or error occured")
    finally:
        db.remove()
        db.close()


@ app.route("/loginNow", methods=["POST"])
def loginNow():
    return 'hello'
