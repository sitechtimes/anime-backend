# Generated by Django 4.1.3 on 2022-12-21 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0006_alter_anime_aired_alter_anime_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anime',
            name='aired',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='status',
        ),
    ]
