import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

# ✅ Load MongoDB Connection from Azure Environment Variable
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://likhithaaaraga:<db_password>@mongodbcluster.9z09bie.mongodb.net/apitesting?retryWrites=true&w=majority&appName=MongoDBCluster")
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

# Reference to "userdata" collection in "apitesting" database
users_collection = mongo.db.userdata

@app.route('/')
def home():
    return jsonify({"message": "API is running and connected to MongoDB!"})

@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    users_collection.insert_one(data)
    return jsonify({"message": "User added successfully"}), 201

@app.route('/users', methods=['GET'])
def get_all_users():
    users = list(users_collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId
    return jsonify(users)

# ✅ Use Azure's Assigned Port
if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))  # Use Azure-assigned port
    app.run(host='0.0.0.0', port=port)
