# Generated by Django 5.0.3 on 2024-04-03 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LoanApp', '0008_rename_id_loan_loan_id_rename_id_payment_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='amount_paid_till_date',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='loan',
            name='loan_status',
            field=models.CharField(default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_type',
            field=models.CharField(max_length=10),
        ),
    ]
