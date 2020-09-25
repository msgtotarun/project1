import os
from flask import Flask, render_template, request
from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
app = Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()