import pandas as pd
import joblib
import os
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score
import seaborn as sns

# Function to read the CSV file and process it
def process_lexical_file(file_path):
    # Load the trained Random Forest model and PCA
    print("Loading the trained Random Forest model and PCA...")
    lr_model = joblib.load('random_forest_lexical.pkl')
    pca = joblib.load('pca_lexical.pkl')
    token_value_encoder = joblib.load('label_encoder_TokenValues.pkl')

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    
    # Load the new lexical data (e.g., 'lexical.csv')
    print(f"Loading new data from {file_path}...")
    dtype_spec = {
        'Filename': str,
        'TokenID': int,
        'TokenValue': str,
        'Target': int
    }
    new_data = pd.read_csv(file_path, dtype=dtype_spec)

    # Encode the TokenValue using the same encoder
    print("Encoding TokenValue in the new data...")
    new_data['TokenValue'] = token_value_encoder.transform(new_data['TokenValue'])

    # Prepare the feature set (X) - In this case, only TokenValue is used since PCA is applied to it
    X_new = new_data[['TokenValue']]

    # Apply PCA to the new data
    print("Applying PCA to the new data...")
    X_new_pca = pca.transform(X_new)

    # Make predictions using the Random Forest model
    print("Making predictions...")
    predictions = lr_model.predict(X_new_pca)

    # Convert predictions to [0, 1] format
    print("Predictions:")
    print(predictions)

    # Calculate the percentage of "Malicious" and "Benign"
    benign_count = (predictions == 0).sum()
    malicious_count = (predictions == 1).sum()
    total_count = len(predictions)

    benign_percentage = (benign_count / total_count) * 100
    malicious_percentage = (malicious_count / total_count) * 100

    # Print percentages
    print(f"Benign: {benign_percentage:.2f}%")
    print(f"Malicious: {malicious_percentage:.2f}%")

    # Determine overall result
    overall_result = "Malicious" if malicious_count > benign_count else "Benign"
    print(f"Overall result: {overall_result}")

    # Save the predictions if needed
    output_filename = 'predictions.csv'
    new_data['Predicted'] = predictions
    new_data.to_csv(output_filename, index=False)
    print(f"Predictions saved to {output_filename}.")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Process a lexical CSV file and run predictions.')
    parser.add_argument('lexical_file', help='Path to the lexical CSV file')
    args = parser.parse_args()

    process_lexical_file(args.lexical_file)

if __name__ == "__main__":
    main()
