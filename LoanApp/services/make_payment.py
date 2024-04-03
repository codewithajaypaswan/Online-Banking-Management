from datetime import datetime
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Payment, Loan
from .helper import calculate_emi, calculate_due_dates
from ..constants import MISSING_REQUIRED_FILED, PAYMENT_DONE_MESSAGE, PAYMENT_ALREADY_MADE, PREVIOUS_EMI_DUE

@api_view(['POST'])
def user_loan_payment(request):
    loan_id = request.data.get('loan_id')
    amount = request.data.get('amount')
    payment_date = request.data.get('payment_date')

    if not all([loan_id, amount, payment_date]):
        return JsonResponse({'error': MISSING_REQUIRED_FILED}, status=400)

    # if payment is already made for that date
    if Payment.objects.filter(loan=loan_id, payment_date=payment_date).exists():
        return JsonResponse({'error': PAYMENT_ALREADY_MADE}, status=400)

    # if previous EMIs are due
    loan = Loan.objects.get(loan_id=loan_id)
    if loan.is_previous_emis_due():
        return JsonResponse({'error': PREVIOUS_EMI_DUE}, status=400)

    # Recalculate EMI amount if the amount being paid is less/more than the due installment amount
    emi_amount = loan.emi_amount
    payment_date = datetime.strptime(payment_date, '%Y-%m-%d')
    if amount != emi_amount:
        emi_amount = calculate_emi(float(amount), float(loan.interest_rate), int(loan.term_period))
    loan.amount_paid_till_date = float(loan.amount_paid_till_date) + float(amount)
    Payment.objects.create(
        loan_id=loan_id,
        amount=amount,
        payment_date=payment_date
    )

    return JsonResponse({'message': PAYMENT_DONE_MESSAGE}, status=200)
