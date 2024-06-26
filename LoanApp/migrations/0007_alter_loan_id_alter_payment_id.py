# Generated by Django 5.0.3 on 2024-04-02 20:44

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LoanApp', '0006_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
