# Generated by Django 4.1.5 on 2023-02-06 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0011_remove_animeawards_anime_award_name_and_more'),
        ('users', '0012_remove_userprofile_user_voted_animes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_voted_animes',
            field=models.ManyToManyField(blank=True, to='anime.animeawards'),
        ),
    ]
