# Generated by Django 4.1.5 on 2023-03-20 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0017_anime_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='avg_rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
