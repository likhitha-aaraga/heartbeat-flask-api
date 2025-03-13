from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

# ✅ Use Environment Variable for MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://likhithaaaraga:<db_password>@mongodbcluster.9z09bie.mongodb.net/apitesting?retryWrites=true&w=majority&appName=MongoDBCluster")

app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

# Reference to the "userdata" collection
users_collection = mongo.db.userdata

# ✅ Health Check Route (Root)
@app.route('/')
def home():
    return jsonify({"message": "API is running and connected to MongoDB!"})

# ✅ POST Method - Store JSON Data in MongoDB
@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()

    # Ensure required fields exist
    required_fields = ["first_name", "last_name", "username", "email", "contact_number", "address"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Insert data into MongoDB
    users_collection.insert_one(data)
    return jsonify({"message": "User added successfully"}), 201

# ✅ GET Method - Retrieve All Users from MongoDB
@app.route('/users', methods=['GET'])
def get_all_users():
    users = list(users_collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId
    return jsonify(users)

# ✅ Run Flask App (Use Azure's Assigned Port)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # Use Azure-assigned port
    app.run(host='0.0.0.0', port=port)
