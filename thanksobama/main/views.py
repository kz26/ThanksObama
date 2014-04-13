from rest_framework.views import APIView
from rest_framework.response import Response
import questions

# Create your views here.

class NewQuestion(APIView):
	def get(self, request, *args, **kwargs):
		return Response(questions.gen_question())
