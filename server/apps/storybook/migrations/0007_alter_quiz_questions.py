# Generated by Django 5.1.5 on 2025-02-01 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storybook', '0006_quiz_total_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='questions',
            field=models.JSONField(help_text='Stores questions with options and correct answers in JSON format.'),
        ),
    ]
