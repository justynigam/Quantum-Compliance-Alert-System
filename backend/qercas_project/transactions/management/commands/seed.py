import random
from django.core.management.base import BaseCommand
from transactions.models import Transaction, XaiExplanation
from decimal import Decimal
from xai_engine.services import XAIService

class Command(BaseCommand):
    help = 'Seeds the database with sample transactions and explanations for development.'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        XaiExplanation.objects.all().delete()
        Transaction.objects.all().delete()

        sample_data = [
            {'id': 'TXN789012', 'type': Transaction.TransactionType.WIRE_TRANSFER, 'amount': '550000.00', 'client': 'Global Innovations Inc.', 'status': Transaction.Status.BLOCKED},
            {'id': 'TXN456789', 'type': Transaction.TransactionType.EQUITY_TRADE, 'amount': '1200000.00', 'client': 'Quantum Dynamics Ltd.', 'status': Transaction.Status.HIGH_RISK},
            {'id': 'TXN123456', 'type': Transaction.TransactionType.FX_SPOT, 'amount': '75000.00', 'client': 'Secure Holdings Co.', 'status': Transaction.Status.COMPLIANT},
            {'id': 'TXN987654', 'type': Transaction.TransactionType.CRYPTO, 'amount': '15000.50', 'client': 'Crypto Ventures', 'status': Transaction.Status.HIGH_RISK},
            {'id': 'TXN321654', 'type': Transaction.TransactionType.WIRE_TRANSFER, 'amount': '5200.00', 'client': 'Local Goods LLC', 'status': Transaction.Status.COMPLIANT},
        ]

        # First, create and save all transactions
        transactions_created = []
        for data in sample_data:
            transaction = Transaction.objects.create(
                transaction_id_str=data['id'],
                transaction_type=data['type'],
                amount=Decimal(data['amount']),
                currency='USD',
                client_name=data['client'],
                source_account=f'ACC{random.randint(10000, 99999)}',
                destination_account=f'ACC{random.randint(10000, 99999)}',
                status=data['status']
            )
            transactions_created.append(transaction)

        # Then, create explanations for risky transactions
        explanations_created = 0
        xai_service = XAIService()  # Create an instance
        for transaction in transactions_created:
            if transaction.status in [Transaction.Status.HIGH_RISK, Transaction.Status.BLOCKED]:
                try:
                    features = transaction.to_feature_dict()
                    explanation_data = xai_service.generate_explanation(features)  # Use instance method
                    
                    if explanation_data:
                        XaiExplanation.objects.create(
                            transaction=transaction,
                            base_value=explanation_data['base_value'],
                            shap_values=explanation_data['shap_values'],
                            feature_names=explanation_data['feature_names'],
                            feature_values=explanation_data['feature_values']
                        )
                        explanations_created += 1
                except Exception as e:
                    self.stdout.write(f"Could not create explanation for {transaction.transaction_id_str}: {e}")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(transactions_created)} transactions and {explanations_created} explanations.')
        )
