# Generated by Django 5.0.1 on 2024-01-14 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_answer_correct'),
    ]

    operations = [
        migrations.AddField(
            model_name='soha',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
