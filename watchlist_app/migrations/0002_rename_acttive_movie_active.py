# Generated by Django 5.0.2 on 2024-03-21 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='acttive',
            new_name='active',
        ),
    ]
