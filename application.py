import os

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
active = 'active'

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
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


@app.route("/registration", methods=["POST"])
def registration():
    name = request.form.get("Username")
    email = request.form.get("email")
    password = request.form.get("password")
    print(name, password, email)
    return name+" , "+email

@app.route("/loginNow", methods=["POST"])
def loginNow():
    return 'hello'