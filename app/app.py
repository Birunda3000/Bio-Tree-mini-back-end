import os.path

from config import config_by_name, db
from controllers import tag_ns, taxon_ns
from flask import Blueprint, Flask
from flask_cors import CORS
from flask_restx import Api
from flask_restx.swagger import Swagger
from flask_sqlalchemy import SQLAlchemy
from seeders import seed_db


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    return app


env_name = os.environ.get("ENV_NAME", "dev")
app = create_app(env_name)
CORS(app)

blueprint = Blueprint("api", __name__)

api = Api(app, version="1.0", title="Bio Tree API", description="A mini Bio Tree API")
api.add_namespace(tag_ns, path="/tag")
api.add_namespace(taxon_ns, path="/taxon")


if __name__ == "__main__":
    with app.app_context():
        print("Creating database...")
        db.drop_all()
        db.create_all()
        seed_db()
        db.session.commit()
    app.run(debug=True)
