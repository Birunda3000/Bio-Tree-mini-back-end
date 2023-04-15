import logging
import os

import app.main.model
from app import blueprint
from app.main import create_app, db
from app.main.model import User
from app.main.service import (
    create_default_cid_10,
    create_default_commission_types,
    create_default_leavings,
    create_default_queues,
    create_default_resources,
    create_default_roles,
    create_default_agencies_and_occupations,
)


env_name = os.environ.get("ENV_NAME", "dev")

app = create_app(env_name)
app.register_blueprint(blueprint)




@app.cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

    create_seed()

if __name__ == "__main__":

    app.run(host=app.config["HOST"])
