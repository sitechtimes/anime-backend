# Generated by Django 4.1.3 on 2022-11-12 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Awards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('award_name', models.CharField(max_length=255)),
                ('award_description', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='AnimeAwards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nominated_for_award', models.BooleanField()),
                ('has_award', models.BooleanField()),
                ('anime_award_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='anime.awards')),
            ],
        ),
        migrations.AddField(
            model_name='anime',
            name='anime_awards',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='anime.animeawards'),
        ),
    ]
