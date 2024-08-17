import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Preprocessing functions
def preprocess_categorical_columns(df, categorical_columns):
    label_encoders = {}
    for col in categorical_columns:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            label_encoders[col] = le
            logging.debug(f"Encoded column {col} with unique values: {df[col].unique()}")
    return df, label_encoders

def preprocess_lexical_data(df):
    df['TokenID'].fillna(0, inplace=True)
    df['TokenValue'].fillna('', inplace=True)
    df['TokenID'] = df['TokenID'].astype(int)
    logging.debug(f"Preprocessed TokenID column: {df['TokenID'].head()}")
    df, label_encoders = preprocess_categorical_columns(df, ['TokenValue'])
    logging.debug(f"Preprocessed lexical data: {df.head()}")
    return df, label_encoders

def preprocess_syntactic_data(df):
    df['FeatureID'].fillna(0, inplace=True)
    df['Feature'].fillna('', inplace=True)
    df['FeatureID'] = df['FeatureID'].astype(int)
    logging.debug(f"Preprocessed FeatureID column: {df['FeatureID'].head()}")
    df, label_encoders = preprocess_categorical_columns(df, ['Feature'])
    logging.debug(f"Preprocessed syntactic data: {df.head()}")
    return df, label_encoders

# Load and preprocess datasets
logging.info("Loading datasets...")
df_lexical = pd.read_csv("lexical_dataset_alternate.csv")
df_syntactic = pd.read_csv("syntactic_dataset_alternate.csv")

df_lexical, lexical_encoders = preprocess_lexical_data(df_lexical)
df_syntactic, syntactic_encoders = preprocess_syntactic_data(df_syntactic)

# Save label encoders
joblib.dump(lexical_encoders['TokenValue'], 'label_encoder_TokenValues.pkl')
joblib.dump(syntactic_encoders['Feature'], 'label_encoder_Features.pkl')
logging.info("Label encoders saved.")

# Prepare features and target
X_lexical = df_lexical.drop(columns=['Target', 'Filename', 'TokenID'])
y_lexical = df_lexical['Target']

X_syntactic = df_syntactic.drop(columns=['Target', 'Filename', 'FeatureID'])
y_syntactic = df_syntactic['Target']

logging.debug(f"Lexical features shape: {X_lexical.shape}")
logging.debug(f"Syntactic features shape: {X_syntactic.shape}")

# Apply PCA
pca_lexical = PCA(n_components=min(50, X_lexical.shape[1]))
X_lexical_pca = pca_lexical.fit_transform(X_lexical)
joblib.dump(pca_lexical, 'pca_lexical.pkl')
logging.info(f"PCA applied to lexical data. Explained variance ratio: {pca_lexical.explained_variance_ratio_}")

pca_syntactic = PCA(n_components=min(50, X_syntactic.shape[1]))
X_syntactic_pca = pca_syntactic.fit_transform(X_syntactic)
joblib.dump(pca_syntactic, 'pca_syntactic.pkl')
logging.info(f"PCA applied to syntactic data. Explained variance ratio: {pca_syntactic.explained_variance_ratio_}")

# Split data
X_lexical_train, X_lexical_test, y_lexical_train, y_lexical_test = train_test_split(X_lexical_pca, y_lexical, test_size=0.2, random_state=42)
X_syntactic_train, X_syntactic_test, y_syntactic_train, y_syntactic_test = train_test_split(X_syntactic_pca, y_syntactic, test_size=0.2, random_state=42)
logging.info(f"Data split: Lexical train shape: {X_lexical_train.shape}, Syntactic train shape: {X_syntactic_train.shape}")

# Apply SMOTE
smote_lexical = SMOTE(random_state=42)
X_lexical_train_res, y_lexical_train_res = smote_lexical.fit_resample(X_lexical_train, y_lexical_train)
logging.debug(f"After SMOTE: Lexical train shape: {X_lexical_train_res.shape}")

smote_syntactic = SMOTE(random_state=42)
X_syntactic_train_res, y_syntactic_train_res = smote_syntactic.fit_resample(X_syntactic_train, y_syntactic_train)
logging.debug(f"After SMOTE: Syntactic train shape: {X_syntactic_train_res.shape}")

# Train and save Logistic Regression models
clf_lexical_lr = LogisticRegression(random_state=42)
clf_syntactic_lr = LogisticRegression(random_state=42)

logging.info("Training Logistic Regression model on lexical data...")
clf_lexical_lr.fit(X_lexical_train_res, y_lexical_train_res)
logging.info("Training Logistic Regression model on syntactic data...")
clf_syntactic_lr.fit(X_syntactic_train_res, y_syntactic_train_res)

joblib.dump(clf_lexical_lr, 'lr_lexical.pkl')
joblib.dump(clf_syntactic_lr, 'lr_syntactic.pkl')
logging.info("Logistic Regression models saved.")

# Predictions and evaluation
y_lexical_lr_pred = clf_lexical_lr.predict(X_lexical_test)
y_syntactic_lr_pred = clf_syntactic_lr.predict(X_syntactic_test)

logging.info("Generating classification reports...")
print("\nLexical Dataset Classification Report (Logistic Regression):")
print(classification_report(y_lexical_test, y_lexical_lr_pred))

print("\nSyntactic Dataset Classification Report (Logistic Regression):")
print(classification_report(y_syntactic_test, y_syntactic_lr_pred))
