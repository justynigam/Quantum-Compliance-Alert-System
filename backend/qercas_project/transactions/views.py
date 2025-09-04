from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Transaction, XaiExplanation
from .serializers import TransactionSerializer, XaiExplanationSerializer
from .tasks import analyze_transaction_risk


class TransactionList(APIView):
    def get(self,request,format=None):
        transaction = Transaction.objects.all().order_by('-timestamp')
        serializer = TransactionSerializer(transaction , many=True)

        return Response(serializer.data)

    def post(self, request , format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()

            analyze_transaction_risk.delay(transaction.id)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class TransactionDetail(APIView):
    """
    Retrieve a single transaction instance.
    """
    def get_object(self, pk):
        try:
            # We use the UUID primary key (pk) to find the transaction
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

class ExplanationDetail(APIView):
     def get(self, request, pk, format=None):
        try:
            # Find the explanation linked to the transaction's primary key (pk)
            explanation = XaiExplanation.objects.get(transaction_id=pk)
            serializer = XaiExplanationSerializer(explanation)
            return Response(serializer.data)
        except XaiExplanation.DoesNotExist:
            return Response(
                {"error": "Explanation not found or not yet generated."},
                status=status.HTTP_404_NOT_FOUND
            )
