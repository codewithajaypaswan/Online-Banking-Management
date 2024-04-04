from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .services.user_registration import user_registration_service
from .services.apply_loan import user_apply_loan
from .services.make_payment import user_loan_payment
from .services.get_statement import get_user_statement

# Create your views here.
def index(request):
    return render(request, 'index.html')
    # return HttpResponse("this is home page")

def register(request):
    return render(request, 'register.html')

def loan(request):
    supported_loan_types = ['SELECT A LOAN TYPE', 'Car', 'Home', 'Education', 'Personal']
    context = {'supported_loan_types': supported_loan_types}
    return render(request, 'loan.html', context)

def statement(request):
    return render(request, 'statement.html')

def payment(request):
    return render(request, 'payment.html')

@api_view(['POST'])
def register_user(request):
    # Access the Django HttpRequest object from the DRF Request object
    django_request = request._request
    response = user_registration_service(django_request)  # Call the service function
    return response

@api_view(['POST'])
def apply_loan(request):
    # HttpResponse("this is loan page")
    django_request = request._request
    response = user_apply_loan(django_request)
    return response

@api_view(['POST'])
def make_payment(request):
    django_request = request._request
    response = user_loan_payment(django_request)
    return response

@api_view(['GET'])
def get_statement(request):
    if request.method == 'GET':
        django_request = request._request
        print(request)
        response = get_user_statement(django_request)
        return response