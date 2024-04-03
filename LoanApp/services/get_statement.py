from datetime import datetime, timedelta
from decimal import Decimal
from django.http import JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import User, Payment, Loan
from .helper import calculate_statement
from ..constants import METHOD_NOT_ALLOWED, LOAN_DOES_NOT_EXIST, LOAN_IS_COMPLETED, LOAN_IS_REJECTED, COMLETED, REJECTED

@api_view(['GET'])
def get_user_statement(request):
    if request.method == 'GET':
        loan_id = request.GET.get('loan_id')

        try:
            loan = Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return JsonResponse({'error': LOAN_DOES_NOT_EXIST}, status=400)

        if loan.loan_status == COMLETED:
            return Response({'error': LOAN_IS_COMPLETED}, status=400)

        if loan.loan_status == REJECTED:
            return Response({'error': LOAN_IS_REJECTED}, status=400)

        # Retrieve past transactions
        past_transactions = []
        payments = Payment.objects.filter(loan=loan).order_by('payment_date')
        for payment in payments:
            past_transactions.append({
                'Date': payment.payment_date.strftime('%Y-%m-%d'),
                'Amount_paid': payment.amount,
            })

        # Calculate upcoming EMIs
        upcoming_transactions = []
        emi_date = loan.disbursement_date
        for _ in range(loan.term_period):
            upcoming_transactions.append({
                'Date': emi_date.strftime('%Y-%m-%d'),
                # 'Amount_due': loan.emi_amount, #to create a emi_amount field
            })
            emi_date += timedelta(days=30)  # Assuming monthly payments

        # Calculate current month's statement
        payment = calculate_statement(loan)
        current_date = datetime.now()
        principal_due = payment['Principal_due'] or 0
        interest_on_principal = payment['Interest_on_principal'] or 0
        repayment_of_principal = payment['Repayment_of_principal'] or 0

        statement = {
            'Error': None,
            'Past_transactions': past_transactions,
            'Upcoming_transactions': upcoming_transactions,
            'Principal_due': principal_due,
            'Interest_on_principal': interest_on_principal,
            'Repayment_of_principal': repayment_of_principal,
        }

        return JsonResponse(statement, status=200)

    else:
        return JsonResponse({'error': METHOD_NOT_ALLOWED}, status=405)