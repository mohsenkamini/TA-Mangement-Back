# Generated by Django 5.1.3 on 2024-12-23 07:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0002_delete_course'),
        ('request', '0003_alter_request_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.student'),
        ),
    ]