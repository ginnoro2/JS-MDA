#!/opt/homebrew/bin/python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    response = requests.post('http://localhost:2001/api/scrape', json=data)
    return jsonify(response.json())

@app.route('/api/parse', methods=['POST'])
def parse():
    data = request.get_json()
    response = requests.post('http://localhost:2002/api/parse', json=data)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=2000, debug=True)
