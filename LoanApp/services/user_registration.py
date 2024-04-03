from django.http import JsonResponse
from django.db import IntegrityError
from rest_framework import status
from ..models import User
from ..tasks import calculate_credit_score
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..constants import INCOMPLETE_DATA_PROVIDED, AADHAR_ALREADY_REGISTERED

@api_view(['POST'])
def user_registration_service(request):
    if request.method == 'POST':
        name = request.data.get('name')
        email = request.data.get('email')
        annual_income = request.data.get('annual_income')
        aadhar_id = request.data.get('aadhar_id')

        if not (name and email and annual_income and aadhar_id):
            return JsonResponse({"error": INCOMPLETE_DATA_PROVIDED}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create(name=name, email=email, annual_income=annual_income, aadhar_id=aadhar_id)
            # calculate_credit_score.delay(user.id)  # Trigger credit score calculation asynchronously
                                                   # TO run this we have to run redis-server and celery worker
            return JsonResponse({"unique_user_id": str(user.id), "error": None}, status=status.HTTP_200_OK)
        except IntegrityError as e:
            if 'UNIQUE constraint failed:' in str(e):
                return JsonResponse({"error": AADHAR_ALREADY_REGISTERED}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
