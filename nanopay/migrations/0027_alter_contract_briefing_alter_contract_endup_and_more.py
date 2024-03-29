# Generated by Django 4.1.7 on 2023-05-08 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nanopay', '0026_alter_contract_options_alter_legalentity_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='briefing',
            field=models.CharField(max_length=50, null=True, verbose_name='Briefing'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='endup',
            field=models.DateField(null=True, verbose_name='End Up'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='startup',
            field=models.DateField(null=True, verbose_name='Start Up'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='type',
            field=models.CharField(choices=[('M', 'Maintenance'), ('N', 'New'), ('R', 'Rental'), ('E', 'Expired')], default='M', max_length=1, null=True, verbose_name='Contract Type'),
        ),
    ]
