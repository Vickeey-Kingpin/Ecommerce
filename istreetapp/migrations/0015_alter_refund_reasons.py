# Generated by Django 5.1.2 on 2024-11-29 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('istreetapp', '0014_order_refund_granted_order_refund_requested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refund',
            name='reasons',
            field=models.TextField(blank=True, null=True),
        ),
    ]
