import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    response = client.post('/user', json={
        'username': 'testuser',
        'password': 'testpass',
        'role': 'user'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User created'

def test_get_nonexistent_user(client):
    response = client.get('/user/999')
    assert response.status_code == 404
    assert response.json['error'] == 'Not found'

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert isinstance(response.json, list)
