# Generated by Django 4.1.5 on 2023-01-18 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0007_remove_anime_aired_remove_anime_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='number_rating',
            field=models.IntegerField(default=0),
        ),
    ]
