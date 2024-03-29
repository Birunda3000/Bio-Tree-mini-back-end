import pytest

from app import blueprint
from app import create_app, db

app = create_app("test")
app.register_blueprint(blueprint)


@pytest.fixture()
def client():
    """Init Flask test client"""
    with app.test_client() as client, app.app_context():
        yield client


@pytest.fixture()
def database(client, request):
    """Init database"""
    db.create_all()

    @request.addfinalizer
    def drop_tables():
        db.drop_all()

    return