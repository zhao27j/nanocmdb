# Generated by Django 4.1.7 on 2023-04-27 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nanoassets', '0051_alter_branchsite_city'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activityhistory',
            options={'ordering': ['-description']},
        ),
    ]
