import os
import subprocess
import csv
import json
from flask import Flask, request, jsonify
from lexical_unit import TOKENS
from syntatic_unit import features

app = Flask(__name__)

# Define paths (update as per your environment)
tokenizer_script_path = "tokenizer.js"
syntactic_script_path = "parser.js"
lexical_output_csv_path = "malicious_lexical.csv"
syntactic_output_csv_path = "malicious_syntactic.csv"
labels_csv_path = "labels.csv"

# Load labels into a dictionary
labels = {}
with open(labels_csv_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip the header
    for row in csvreader:
        if len(row) == 2:
            filename, target = row
            labels[filename] = int(target)
        else:
            print(f"Skipping malformed row in labels file: {row}")

# Initialize CSV files with headers if they don't exist
if not os.path.exists(lexical_output_csv_path):
    with open(lexical_output_csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Filename', 'TokenID', 'TokenValue', 'Target'])  # Header

if not os.path.exists(syntactic_output_csv_path):
    with open(syntactic_output_csv_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Filename', 'FeatureID', 'Feature', 'Target'])  # Header

# Function to process JavaScript content
def process_js_content(javascript_code):
    # Temporary paths for outputs
    temp_output_path_tokens = "temp_tokens.txt"
    temp_output_path_syntactic = "temp_syntactic.txt"

    # Write JavaScript code to a temporary file
    temp_js_file_path = "temp_js_file.js"
    with open(temp_js_file_path, 'w') as temp_js_file:
        temp_js_file.write(javascript_code)
    
    # Run the tokenizer script using Node.js
    try:
        result = subprocess.run(
            ["node", tokenizer_script_path, temp_js_file_path, temp_output_path_tokens],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error tokenizing content: {e.stderr}")
        return None, None

    # Run the syntactic analyzer script using Node.js
    try:
        result = subprocess.run(
            ["node", syntactic_script_path, temp_js_file_path, temp_output_path_syntactic],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error parsing content: {e.stderr}")
        return None, None
    
    # Read and parse token output
    tokens = []
    with open(temp_output_path_tokens, 'r') as file:
        lines = file.readlines()
        for line in lines:
            token_type, token_value = line.strip().split(',', 1)
            token_id = TOKENS.get(token_type, -1)  # Use -1 for unknown token types
            tokens.append((token_id, token_value))
    
    # Read and parse syntactic feature output
    syntactic_features = []
    with open(temp_output_path_syntactic, 'r') as file:
        lines = file.readlines()
        for line in lines:
            feature = line.strip()
            feature_id = features.get(feature, -1)  # Use -1 for unknown features
            syntactic_features.append((feature_id, feature))
    
    # Clean up temporary files
    os.remove(temp_js_file_path)
    os.remove(temp_output_path_tokens)
    os.remove(temp_output_path_syntactic)
    
    return tokens, syntactic_features

# Function to write parsed data to CSV
def write_parsed_data_to_csv(filename, tokens, syntactic_features, target):
    # Append results to lexical CSV
    with open(lexical_output_csv_path, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for token in tokens:
            csvwriter.writerow([filename, token[0], token[1], target])  # Append tokens
    
    # Append results to syntactic CSV
    with open(syntactic_output_csv_path, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for feature in syntactic_features:
            csvwriter.writerow([filename, feature[0], feature[1], target])  # Append syntactic features

# Flask route to parse JavaScript content
@app.route('/api/parse', methods=['POST'])
def parse():
    data = request.get_json()
    content = data.get('content')
    if not content:
        return jsonify({'error': 'Content is required'}), 400

    try:
        tokens, syntactic_features = process_js_content(content)
        if tokens is None or syntactic_features is None:
            return jsonify({'error': 'Error processing content'}), 500

        # Example filename and target for demonstration
        filename = "example.js"
        target = labels.get(filename, 0)  # Default target to 0 if not found

        # Write parsed data to CSV files
        write_parsed_data_to_csv(filename, tokens, syntactic_features, target)

        parsed_data = {
            'tokens': tokens,
            'syntactic_features': syntactic_features
        }

        return jsonify(parsed_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    # Example usage: Process JavaScript content
    javascript_code = """
    function example() {
        console.log('This is an example function.');
    }
    """
    tokens, syntactic_features = process_js_content(javascript_code)
    if tokens and syntactic_features:
        filename = "example.js"
        target = labels.get(filename, 0)  # Default target to 0 if not found
        write_parsed_data_to_csv(filename, tokens, syntactic_features, target)
        print(f"Tokenization and parsing complete. Results saved to {lexical_output_csv_path} and {syntactic_output_csv_path}")
    else:
        print("Error processing content.")
