from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store for users
users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"}
}

# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

# GET single user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# POST: Add a new user
@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    new_id = max(users.keys()) + 1 if users else 1
    users[new_id] = {
        "name": data.get("name"),
        "email": data.get("email")
    }
    return jsonify({"message": "User added", "id": new_id}), 201

# PUT: Update an existing user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    data = request.json
    users[user_id].update({
        "name": data.get("name", users[user_id]["name"]),
        "email": data.get("email", users[user_id]["email"])
    })
    return jsonify({"message": "User updated"})

# DELETE: Remove a user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return jsonify({"message": "User deleted"})

if __name__ == "__main__":
    app.run(debug=True)
