from flask import Flask, request, jsonify
import uuid
import re

app = Flask(__name__)

# In-memory data storage
users = {}

# User class to structure user data
class User:
    def __init__(self, id, name, email, age):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

# Email validation regex
email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# Create a new user (POST /users)
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    name = data.get('name')
    email = data.get('email')
    age = data.get('age')

    # Validate name
    if not isinstance(name, str) or name.strip() == '':
        return jsonify({'error': 'Name is required and must be a string'}), 400

    # Validate email
    if not isinstance(email, str) or not email_regex.match(email):
        return jsonify({'error': 'Invalid email format'}), 400

    # Validate age
    if not isinstance(age, int) or age < 0 or age > 120:
        return jsonify({'error': 'Age must be an integer between 0 and 120'}), 400

    # Check if email is unique
    existing_user = next((user for user in users.values() if user.email == email), None)
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 400

    # Generate a new UUID for the user
    user_id = str(uuid.uuid4())
    user = User(user_id, name, email, age)
    users[user_id] = user

    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'age': user.age
    }), 201

# Get all users (GET /users)
@app.route('/users', methods=['GET'])
def get_users():
    user_list = []
    for user in users.values():
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'age': user.age
        }
        user_list.append(user_data)
    return jsonify(user_list), 200

# Get a single user by ID (GET /users/<id>)
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    user = users[user_id]
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'age': user.age
    }), 200

# Update a user by ID (PUT /users/<id>)
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    user = users[user_id]

    # Update name if provided
    if 'name' in data:
        name = data['name']
        if not isinstance(name, str) or name.strip() == '':
            return jsonify({'error': 'Name must be a non-empty string'}), 400
        user.name = name

    # Update email if provided
    if 'email' in data:
        email = data['email']
        if not isinstance(email, str) or not email_regex.match(email):
            return jsonify({'error': 'Invalid email format'}), 400
        # Check if the new email is unique
        existing_user = next((u for u in users.values() if u.email == email and u.id != user_id), None)
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 400
        user.email = email

    # Update age if provided
    if 'age' in data:
        age = data['age']
        if not isinstance(age, int) or age < 0 or age > 120:
            return jsonify({'error': 'Age must be an integer between 0 and 120'}), 400
        user.age = age

    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'age': user.age
    }), 200

# Delete a user by ID (DELETE /users/<id>)
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({'error': 'User not found'}), 404
    del users[user_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)