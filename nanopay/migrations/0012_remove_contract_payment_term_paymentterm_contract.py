# Generated by Django 4.1.7 on 2023-05-04 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nanopay', '0011_alter_contract_endup_alter_contract_startup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='payment_term',
        ),
        migrations.AddField(
            model_name='paymentterm',
            name='contract',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='nanopay.contract', verbose_name=''),
        ),
    ]
