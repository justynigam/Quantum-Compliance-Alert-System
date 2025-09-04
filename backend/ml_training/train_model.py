# backend/ml_training/train_model.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os
import numpy as np

def train_and_save_model():
    """
    This function simulates the model training process.
    It creates dummy data, trains a RandomForest model,
    and saves it to the ml_models directory.
    """
    print("Starting model training process...")

    # --- 1. Generate Sample Data ---
    # In a real project, you would load this from your database.
    np.random.seed(42)  # For reproducible results
    
    # Generate base features
    amounts = np.random.uniform(100, 100000, 1000)
    hours = np.random.randint(0, 24, 1000)
    is_crypto = np.random.randint(0, 2, 1000)
    
    # Create realistic risk patterns
    status = []
    for i in range(1000):
        # High risk conditions
        if (amounts[i] > 50000 or  # Large amounts
            (hours[i] < 6 or hours[i] > 22) or  # Unusual hours
            is_crypto[i] == 1):  # Crypto transactions
            status.append(np.random.choice(['HIGH_RISK', 'BLOCKED'], p=[0.7, 0.3]))
        else:
            status.append('COMPLIANT')
    
    data = {
        'amount': amounts,
        'hour_of_day': hours,
        'is_crypto': is_crypto,
        'status': status
    }
    df = pd.DataFrame(data)
    print(f"Generated a sample dataset with {len(df)} rows.")

    # --- 2. Feature Engineering & Preprocessing ---
    # Convert categorical status to numerical labels for the model
    X = df[['amount', 'hour_of_day', 'is_crypto']]
    y = df['status']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("Split data into training and testing sets.")

    # --- 3. Model Training ---
    print("Training a RandomForestClassifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    print("Model training complete.")

    # --- 4. Model Evaluation ---
    print("\nEvaluating model performance on the test set:")
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # --- 5. Save the Trained Model ---
    # Ensure the ml_models directory exists
    model_dir = 'ml_models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    
    model_path = os.path.join(model_dir, 'risk_model.joblib')
    joblib.dump(model, model_path)
    
    print(f"\nModel successfully saved to: {model_path}")

if __name__ == '__main__':
    train_and_save_model()