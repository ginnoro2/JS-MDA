import os
import subprocess
import csv
from lexical_unit import TOKENS
from syntatic_unit import features

# Define paths
base_folder = os.path.expanduser("/Users/priyankarai/Desktop/Desktop/shiva/ML/DataSet/javascript-malware-collection/a")
tokenizer_script_path = "tokenizer.js"
syntactic_script_path = "parser.js"

# Define output CSV paths
lexical_output_csv_path = "/Users/priyankarai/Desktop/Desktop/shiva/ML/test.csv"
syntactic_output_csv_path = "/Users/priyankarai/Desktop/Desktop/shiva/ML/mtest.csv"
labels_csv_path = "/Users/priyankarai/Desktop/Desktop/shiva/ML/label.csv"  # Replace with the path to your labels CSV file

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

# Function to process a single JavaScript file
def process_js_file(js_file_path):
    # Temporary paths for outputs
    temp_output_path_tokens = "temp_tokens.txt"
    temp_output_path_syntactic = "temp_syntactic.txt"
    
    # Run the tokenizer script using Node.js
    try:
        result = subprocess.run(
            ["node", tokenizer_script_path, js_file_path, temp_output_path_tokens],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error tokenizing file {js_file_path}: {e.stderr}")
        return None, None

    # Run the syntactic analyzer script using Node.js
    try:
        result = subprocess.run(
            ["node", syntactic_script_path, js_file_path, temp_output_path_syntactic],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error parsing file {js_file_path}: {e.stderr}")
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
    
    return tokens, syntactic_features

# Function to iterate through folders and process each JS file
def process_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".js"):
                js_file_path = os.path.join(root, file)
                tokens, syntactic_features = process_js_file(js_file_path)
                
                if tokens is None or syntactic_features is None:
                    continue  # Skip files with errors

                filename = os.path.basename(js_file_path)
                target = labels.get(filename, 0)  # Default target to 0 if not found
                
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

# Example usage: Process each folder containing JavaScript files
process_folder(base_folder)

print(f"Tokenization and parsing complete. Results saved to {lexical_output_csv_path} and {syntactic_output_csv_path}")
