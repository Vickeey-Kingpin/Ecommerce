# Generated by Django 5.1.2 on 2024-11-29 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('istreetapp', '0012_refund'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='refund_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
