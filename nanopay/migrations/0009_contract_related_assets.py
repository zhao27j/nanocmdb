# Generated by Django 4.1.7 on 2023-05-04 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nanoassets', '0052_alter_activityhistory_options'),
        ('nanopay', '0008_remove_contract_assets'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='related_assets',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nanoassets.instance', verbose_name='Related Assets'),
        ),
    ]
