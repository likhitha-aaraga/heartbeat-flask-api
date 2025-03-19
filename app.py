# import os
# from flask import Flask, request, jsonify
# from flask_pymongo import PyMongo

# app = Flask(__name__)

# # ✅ Load MongoDB URI from Azure Environment Variable or fallback
# MONGO_URI = os.getenv(
#     "MONGO_URI",
#     "mongodb+srv://likhitha_aaraga:<Likhi501>@mongodbcluster.9z09bie.mongodb.net/?retryWrites=true&w=majority&appName=MongoDBCluster"
# )
# app.config["MONGO_URI"] = MONGO_URI
# mongo = PyMongo(app)

# # Reference to "userdata" collection in "apitesting" database
# users_collection = mongo.db.userdata

# # ✅ Root Health Check Route
# @app.route('/')
# def home():
#     return jsonify({"message": "API is running and connected to MongoDB!"})

# # ✅ Test MongoDB Connection Route (Use for Debugging)
# @app.route('/test-mongo', methods=['GET'])
# def test_mongo_connection():
#     try:
#         server_info = mongo.cx.server_info()
#         return jsonify({"status": "MongoDB Connected", "server_info": server_info}), 200
#     except Exception as e:
#         print(f"MongoDB connection failed: {str(e)}")
#         return jsonify({"error": "MongoDB connection failed", "details": str(e)}), 500

# # ✅ POST Method - Store JSON Data in MongoDB
# @app.route('/user', methods=['POST'])
# def add_user():
#     try:
#         data = request.get_json(force=True)
#         print(f"Received JSON: {data}")  # ✅ Log incoming data

#         # Validate required user fields
#         required_fields = ["first_name", "last_name", "username", "email", "contact_number", "address"]
#         address_fields = ["street", "city", "state", "pincode"]

#         for field in required_fields:
#             if field not in data:
#                 error_msg = f"Missing field: {field}"
#                 print(error_msg)
#                 return jsonify({"error": error_msg}), 400

#         for addr_field in address_fields:
#             if addr_field not in data["address"]:
#                 error_msg = f"Missing address field: {addr_field}"
#                 print(error_msg)
#                 return jsonify({"error": error_msg}), 400

#         # Insert into MongoDB
#         result = users_collection.insert_one(data)
#         print(f"Inserted document ID: {result.inserted_id}")

#         return jsonify({"message": "User added successfully"}), 201

#     except Exception as e:
#         print(f"Error in POST /user: {str(e)}")
#         return jsonify({"error": "Internal server error", "details": str(e)}), 500

# # ✅ GET Method - Retrieve All Users from MongoDB
# @app.route('/users', methods=['GET'])
# def get_all_users():
#     try:
#         users = list(users_collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId
#         print(f"Fetched {len(users)} users from MongoDB.")
#         return jsonify(users)
#     except Exception as e:
#         print(f"Error in GET /users: {str(e)}")
#         return jsonify({"error": "Internal server error", "details": str(e)}), 500

# # ✅ Azure App Service requires port 8000
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000)

import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# ✅ MongoDB Connection
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://likhitha_aaraga:Likhi501@mongodbcluster.9z09bie.mongodb.net/apitesting?retryWrites=true&w=majority&tls=true"
)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)
users_collection = mongo.db.userdata

# ✅ API Key
API_KEY = "b9f1e4cb-894a-417c-8b35-764b277d7bda"

# ✅ Middleware: Require API Key for all routes except '/' and '/test-mongo'
@app.before_request
def require_api_key():
    if request.endpoint not in ['home', 'test_mongo_connection']:
        key = request.headers.get("X-API-KEY")
        if not key or key != API_KEY:
            print(f"Unauthorized request. Provided key: {key}")
            return jsonify({"error": "Unauthorized – Invalid API Key"}), 401

# ✅ Health Check Route
@app.route('/')
def home():
    return jsonify({"message": "API is running and connected to MongoDB!"})

# ✅ Test MongoDB Connection
@app.route('/test-mongo', methods=['GET'])
def test_mongo_connection():
    try:
        server_info = mongo.cx.server_info()
        return jsonify({"status": "MongoDB Connected", "server_info": server_info}), 200
    except Exception as e:
        print(f"MongoDB connection failed: {str(e)}")
        return jsonify({"error": "MongoDB connection failed", "details": str(e)}), 500

# ✅ POST User Data (Requires API Key)
@app.route('/user', methods=['POST'])
def add_user():
    try:
        data = request.get_json(force=True)

        required_fields = ["first_name", "last_name", "username", "email", "contact_number", "address"]
        address_fields = ["street", "city", "state", "pincode"]

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        for addr_field in address_fields:
            if addr_field not in data["address"]:
                return jsonify({"error": f"Missing address field: {addr_field}"}), 400

        users_collection.insert_one(data)
        return jsonify({"message": "User added successfully"}), 201

    except Exception as e:
        print(f"Error in POST /user: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# ✅ GET All Users (Requires API Key)
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = list(users_collection.find({}, {"_id": 0}))
        return jsonify(users)
    except Exception as e:
        print(f"Error in GET /users: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# ✅ Azure-compatible Port
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
