from flask import Flask, request, jsonify
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os 
load_dotenv()

MONGO_URI = os.getenv('MONGO_URL')
# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

db = client.test

collection = db['flask-tutorial']
app= Flask(__name__)

# Path to the backend data file
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

@app.route('/api', methods=['GET'])
def get_data():
        file = open(DATA_FILE, 'r')
        data = json.load(file)
        file.close()
        return jsonify(data)
    
@app.route('/submit', methods = ['POST'])
def submit():
    form_data = request.get_json()
    collection.insert_one(form_data)
    return "Added record successfully!"

@app.route('/view')
def view():
    data = collection.find()
    data = list(data)
    for item in data:
        del item['_id']
        
    data = {
        'data':data
    }
    return jsonify(data)

@app.route('/submittodoitem', methods = ['POST'])
def submittodoitem():
    form_data = request.get_json()
    collection.insert_one(form_data)
    return "Added record successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000,debug=True)