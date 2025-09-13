from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import NLPService

class RegulatorySearchView(APIView):
    """
    An API endpoint that accepts a question and returns an answer
    from the NLP service.
    """
    def post(self, request, *args, **kwargs):
        question = request.data.get('question')
        if not question:
            return Response(
                {"error": "A 'question' field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        answer = NLPService.answer_question(question)
        return Response({"answer": answer}, status=status.HTTP_200_OK)