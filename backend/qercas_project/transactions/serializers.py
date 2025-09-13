from rest_framework import serializers
from .models import Transaction , XaiExplanation

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class XaiExplanationSerializer(serializers.ModelSerializer):
    class Meta:
        model = XaiExplanation
        fields = ['base_value','shap_values' , 'feature_names','feature_values']