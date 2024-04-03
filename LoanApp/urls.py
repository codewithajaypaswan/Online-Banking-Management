from django.contrib import admin
from django.urls import path
from LoanApp import views
from .views import register_user, apply_loan, make_payment, get_statement, register, loan, payment, statement

urlpatterns = [
    path('', views.index, name="home"),
    path('api/register-user', register_user, name='register_user'),
    path('api/apply-loan', apply_loan, name='apply_loan'),
    path('api/make-payment', make_payment, name='make_payment'),
    path('api/get-statement/', get_statement, name='get_statement'),

    path('register', register, name='register'),
    path('loan', loan, name='loan'),
    path('payment', payment, name='payment'),
    path('statement', statement, name='statement'),
]