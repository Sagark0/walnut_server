# Generated by Django 5.0 on 2023-12-12 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_alter_transaction_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='details',
            field=models.CharField(default='No Details'),
        ),
    ]
