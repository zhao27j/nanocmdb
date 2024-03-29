# Generated by Django 4.1.7 on 2023-03-30 01:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('nanoassets', '0007_alter_scraprequest_case_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instance',
            options={'ordering': ['model_type', 'eol_date']},
        ),
        migrations.AlterField(
            model_name='scraprequest',
            name='case_id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for the particular request', primary_key=True, serialize=False, verbose_name='Request case ID'),
        ),
        migrations.AlterField(
            model_name='scraprequest',
            name='requested_on',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Requested on'),
        ),
    ]
