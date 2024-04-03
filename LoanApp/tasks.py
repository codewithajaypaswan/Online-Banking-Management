from celery import shared_task
from .models import User, Transaction
from django.db.models import Sum


@shared_task
def calculate_credit_score(user_id):
    user = User.objects.get(pk=user_id)
    credit = Transaction.objects.filter(user=user, transaction_type='CREDIT').aggregate(
        credit=Sum('amount')
    )['credit'] or 0
    debit = Transaction.objects.filter(user=user, transaction_type='DEBIT').aggregate(
        debit=Sum('amount')
    )['debit'] or 0
    account_balance = credit - debit

    if account_balance >= 1000000:
        user.credit_score = 900
    elif account_balance <= 100000:
        user.credit_score = 300
    else:
        user.credit_score = 300 + ((account_balance - 100000) // 15000) * 10

    user.save()
