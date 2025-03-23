# Generated by Django 5.1.5 on 2025-01-31 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storybook', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'ordering': ['-generated_on'], 'verbose_name': 'Story', 'verbose_name_plural': 'Stories'},
        ),
        migrations.AddField(
            model_name='story',
            name='complete_story',
            field=models.TextField(blank=True, help_text='The entire generated story.'),
        ),
        migrations.AddField(
            model_name='story',
            name='current_passage',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='story',
            name='introduction',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='story',
            name='user_responses',
            field=models.TextField(blank=True, help_text="Stores the user's responses or decisions as a JSON string."),
        ),
        migrations.AlterField(
            model_name='story',
            name='question_type',
            field=models.CharField(default='short-answer', max_length=50),
        ),
        migrations.AlterField(
            model_name='story',
            name='word_limit',
            field=models.PositiveIntegerField(default=250),
        ),
        migrations.AlterModelTable(
            name='story',
            table='stories',
        ),
    ]
