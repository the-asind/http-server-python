import os
import sys
import pytest
import base64

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import app, db

@pytest.fixture
def app_fixture():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app_fixture):    
    with app_fixture.test_client() as client:
        with app_fixture.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def auth_headers():
    credentials = base64.b64encode(b'admin:admin123').decode('utf-8')
    return {'Authorization': f'Basic {credentials}'}
