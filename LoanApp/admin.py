from django.contrib import admin
from LoanApp.models import User, Transaction, Loan, Payment

# Register your models here.
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Loan)
admin.site.register(Payment)
