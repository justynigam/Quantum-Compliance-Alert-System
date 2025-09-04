# backend/xai_engine/services.py

import joblib
import pandas as pd
import shap
# We will import Transaction inside the method to avoid circular import
# from transactions.models import Transaction 
import os
import numpy as np

class XAIService:
    _model = None
    _explainer = None

    @classmethod
    def _load_model(cls):
        """Loads the pre-trained model from disk. Caches it in memory."""
        if cls._model is None:
            model_path = os.path.join('..', 'ml_models', 'risk_model.joblib')
            try:
                print(f"Loading model from: {model_path}")
                cls._model = joblib.load(model_path)
            except FileNotFoundError:
                print(f"ERROR: Model file not found at {model_path}. Please run the training script.")
                return None
        return cls._model

    @classmethod
    def _get_explainer(cls):
        """Creates a SHAP explainer from the loaded model."""
        if cls._explainer is None:
            model = cls._load_model()
            if model:
                print("Creating SHAP TreeExplainer...")
                cls._explainer = shap.TreeExplainer(model)
        return cls._explainer

    @classmethod
    def predict_status(cls, transaction_features: dict) -> str:
        """
        Predicts the compliance status using the real, trained model.
        """
        # --- FIX: Import here to prevent circular dependency ---
        from transactions.models import Transaction
        
        model = cls._load_model()
        if not model:
            return Transaction.Status.PENDING

        feature_df = pd.DataFrame([transaction_features])[['amount', 'hour_of_day', 'is_crypto']]
        
        prediction = model.predict(feature_df)
        return prediction[0]

    @classmethod
    def generate_explanation(cls, transaction_features: dict) -> dict:
        """
        Generates a real SHAP explanation for a single transaction.
        """
        explainer = cls._get_explainer()
        if not explainer:
            return None

        feature_df = pd.DataFrame([transaction_features])[['amount', 'hour_of_day', 'is_crypto']]
        
        shap_values = explainer(feature_df)
        
        # Handle base_value - it might be an array, so take the mean
        base_val = shap_values.base_values
        if isinstance(base_val, np.ndarray):
            base_value = float(base_val.mean())
        else:
            base_value = float(base_val)
        
        explanation_data = {
            "base_value": base_value,
            "shap_values": shap_values.values[0].tolist(),
            "feature_names": feature_df.columns.tolist(),
            "feature_values": shap_values.data[0].tolist(),
        }
        return explanation_data
