from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# from flask_bcrypt import Bcrypt


db = SQLAlchemy()

app = Flask(__name__)

cpf_validator = CPF()
cnpj_validator = CNPJ()
CORS(app)


def create_app(config_name: str) -> Flask:
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    return app
