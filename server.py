import base64
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import DB_URL
from weather_service import get_weather_info

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)

# In-memory "database"
users_db = {}
current_id = 1
admins = {'admin': 'admin123'}  # username: password
regulars = {}  # username: password

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    role = db.Column(db.String(20))

db.create_all()

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
    if username in admins:
        return True
    return users_db.get(user_id, {}).get('username') == username

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    global current_id
    users_db[current_id] = {
        'id': current_id,
        'username': data.get('username'),
        'role': data.get('role', 'user'),
        'details': data
    }
    if data.get('role') == 'admin':
        admins[data['username']] = data.get('password', 'pass')
    else:
        regulars[data['username']] = data.get('password', 'pass')
    current_id += 1
    return jsonify({'message': 'User created'}), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id not in users_db:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(users_db[user_id])

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(list(users_db.values()))

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    username, password = check_auth(request)
    if not username or not password:
        return jsonify({'error': 'Unauthorized'}), 401
    if (username in admins and admins[username] == password) or \
       (username in regulars and regulars[username] == password):
        if is_authorized(username, user_id):
            if user_id in users_db:
                del users_db[user_id]
                return jsonify({'message': 'User deleted'})
            return jsonify({'error': 'Not found'}), 404
        else:
            return jsonify({'error': 'Forbidden'}), 403
    return jsonify({'error': 'Unauthorized'}), 401

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    username, password = check_auth(request)
    if not username or not password:
        return jsonify({'error': 'Unauthorized'}), 401
    if (username in admins and admins[username] == password) or \
       (username in regulars and regulars[username] == password):
        if is_authorized(username, user_id):
            if user_id in users_db:
                data = request.json
                users_db[user_id]['details'].update(data)
                return jsonify({'message': 'User updated'})
            return jsonify({'error': 'Not found'}), 404
        else:
            return jsonify({'error': 'Forbidden'}), 403
    return jsonify({'error': 'Unauthorized'}), 401

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city', 'Moscow')
    info = get_weather_info(city)
    return jsonify(info)

if __name__ == '__main__':
    app.run(port=5000, debug=True)