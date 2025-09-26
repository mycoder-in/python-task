from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory user storage (dictionary)
users = {}

# GET - Fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET - Fetch user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id in users:
        return jsonify({user_id: users[user_id]})
    return jsonify({"error": "User not found"}), 404

# POST - Add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user_id = data.get("id")
    name = data.get("name")

    if user_id in users:
        return jsonify({"error": "User already exists"}), 400

    users[user_id] = {"name": name}
    return jsonify({"message": "User added", "user": users[user_id]}), 201

# PUT - Update user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    users[user_id].update(data)
    return jsonify({"message": "User updated", "user": users[user_id]})

# DELETE - Remove user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    del users[user_id]
    return jsonify({"message": "User deleted"})


if __name__ == '__main__':
    app.run(debug=True)
