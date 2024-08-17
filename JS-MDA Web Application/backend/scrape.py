from flask import Flask, request, jsonify, json
from flask_cors import CORS
from helium import start_chrome
from bs4 import BeautifulSoup
import subprocess
import joblib
import pandas as pd
import os

app = Flask(__name__)
tmp_file_path = "tmp.txt" #Define temporary file path 
lexical_file_path = "lexical.csv"
CORS(app)

# Load trained model and LabelEncoders
#pipeline_rf = joblib.load('random_forest_model.pkl')
#le_token = joblib.load('label_encoder_token.pkl')
#le_feature = joblib.load('label_encoder_feature.pkl')
@app.route('/api/saveToTmp', methods=['POST'])
def save_to_tmp():
    try:
        content = request.json['content']
        tmp_file_path = "tmp.txt"

        # Clear the contents of tmp.txt and append the new content
        with open(tmp_file_path, 'w') as tmp_file:
            tmp_file.write(content)

        return {'message': 'Content saved to tmp.txt.'}, 200
    except Exception as e:
        return {'error': str(e)}, 500
    
@app.route('/api/upload', methods=['POST'])
def upload_file():
    content = request.form.get('content')
    
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    try:
        # Clear the contents of tmp.txt and append the new content
        with open(tmp_file_path, 'w') as tmp_file:
            tmp_file.write(content)
        
        return jsonify({'message': 'File content saved to tmp.txt successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scrape', methods=['POST', 'OPTIONS'])
def scrape():
    if request.method == 'OPTIONS':
        return jsonify({'allow': 'POST'}), 200
    
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        browser = start_chrome(url, headless=True)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        scripts = soup.find_all('script')
        
        script_tags = []
        for script in scripts:
            src = script.get('src')
            if src:
                script_tag = f'<script src="{src}"></script>'
                script_tags.append(script_tag)
        with open(tmp_file_path, 'w') as file:
            json.dump(script_tags, file)
        
        return jsonify({'scripts': script_tags})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/parse', methods=['POST', 'OPTIONS'])
def parse():
    if request.method == 'OPTIONS':
        return jsonify({'allow': 'POST'}), 200

    try:
        # Load content from tmp.txt
        with open(tmp_file_path, 'r') as file:
            content = file.read()

        if not content:
            return jsonify({'error': 'Content is required'}), 400

        print("Received content:", content)

        # Run the parser script to parse JavaScript content
        result = subprocess.run(
            ["python3.10", "parse.py", content],
            capture_output=True,
            text=True
        )

        # Check if the subprocess command was successful
        if result.returncode != 0:
            raise RuntimeError(f"Parser script failed: {result.stderr.strip()}")

        parsed_data = result.stdout.strip()  # Adjust as per your parsing logic

        return jsonify({'parsed_data': parsed_data})

    except FileNotFoundError:
        return jsonify({'error': 'tmp.txt not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/identify', methods=['POST', 'OPTIONS'])
def identify():
    if request.method == 'OPTIONS':
        return jsonify({'allow': 'POST'}), 200

    try:
        with open(tmp_file_path, 'r') as file:
            content = file.read()

        if not content:
            return jsonify({'error': 'Content is required'}), 400

        result = subprocess.run(
            ["python", "detect_obfuscation.py", content],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"Detect script failed: {result.stderr.strip()}")

        detection_output = result.stdout.strip()

        return jsonify({'detection_output': detection_output})

    except FileNotFoundError:
        return jsonify({'error': 'tmp.txt not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/report', methods=['POST'])
def generate_report():
    try:
        data = request.get_json()
        file_path = data.get('filePath', 'tmp.txt')
        
        result = subprocess.run(
            ["python3.10", "static_report.py", file_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"Report script failed: {result.stderr.strip()}")

        report = result.stdout.strip()
        return jsonify({'report': report})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/detect', methods=['POST'])
def detectionengine():
    try:
        data = request.get_json()
        file_path = data.get('filePath', 'lexical.csv')
        
        # Ensure the file path exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Run the prediction script with the given file path
        result = subprocess.run(
            ["python", "predection.py", file_path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"Prediction script failed: {result.stderr.strip()}")

        report = result.stdout.strip()
        return jsonify({'report': report})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(port=2000, debug=True)
