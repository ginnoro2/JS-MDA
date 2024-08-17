import os
import csv

# Define the folders containing benign and malicious JS files
benign_folder = "/Users/priyankarai/Desktop/Desktop/shiva/ML/DataSet/benign-javascript-dataset"
malicious_folder = "/Users/priyankarai/Desktop/Desktop/shiva/ML/js-malicious-dataset"
ad_malicious_folder = "/Users/priyankarai/Desktop/Desktop/shiva/ML/DataSet/javascript-malware-collection"

# Path to the labels.csv file
labels_csv_path = "/Users/priyankarai/Desktop/Desktop/shiva/ML/label.csv"

# Function to collect files and their labels
def collect_files_and_labels(folder, target_label):
    rows = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".js"):
                filename = file
                rows.append([filename, target_label])
    return rows

# Collect benign files with target label 0
benign_rows = collect_files_and_labels(benign_folder, 0)

# Collect malicious files with target label 1
malicious_rows = collect_files_and_labels(malicious_folder, 1)

# Collect additional malicious files with target label 1
ad_malicious_rows = collect_files_and_labels(ad_malicious_folder, 1)

# Combine all sets of rows
updated_rows = benign_rows + malicious_rows + ad_malicious_rows

# Write the updated rows to labels.csv
with open(labels_csv_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['filename', 'target'])  # Write header
    csvwriter.writerows(updated_rows)

print(f"Labels updated in {labels_csv_path} for both benign and malicious JavaScript files.")
