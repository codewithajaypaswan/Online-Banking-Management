# Generated by Django 5.0.3 on 2024-04-03 03:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LoanApp', '0007_alter_loan_id_alter_payment_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='id',
            new_name='loan_id',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='id',
            new_name='payment_id',
        ),
    ]
