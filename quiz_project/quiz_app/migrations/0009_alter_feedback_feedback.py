# Generated by Django 3.2.8 on 2021-11-09 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0008_feedback_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='feedback',
            field=models.TextField(blank=True, max_length=2000, null=True),
        ),
    ]
