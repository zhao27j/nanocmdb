# Generated by Django 4.1.7 on 2023-06-05 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nanobase', '0004_alter_userprofile_dept_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='work_phone',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True, verbose_name='Work Phone'),
        ),
    ]
