# Generated by Django 4.1.7 on 2023-12-22 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nanopay', '0078_alter_nonpayrollexpense_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentterm',
            options={'ordering': ['contract', '-pay_day']},
        ),
    ]
