import os
import sys
import base64
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server import app, db, User

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def auth_headers():
    credentials = base64.b64encode(b'admin:admin123').decode('utf-8')
    return {'Authorization': f'Basic {credentials}'}

def test_create_user(client, app):
    with app.app_context():
        response = client.post('/user', json={
            'username': 'testuser',
            'password': 'testpass',
            'role': 'user'
        })
        assert response.status_code == 201
        assert response.json['message'] == 'User created'
        
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.role == 'user'

def test_get_nonexistent_user(client):
    response = client.get('/user/999')
    assert response.status_code == 404
    assert response.json['error'] == 'Not found'

def test_get_users(client):
    users = [
        User(username='user1', password='pass1', role='user'),
        User(username='user2', password='pass2', role='admin')
    ]
    with app.app_context():
        db.session.bulk_save_objects(users)
        db.session.commit()

    response = client.get('/users')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 2
    assert response.json[0]['username'] == 'user1'
    assert response.json[1]['username'] == 'user2'

def test_update_user(client, auth_headers):
    user = User(username='updateme', password='oldpass', role='user')
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    response = client.put(
        f'/user/{user_id}',
        headers=auth_headers,
        json={'username': 'updated', 'password': 'newpass'}
    )
    assert response.status_code == 200
    
    updated_user = User.query.get(user_id)
    assert updated_user.username == 'updated'
    assert updated_user.password == 'newpass'

def test_delete_user(client, auth_headers):
    user = User(username='deleteme', password='pass', role='user')
    with app.app_context():
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    response = client.delete(f'/user/{user_id}', headers=auth_headers)
    assert response.status_code == 200

    deleted_user = User.query.get(user_id)
    assert deleted_user is None
