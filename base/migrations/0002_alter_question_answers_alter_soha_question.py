# Generated by Django 5.0.1 on 2024-01-14 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='answers',
            field=models.ManyToManyField(blank=True, to='base.answer'),
        ),
        migrations.AlterField(
            model_name='soha',
            name='question',
            field=models.ManyToManyField(blank=True, to='base.question'),
        ),
    ]
