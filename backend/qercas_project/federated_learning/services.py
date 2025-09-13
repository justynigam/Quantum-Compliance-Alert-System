import torch
import torch.nn as nn
import torch.optim as optim
import joblib
import os
from django.conf import settings

class FederatedTrainingService:
    """
    Simulates a federated learning cycle to train the risk model.
    """
    @staticmethod
    def get_simulated_data_for_bank():
        """Creates some dummy data representing a bank's private transactions."""
        data = torch.randn(100, 4)
        labels = torch.randint(0, 2, (100, 1)).float()
        return data, labels

    @staticmethod
    def run_training_cycle():
        print("--- Starting Federated Learning Training Cycle ---")
        
        model = nn.Sequential(
            nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 1), nn.Sigmoid()
        )

        bank_1_data, bank_1_labels = FederatedTrainingService.get_simulated_data_for_bank()
        bank_2_data, bank_2_labels = FederatedTrainingService.get_simulated_data_for_bank()
        
        optimizer = optim.SGD(model.parameters(), lr=0.01)
        criterion = nn.BCELoss()

        print("Training on Bank 1's private data...")
        optimizer.zero_grad()
        output = model(bank_1_data)
        loss = criterion(output, bank_1_labels)
        loss.backward()
        optimizer.step()

        print("Training on Bank 2's private data...")
        optimizer.zero_grad()
        output = model(bank_2_data)
        loss = criterion(output, bank_2_labels)
        loss.backward()
        optimizer.step()
        
        model_dir = os.path.join(settings.BASE_DIR, 'ml_models')
        os.makedirs(model_dir, exist_ok=True)
        model_path = os.path.join(model_dir, "risk_model.joblib")
        joblib.dump(model, model_path)
        
        print(f"\n--- Federated training complete. New aggregated model saved to: {model_path} ---")
        return model_path
