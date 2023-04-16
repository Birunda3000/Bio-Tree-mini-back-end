import os.path
from flask_restx import Api
from flask import Flask
from flask_restx.swagger import Swagger
from flask_sqlalchemy import SQLAlchemy
from config import db
from controllers import tag_ns

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "storage.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

api = Api(app, version="1.0", title="Bio Tree API", description="A mini Bio Tree API")
api.add_namespace(tag_ns, path="/tag")


def create_app(config_name: str) -> Flask:
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)

    return app


if __name__ == "__main__":
    with app.app_context():
        print("Creating database...")
        db.init_app(app)
        db.drop_all()
        db.create_all()
        db.session.commit()
    app.run(debug=True)

