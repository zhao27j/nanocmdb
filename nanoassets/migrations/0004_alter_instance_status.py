# Generated by Django 4.1.7 on 2023-03-26 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nanoassets', '0003_alter_instance_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='status',
            field=models.CharField(choices=[('Maintenance', 'Maintenance'), ('Available', 'Available'), ('In use', 'In use')], default='Available', help_text='Asset availability', max_length=15),
        ),
    ]
