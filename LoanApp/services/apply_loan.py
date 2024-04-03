from decimal import Decimal
from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import User, Payment, Loan
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from .helper import calculate_emi, calculate_due_dates
from ..constants import SUPPORTED_LOAN_TYPES, USER_NOT_EXIST, INSUFFICIENT_CREDIT_SCORE, INSUFFICIENT_ANNUAL_INCOME, LOAN_AMOUNT_EXCEEDS_BOUNDS, EMI_EXCEEDS_MONTHLY_INCOME, LOAN_AMOUNT_BOUNDS

@api_view(['POST'])
def user_apply_loan(request):
    if request.method == 'POST':
        unique_user_id = request.data.get('unique_user_id')
        loan_type = request.data.get('loan_type')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        term_period = request.data.get('term_period')
        disbursement_date = request.data.get('disbursement_date')

        if loan_type not in SUPPORTED_LOAN_TYPES:
            return JsonResponse({"error": f"Unsupported loan type. Supported types: {', '.join(SUPPORTED_LOAN_TYPES)}"}, status=400)

        try:
            user = User.objects.get(id=unique_user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': USER_NOT_EXIST}, status=400)

        # Validate credit score
        if user.credit_score < 450:
            return JsonResponse({'error': INSUFFICIENT_CREDIT_SCORE}, status=400)
        # Validate user income
        if user.annual_income < 150000:
            return JsonResponse({'error': INSUFFICIENT_ANNUAL_INCOME}, status=400)

        # Validate loan amount bounds based on loan type
        loan_amount = int(loan_amount)
        if loan_amount > LOAN_AMOUNT_BOUNDS.get(loan_type, 0):
            return JsonResponse({'error': LOAN_AMOUNT_EXCEEDS_BOUNDS}, status=400)

        # Calculate EMIs
        emi = calculate_emi(loan_amount, float(interest_rate), int(term_period))
        monthly_income = user.annual_income  / 12
        max_emi = float(monthly_income) * 0.6  # Max EMI is 60% of monthly income
        if emi > max_emi:
            return JsonResponse({'error': EMI_EXCEEDS_MONTHLY_INCOME}, status=400)

        # Interest is incurred starting from the next day of disbursal
        disbursement_date = datetime.strptime(disbursement_date, '%Y-%m-%d')
        start_date = disbursement_date + timedelta(days=1)

        loan = Loan.objects.create(
            user=user,
            loan_type=loan_type,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            term_period=term_period,
            disbursement_date=disbursement_date,
            emi_amount = emi
        )

        response_data = {
            'Loan_id': loan.loan_id,
            'Due_dates': calculate_due_dates(start_date, int(term_period), emi)
        }
        return JsonResponse(response_data, status=200)
