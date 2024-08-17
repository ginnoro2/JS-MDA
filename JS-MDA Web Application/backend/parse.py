import os
import subprocess
import csv
import json
from lexical_unit import TOKENS
from syntatic_unit import features

# Define paths (update as per your environment)
tokenizer_script_path = "token_parser.js"  # Combined script path
lexical_output_csv_path = "lexical.csv"
syntactic_output_csv_path = "syntactic.csv"
labels_csv_path = "label.csv"
tmp_txt_path = "tmp.txt"

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
    temp_output_path = "temp_output.json"

    # Write JavaScript code to a temporary file
    temp_js_file_path = "temp_js_file.js"
    with open(temp_js_file_path, 'w') as temp_js_file:
        temp_js_file.write(javascript_code)
    
    # Run the combined tokenizer and parser script using Node.js
    try:
        result = subprocess.run(
            ["node", tokenizer_script_path, temp_js_file_path, temp_output_path],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error processing content: {e.stderr}")
        return None, None

    # Read and parse the output JSON
    with open(temp_output_path, 'r') as file:
        data = json.load(file)

    tokens = data.get('tokens', [])
    syntactic_features = data.get('syntactic_features', [])

    # Clean up temporary files
    os.remove(temp_js_file_path)
    os.remove(temp_output_path)
    
    return tokens, syntactic_features

# Function to write parsed data to CSV
def write_parsed_data_to_csv(filename, tokens, syntactic_features, target):
    # Append results to lexical CSV
    with open(lexical_output_csv_path, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for token in tokens:
            token_id = TOKENS.get(token['type'], -1)  # Use -1 for unknown token types
            csvwriter.writerow([filename, token_id, token['value'], target])  # Append tokens
    
    # Append results to syntactic CSV
    with open(syntactic_output_csv_path, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for feature in syntactic_features:
            feature_id = features.get(feature['type'], -1)  # Use -1 for unknown features
            csvwriter.writerow([filename, feature_id, feature['type'], target])  # Append syntactic features

if __name__ == "__main__":
    # Example usage: Read JavaScript content from tmp.txt
    try:
        with open(tmp_txt_path, 'r') as file:
            javascript_code = file.read()

        tokens, syntactic_features = process_js_content(javascript_code)
        if tokens is None or syntactic_features is None:
            print('Error processing content.')
        else:
            filename = "tmp.txt"
            target = labels.get(filename, 0)  # Default target to 0 if not found
            write_parsed_data_to_csv(filename, tokens, syntactic_features, target)
            print(f"Tokenization and parsing complete. Results saved to {lexical_output_csv_path} and {syntactic_output_csv_path}")
    
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
