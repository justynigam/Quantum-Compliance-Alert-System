import joblib
import os
import shap
import numpy as np
from django.conf import settings
from transactions.models import Transaction

class XAIService:
    """
    A service to load a trained model and generate explanations for its predictions.
    """
    _model = None
    _explainer = None

    def _load_model(self):
        """Loads the trained model and explainer from disk."""
        if XAIService._model is None:
            model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'risk_model.joblib')
            print(f"Loading model from: {model_path}")
            try:
                XAIService._model = joblib.load(model_path)
                print("Initializing explainer...")
                
                # Handle different model types
                if hasattr(XAIService._model, 'predict_proba'):  # Scikit-learn model
                    XAIService._explainer = shap.TreeExplainer(XAIService._model)
                elif hasattr(XAIService._model, 'named_modules'):  # PyTorch model
                    import torch
                    background = torch.randn(100, 4)  # Example background data
                    XAIService._explainer = shap.DeepExplainer(XAIService._model, background)
                else:
                    print("WARNING: Model type not fully supported - limited explainability")
                    
            except FileNotFoundError:
                print(f"ERROR: Model file not found at {model_path}")
            except Exception as e:
                print(f"Error loading model or explainer: {e}")

    def predict_status(self, features: dict):
        """
        Predicts the compliance status of a transaction using the loaded model
        and applies hard-coded business rules.
        """
        self._load_model()
        if XAIService._model is None:
            return Transaction.Status.PENDING, 0.0, 0

        # --- Business Rule ---
        is_crypto = features.get('is_crypto', 0) == 1
        amount = features.get('amount', 0.0)
        if is_crypto and amount > 100000.00:
            print("DEBUG: Business rule triggered! Forcing BLOCKED status.")
            return Transaction.Status.BLOCKED, 1.0, 1

        # --- ML Model Prediction ---
        feature_values = [
            features.get('amount', 0.0),
            features.get('day_of_week', 0),
            features.get('hour_of_day', 0),
            features.get('is_crypto', 0)
        ]

        try:
            # Handle different model types
            if hasattr(XAIService._model, 'predict_proba'):
                # Standard scikit-learn model
                probability = XAIService._model.predict_proba([feature_values])[0][1]
                prediction_raw = XAIService._model.predict([feature_values])[0]
            elif hasattr(XAIService._model, 'named_modules'):  # PyTorch model
                import torch
                feature_tensor = torch.tensor([feature_values], dtype=torch.float32)
                with torch.no_grad():
                    prediction = XAIService._model(feature_tensor)
                probability = float(torch.sigmoid(prediction).item())
                prediction_raw = 1 if probability > 0.5 else 0
            elif hasattr(XAIService._model, 'predict'):
                # Keras or other models with predict method
                prediction = XAIService._model.predict([feature_values])[0]
                probability = float(prediction[0]) if isinstance(prediction, (list, np.ndarray)) else float(prediction)
                prediction_raw = 1 if probability > 0.5 else 0
            else:
                raise AttributeError("Model doesn't support required prediction methods")

            if probability > 0.8:
                predicted_status = Transaction.Status.BLOCKED
            elif probability > 0.5:
                predicted_status = Transaction.Status.HIGH_RISK
            else:
                predicted_status = Transaction.Status.COMPLIANT
        
            return predicted_status, probability, prediction_raw

        except Exception as e:
            print(f"Error during prediction: {e}")
            return Transaction.Status.PENDING, 0.0, 0

    def generate_explanation(self, features: dict) -> dict:
        """Generates a SHAP explanation for a single transaction."""
        self._load_model()
        if XAIService._explainer is None:
            return {}

        feature_values = [
            features.get('amount', 0.0),
            features.get('day_of_week', 0),
            features.get('hour_of_day', 0),
            features.get('is_crypto', 0)
        ]
        
        try:
            if hasattr(XAIService._model, 'named_modules'):  # PyTorch model
                import torch
                input_tensor = torch.tensor([feature_values], dtype=torch.float32)
                shap_values = XAIService._explainer.shap_values(input_tensor)
                return {
                    "base_value": float(XAIService._explainer.expected_value),
                    "shap_values": [float(v) for v in shap_values[0]],
                    "feature_names": ['amount', 'day_of_week', 'hour_of_day', 'is_crypto'],
                    "feature_values": feature_values,
                }
            else:  # Other model types
                shap_values = XAIService._explainer.shap_values([feature_values])
                return {
                    "base_value": float(XAIService._explainer.expected_value),
                    "shap_values": shap_values[0].tolist(),
                    "feature_names": ['amount', 'day_of_week', 'hour_of_day', 'is_crypto'],
                    "feature_values": feature_values,
                }
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return {}
