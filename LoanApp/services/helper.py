
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from ..models import Payment

def calculate_due_dates(start_date, term_period, emi):
    due_dates = []
    current_date = start_date
    for _ in range(term_period):
        due_dates.append({
            'Date': current_date.strftime('%Y-%m-%d'),
            'Amount_due': emi
        })
        current_date += relativedelta(months=1)
    return due_dates

def calculate_emi(principal, rate, time_period):
    rate = rate / 100 / 12  
    emi = (principal * rate * (1 + rate) ** time_period) / ((1 + rate) ** time_period - 1)
    return round(emi, 2)

def calculate_statement(loan):

    payments = Payment.objects.filter(loan=loan).order_by('payment_date')
    total_paid = sum(payment.amount for payment in payments)
    principal_due = loan.loan_amount - total_paid
    interest_rate = loan.interest_rate / Decimal(100)
    interest_on_principal = principal_due * interest_rate
    # Calculate the repayment of principal for the current month
    repayment_of_principal = loan.emi_amount - interest_on_principal

    return {
        'Principal_due': principal_due,
        'Interest_on_principal': interest_on_principal,
        'Repayment_of_principal': repayment_of_principal,
    }