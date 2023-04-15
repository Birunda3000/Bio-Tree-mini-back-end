import os.path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# app.register_blueprint(tag_controller)


if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()
    app.run(debug=True)

