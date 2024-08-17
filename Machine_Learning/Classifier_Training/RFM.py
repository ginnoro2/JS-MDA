import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
import time

# Function to preprocess categorical columns
def preprocess_categorical_columns(df, categorical_columns):
    print(f"Preprocessing columns: {categorical_columns}")
    label_encoders = {}
    for col in categorical_columns:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))  # Ensure column is treated as string
            label_encoders[col] = le
            print(f"Encoded {col}: {df[col].head()}")
        else:
            print(f"Column '{col}' not found in DataFrame.")
    return df, label_encoders

# Define paths to your CSV files
Lexical_DataSet_csv = "lexical_dataset_alternate.csv"
Syntactic_DataSet_csv = "syntactic_dataset_alternate.csv"

# Load data into DataFrames with explicit dtype specification
start_time = time.time()
df_lexical = pd.read_csv(Lexical_DataSet_csv, dtype={'Filename': str, 'TokenID': int, 'TokenValue': str, 'Target': int})
df_syntactic = pd.read_csv(Syntactic_DataSet_csv, dtype={'Filename': str, 'FeatureID': int, 'Feature': str, 'Target': int})
end_time = time.time()
print(f"Datasets loaded in {end_time - start_time:.2f} seconds.")

# Debug: Print columns present in the DataFrames
print("Lexical DataFrame columns:", df_lexical.columns)
print("Syntactic DataFrame columns:", df_syntactic.columns)

# Checking columns
expected_columns_lexical = ['Filename', 'TokenID', 'TokenValue', 'Target']
missing_columns_lexical = [col for col in expected_columns_lexical if col not in df_lexical.columns]

expected_columns_syntactic = ['Filename', 'FeatureID', 'Feature', 'Target']
missing_columns_syntactic = [col for col in expected_columns_syntactic if col not in df_syntactic.columns]

if missing_columns_lexical:
    print(f"Missing columns in lexical DataFrame: {missing_columns_lexical}")
if missing_columns_syntactic:
    print(f"Missing columns in syntactic DataFrame: {missing_columns_syntactic}")

# Preprocess lexical data
def preprocess_lexical_data(df):
    df['TokenID'].fillna(0, inplace=True)
    df['TokenValue'].fillna('', inplace=True)
    df['TokenID'] = df['TokenID'].astype(int)
    df, label_encoders = preprocess_categorical_columns(df, ['TokenValue'])  # Adjust based on actual columns
    return df, label_encoders

# Preprocess syntactic data
def preprocess_syntactic_data(df):
    df['FeatureID'].fillna(0, inplace=True)
    df['Feature'].fillna('', inplace=True)
    df['FeatureID'] = df['FeatureID'].astype(int)
    df, label_encoders = preprocess_categorical_columns(df, ['Feature'])  # Adjust based on actual columns
    return df, label_encoders

# Preprocess both DataFrames
start_time = time.time()
df_lexical, lexical_encoders = preprocess_lexical_data(df_lexical)
end_time = time.time()
print(f"Lexical DataFrame preprocessed in {end_time - start_time:.2f} seconds.")

start_time = time.time()
df_syntactic, syntactic_encoders = preprocess_syntactic_data(df_syntactic)
end_time = time.time()
print(f"Syntactic DataFrame preprocessed in {end_time - start_time:.2f} seconds.")

# Save entire label encoders dictionary
joblib.dump(lexical_encoders['TokenValue'], 'label_encoder_TokenValues.pkl')
joblib.dump(syntactic_encoders['Feature'], 'label_encoder_Features.pkl')
print("Label encoders saved.")

# Separate features and target for lexical dataset
X_lexical = df_lexical.drop(columns=['Target', 'Filename', 'TokenID'])
y_lexical = df_lexical['Target']
print("Lexical features and target separated.")

# Separate features and target for syntactic dataset
X_syntactic = df_syntactic.drop(columns=['Target', 'Filename', 'FeatureID'])
y_syntactic = df_syntactic['Target']
print("Syntactic features and target separated.")

# Determine n_components dynamically based on data size
n_components_lexical = min(50, X_lexical.shape[1])  # Ensure it's within valid range
n_components_syntactic = min(50, X_syntactic.shape[1])  # Ensure it's within valid range
print(f"PCA components: Lexical = {n_components_lexical}, Syntactic = {n_components_syntactic}")

# Apply PCA to reduce dimensionality
start_time = time.time()
pca_lexical = PCA(n_components=n_components_lexical)
X_lexical_pca = pca_lexical.fit_transform(X_lexical)
end_time = time.time()
print(f"PCA applied to lexical dataset in {end_time - start_time:.2f} seconds.")

start_time = time.time()
pca_syntactic = PCA(n_components=n_components_syntactic)
X_syntactic_pca = pca_syntactic.fit_transform(X_syntactic)
end_time = time.time()
print(f"PCA applied to syntactic dataset in {end_time - start_time:.2f} seconds.")

# Save PCA models
joblib.dump(pca_lexical, 'pca_lexical.pkl')
joblib.dump(pca_syntactic, 'pca_syntactic.pkl')
print("PCA models saved.")

# Split data into training and testing sets for both datasets
start_time = time.time()
X_lexical_train, X_lexical_test, y_lexical_train, y_lexical_test = train_test_split(X_lexical_pca, y_lexical, test_size=0.2, random_state=42)
X_syntactic_train, X_syntactic_test, y_syntactic_train, y_syntactic_test = train_test_split(X_syntactic_pca, y_syntactic, test_size=0.2, random_state=42)
end_time = time.time()
print(f"Data split into training and testing sets in {end_time - start_time:.2f} seconds.")

# Apply SMOTE to handle class imbalance in lexical dataset
start_time = time.time()
print("Applying SMOTE to lexical dataset...")
smote = SMOTE(random_state=42)
X_lexical_train_res, y_lexical_train_res = smote.fit_resample(X_lexical_train, y_lexical_train)
end_time = time.time()
print(f"SMOTE applied to lexical dataset in {end_time - start_time:.2f} seconds.")

# Apply SMOTE to handle class imbalance in syntactic dataset
start_time = time.time()
print("Applying SMOTE to syntactic dataset...")
X_syntactic_train_res, y_syntactic_train_res = smote.fit_resample(X_syntactic_train, y_syntactic_train)
end_time = time.time()
print(f"SMOTE applied to syntactic dataset in {end_time - start_time:.2f} seconds.")

# Initialize Random Forest classifiers
print("Initializing Random Forest classifiers...")
clf_lexical_rf = RandomForestClassifier(random_state=42)
clf_syntactic_rf = RandomForestClassifier(random_state=42)

# Fit Random Forest classifiers on training data
start_time = time.time()
print("Fitting Random Forest on lexical dataset...")
clf_lexical_rf.fit(X_lexical_train_res, y_lexical_train_res)
end_time = time.time()
print(f"Random Forest trained on lexical dataset in {end_time - start_time:.2f} seconds.")

start_time = time.time()
print("Fitting Random Forest on syntactic dataset...")
clf_syntactic_rf.fit(X_syntactic_train_res, y_syntactic_train_res)
end_time = time.time()
print(f"Random Forest trained on syntactic dataset in {end_time - start_time:.2f} seconds.")

# Save the trained models
joblib.dump(clf_lexical_rf, 'random_forest_lexical.pkl')
joblib.dump(clf_syntactic_rf, 'random_forest_syntactic.pkl')
print("Random Forest models saved.")

# Predict on test data with Random Forest classifiers
start_time = time.time()
print("Predicting on lexical test data with Random Forest...")
y_lexical_rf_pred = clf_lexical_rf.predict(X_lexical_test)
end_time = time.time()
print(f"Prediction on lexical test data completed in {end_time - start_time:.2f} seconds.")

start_time = time.time()
print("Predicting on syntactic test data with Random Forest...")
y_syntactic_rf_pred = clf_syntactic_rf.predict(X_syntactic_test)
end_time = time.time()
print(f"Prediction on syntactic test data completed in {end_time - start_time:.2f} seconds.")

# Evaluate Random Forest classifiers
print("\nLexical Dataset Classification Report (Random Forest):")
print(classification_report(y_lexical_test, y_lexical_rf_pred, digits=4))

print("\nSyntactic Dataset Classification Report (Random Forest):")
print(classification_report(y_syntactic_test, y_syntactic_rf_pred, digits=4))
