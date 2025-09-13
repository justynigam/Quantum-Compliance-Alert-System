from celery import shared_task
from xai_engine.services import XAIService
from gnn_analyzer.services import GNNService
from privacy_vault.services import CryptoService
from .models import Transaction, XaiExplanation

@shared_task(name="transactions.analyze_transaction_risk")
def analyze_transaction_risk(transaction_id):
    """
    Celery task to analyze a transaction's risk and trigger advanced analytics.
    """
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        
        # --- XAI Analysis ---
        features = transaction.to_feature_dict()
        service = XAIService()
        predicted_status, probability, _ = service.predict_status(features)
        transaction.status = predicted_status
        transaction.save()

        # Generate explanation for risky transactions
        if predicted_status in [Transaction.Status.HIGH_RISK, Transaction.Status.BLOCKED]:
            explanation_data = service.generate_explanation(features)
            
            if explanation_data and explanation_data.get("base_value") is not None:
                XaiExplanation.objects.create(
                    transaction=transaction,
                    **explanation_data
                )
            else:
                print(f"WARNING: Could not generate explanation for transaction {transaction.id}. Skipping.")
        
        # --- GNN Analysis ---
        # FIX: Use the 'predicted_status' variable for a reliable check
        if predicted_status in [Transaction.Status.HIGH_RISK, Transaction.Status.BLOCKED]:
            GNNService.analyze_and_generate_graph(transaction.id)

        # --- PQC TEST ---
        if predicted_status == Transaction.Status.BLOCKED:
            print("\n--- PQC TEST: Securing critical transaction note with PQC ---")
            try:
                public_key, secret_key = CryptoService.generate_pqc_keys()
                note = f"Urgent review needed for transaction {transaction.transaction_id_str}"
                encrypted_note_ciphertext = CryptoService.encrypt_pqc(public_key, note)
                print(f"Encrypted Note (Ciphertext): {encrypted_note_ciphertext[:30]}...")
                CryptoService.decrypt_pqc(secret_key, encrypted_note_ciphertext)
                print("--- PQC TEST: Decryption successful. ---")
            except Exception as e:
                print(f"PQC operation failed: {e}")

        return f"Transaction {transaction.transaction_id_str} status updated to {transaction.status}"
        
    except Transaction.DoesNotExist:
        return f"Transaction with id {transaction_id} not found."