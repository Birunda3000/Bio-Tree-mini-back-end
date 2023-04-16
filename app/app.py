import os.path
from flask import Flask
from flask_restx import Api
from flask_restx.swagger import Swagger
from flask_sqlalchemy import SQLAlchemy
from controllers import tag_ns


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "storage.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

api = Api(app, version="1.0", title="Bio Tree API", description="A simple Bio Tree API")
api.add_namespace(tag_ns, path="/tag")

if __name__ == "__main__":
    with app.app_context():
        print("Creating database...")
        db.drop_all()
        db.create_all()
        db.session.commit()
    app.run(debug=True)

#att

