# from flask import Flask, jsonify, request
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Sample data store
# data_store = [
#     {
#         "firstname": "Likhitha",
#         "lastname": "Aaraga",
#         "email": "likhitha@gmail.com",
#         "username": "likhitha123",
#         "address": {
#             "street": "123 Main St",
#             "city": "Hyderabad",
#             "state": "Telangana",
#             "pincode": "500081"
#         },
#         "contact_number": "9876543210"
#     },
#     {
#         "firstname": "Pravallika",
#         "lastname": "Pavuluri",
#         "email": "pravallika@gmail.com",
#         "username": "pravallika456",
#         "address": {
#             "street": "456 Park Ave",
#             "city": "Bangalore",
#             "state": "Karnataka",
#             "pincode": "560001"
#         },
#         "contact_number": "8765432109"
#     }
# ]


# # Home route
# @app.route('/')
# def home():
#     return jsonify({"message": "Welcome to the Flask API!"})

# # GET all users
# @app.route('/users', methods=['GET'])
# def get_all_users():
#     return jsonify({"users": data_store})

# # GET a single user by firstname (Fixed)
# @app.route('/users/<string:firstname>', methods=['GET'])
# def get_user_by_name(firstname):
#     user = next((user for user in data_store if user["firstname"].lower() == firstname.lower()), None)
#     if user:
#         return jsonify(user)
#     return jsonify({"error": "User not found"}), 404

# # POST method - Add a new user
# @app.route('/users', methods=['POST'])
# def add_user():
#     new_user = request.get_json()
#     if "firstname" not in new_user or "lastname" not in new_user or "email" not in new_user:
#         return jsonify({"error": "Invalid data format"}), 400

#     data_store.append(new_user)
#     return jsonify({"message": "User added successfully", "user": new_user}), 201

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, jsonify, request

app = Flask(__name__)

# Secure API Key
API_KEY = "mysecureapikey123"

# Sample data store
data_store = [
    {
        "firstname": "Likhitha",
        "lastname": "Aaraga",
        "email": "likhitha@gmail.com",
        "username": "likhitha123",
        "address": {
            "street": "123 Main St",
            "city": "Hyderabad",
            "state": "Telangana",
            "pincode": "500081"
        },
        "contact_number": "9876543210"
    },
    {
        "firstname": "Pravallika",
        "lastname": "Pavuluri",
        "email": "pravallika@gmail.com",
        "username": "pravallika456",
        "address": {
            "street": "456 Park Ave",
            "city": "Bangalore",
            "state": "Karnataka",
            "pincode": "560001"
        },
        "contact_number": "8765432109"
    }
]

# Middleware to check API Key
@app.before_request
def require_api_key():
    """Check if API Key is valid."""
    if request.endpoint != "home":  # Allow home route without authentication
        api_key = request.headers.get("X-API-KEY")
        if not api_key or api_key != API_KEY:
            return jsonify({"error": "Unauthorized - Invalid API Key"}), 403

# Home route (No API key required)
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

# ✅ GET all users (Requires API Key)
@app.route('/users', methods=['GET'])
def get_all_users():
    return jsonify({"users": data_store})

# ✅ GET a single user by firstname (Requires API Key)
@app.route('/users/<string:firstname>', methods=['GET'])
def get_user_by_name(firstname):
    user = next((user for user in data_store if user["firstname"].lower() == firstname.lower()), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# ✅ POST a new user (Requires API Key)
@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.get_json()

    required_fields = ["firstname", "lastname", "email", "username", "address", "contact_number"]
    address_fields = ["street", "city", "state", "pincode"]

    for field in required_fields:
        if field not in new_user:
            return jsonify({"error": f"Missing field: {field}"}), 400

    for addr_field in address_fields:
        if addr_field not in new_user["address"]:
            return jsonify({"error": f"Missing address field: {addr_field}"}), 400

    data_store.append(new_user)
    return jsonify({"message": "User added successfully", "user": new_user}), 201

if __name__ == '__main__':
    app.run(debug=True)
