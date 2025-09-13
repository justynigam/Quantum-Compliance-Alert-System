from django.db import models
import uuid

class Transaction(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'pending'
        COMPLIANT = 'COMPLIANT', 'Compliant'
        HIGH_RISK = 'HIGH_RISK', 'High-Risk'
        BLOCKED = 'BLOCKED' , 'Blocked'

    class TransactionType(models.TextChoices):
        WIRE_TRANSFER = 'WIRE' , 'WireTransfer'
        EQUITY_TRADE = 'EQUITY' , 'Equity Trade'
        FX_SPOT = 'FX' , 'FX Spot'    
        CRYPTO = 'CRYPTO' , 'Crypto Trade'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4 , editable=False)
    transaction_id_str = models.CharField(max_length=100 , unique=True , db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        default=TransactionType.WIRE_TRANSFER
    )    

    amount = models.DecimalField(max_digits=19 , decimal_places=4)
    currency = models.CharField(max_length=5)

    client_name = models.CharField(max_length=255)
    source_account = models.CharField(max_length=100)
    destination_account = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )

    def __str__(self):
        return f"{self.transaction_id_str} - {self.amount} {self.currency} [{self.status}]"

    def to_feature_dict(self):
        return{
            'amount' : float(self.amount),
            'day_of_week': self.timestamp.weekday(),
            'hour_of_day': self.timestamp.hour,
            'is_crypto': 1 if self.transaction_type == self.TransactionType.CRYPTO else 0,
        }    

class XaiExplanation(models.Model):
       transaction = models.OneToOneField(
        Transaction, 
        on_delete=models.CASCADE,
        primary_key=True,
       )

       base_value = models.FloatField(null=True, blank=True)
       shap_values = models.JSONField()
       feature_names = models.JSONField()
       feature_values = models.JSONField()

       created_at = models.DateTimeField(auto_now_add=True)

       def __str__(self):
        return f"Explanation for {self.transaction.transaction_id_str}"
