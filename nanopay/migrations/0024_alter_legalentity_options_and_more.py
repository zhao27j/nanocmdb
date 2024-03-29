# Generated by Django 4.1.7 on 2023-05-06 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nanopay', '0023_remove_paymentterm_paid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='legalentity',
            options={'ordering': ['type']},
        ),
        migrations.RemoveField(
            model_name='contract',
            name='party_c_list',
        ),
        migrations.AlterField(
            model_name='contract',
            name='briefing',
            field=models.CharField(max_length=50, verbose_name='Briefing'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='type',
            field=models.CharField(choices=[('M', 'Maintenance'), ('N', 'New'), ('E', 'Expired')], default='M', max_length=1, verbose_name='Contract Type'),
        ),
    ]
