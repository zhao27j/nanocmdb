# Generated by Django 4.1.7 on 2023-04-11 02:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nanoassets', '0039_alter_branchsite_onsitetech'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchsite',
            name='onSiteTech',
            field=models.ManyToManyField(limit_choices_to={'is_staff': True}, to=settings.AUTH_USER_MODEL, verbose_name='Onsite IT Support'),
        ),
    ]
