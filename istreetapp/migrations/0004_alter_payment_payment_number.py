# Generated by Django 5.1.2 on 2024-11-28 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('istreetapp', '0003_payment_payment_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_number',
            field=models.CharField(max_length=10),
        ),
    ]
