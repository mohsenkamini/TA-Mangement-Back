# Generated by Django 5.1.3 on 2024-12-22 12:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0002_course_condition'),
        ('faculty', '0002_delete_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Pending'), ('C', 'Complete'), ('F', 'Failed')], default='P', max_length=1)),
                ('date', models.DateField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='faculty.student')),
            ],
        ),
    ]
