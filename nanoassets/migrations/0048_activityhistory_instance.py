# Generated by Django 4.1.7 on 2023-04-14 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nanoassets', '0047_activityhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityhistory',
            name='Instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nanoassets.instance', verbose_name=''),
        ),
    ]
