import os.path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from models import *
from controllers import *

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "storage.db"
)
db = SQLAlchemy(app)

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
