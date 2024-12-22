import base64
import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DB_URL
from weather_service import get_weather_info

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    role = db.Column(db.String(20))
    _details = db.Column('details', db.String(1000), default='{}')

    @property
    def details(self):
        return json.loads(self._details)

    @details.setter 
    def details(self, value):
        self._details = json.dumps(value)

def check_auth(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None, None
    try:
        method, encoded = auth_header.split()
        if method.lower() == 'basic':
            decoded = base64.b64decode(encoded).decode()
            username, password = decoded.split(':')
            return username, password
    except:
        pass
    return None, None

def is_authorized(username, user_id):
    user = User.query.get(user_id)
    if not user:
        return False
    auth_user = User.query.filter_by(username=username).first()
    return auth_user and (auth_user.role == 'admin' or auth_user.id == user_id)

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(
        username=data.get('username'),
        password=data.get('password', 'pass'),
        role=data.get('role', 'user'),
        _details=json.dumps(data)
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created', 'id': new_user.id}), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'details': user.details
    })

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'details': user.details
    } for user in users])

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    username, password = check_auth(request)
    if not username or not password:
        return jsonify({'error': 'Unauthorized'}), 401
    
    auth_user = User.query.filter_by(username=username, password=password).first()
    if not auth_user:
        return jsonify({'error': 'Unauthorized'}), 401

    if is_authorized(username, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted'})
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'error': 'Forbidden'}), 403

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    username, password = check_auth(request)
    if not username or not password:
        return jsonify({'error': 'Unauthorized'}), 401
    
    auth_user = User.query.filter_by(username=username, password=password).first()
    if not auth_user:
        return jsonify({'error': 'Unauthorized'}), 401

    if is_authorized(username, user_id):
        user = User.query.get(user_id)
        if user:
            data = request.json
            user.details.update(data)
            if 'username' in data:
                user.username = data['username']
            if 'password' in data:
                user.password = data['password']
            if 'role' in data:
                user.role = data['role']
            db.session.commit()
            return jsonify({'message': 'User updated'})
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'error': 'Forbidden'}), 403

@app.route('/')
def index():
    return jsonify({
        "status": "running",
        "endpoints": {
            "weather": "/api/weather/{city}",  # Updated format
            "users": "/users",
            "user": "/user/<id>"
        }
    })

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city', 'Moscow')
    info = get_weather_info(city)
    return jsonify(info)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)