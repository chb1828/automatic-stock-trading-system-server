# Generated by Django 3.1.4 on 2021-02-21 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0002_newskeyword'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newskeyword',
            old_name='news',
            new_name='url',
        ),
    ]
