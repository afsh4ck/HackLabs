import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app as flask_app


@pytest.fixture()
def app():
    flask_app.config['TESTING'] = True
    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()
