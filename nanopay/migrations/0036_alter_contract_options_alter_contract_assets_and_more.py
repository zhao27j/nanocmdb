# Generated by Django 4.1.7 on 2023-05-16 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import nanopay.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nanoassets', '0053_activityhistory_contract'),
        ('nanopay', '0035_alter_contract_briefing'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contract',
            options={'ordering': ['-startup']},
        ),
        migrations.AlterField(
            model_name='contract',
            name='assets',
            field=models.ManyToManyField(blank=True, to='nanoassets.instance'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='briefing',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contract',
            name='endup',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='party_a_list',
            field=models.ManyToManyField(related_name='partyas', to='nanopay.legalentity'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='party_b_list',
            field=models.ManyToManyField(related_name='partybs', to='nanopay.legalentity'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='scanned_copy',
            field=models.FileField(blank=True, null=True, upload_to=nanopay.models.contract_scanned_copy_path),
        ),
        migrations.AlterField(
            model_name='contract',
            name='startup',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='type',
            field=models.CharField(choices=[('M', 'Maintenance'), ('N', 'New'), ('R', 'Rental'), ('E', 'Expired'), ('T', 'Terminated')], default='M', max_length=1),
        ),
    ]
