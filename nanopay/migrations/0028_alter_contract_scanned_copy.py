# Generated by Django 4.1.7 on 2023-05-08 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nanopay', '0027_alter_contract_briefing_alter_contract_endup_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='scanned_copy',
            field=models.FileField(blank=True, null=True, upload_to='contract_scanned_copy/', verbose_name='Scanned Copy'),
        ),
    ]
