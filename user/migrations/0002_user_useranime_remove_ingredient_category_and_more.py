# Generated by Django 4.1.2 on 2022-11-04 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('grade', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='UserAnime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anime', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('notes', models.TextField()),
                ('currently_watching', models.BooleanField()),
                ('watchlist', models.BooleanField()),
                ('finished_anime', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
        migrations.AddField(
            model_name='user',
            name='place',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.useranime'),
        ),
    ]
