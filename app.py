import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# ✅ Load MongoDB Connection from Azure Environment Variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://likhitha_aaraga:<Likhi501>@mongodbcluster.9z09bie.mongodb.net/?retryWrites=true&w=majority&appName=MongoDBCluster")
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

# Reference to "userdata" collection in "apitesting" database
users_collection = mongo.db.userdata

# ✅ Health Check Route
@app.route('/')
def home():
    return jsonify({"message": "API is running and connected to MongoDB!"})

# ✅ POST Method - Store JSON Data in MongoDB
@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()

    # ✅ Ensure all required fields exist
    required_fields = ["first_name", "last_name", "username", "email", "contact_number", "address"]
    address_fields = ["street", "city", "state", "pincode"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    for addr_field in address_fields:
        if addr_field not in data["address"]:
            return jsonify({"error": f"Missing address field: {addr_field}"}), 400

    # ✅ Insert data into MongoDB
    users_collection.insert_one(data)
    return jsonify({"message": "User added successfully"}), 201

# ✅ GET Method - Retrieve All Users from MongoDB
@app.route('/users', methods=['GET'])
def get_all_users():
    users = list(users_collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId
    return jsonify(users)

# ✅ Use Azure's Assigned Port
if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))  # Use Azure-assigned port
    app.run(host='0.0.0.0', port=port)
