# Generated by Django 3.1.4 on 2021-02-21 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0004_auto_20210221_0536'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='posted_date',
            field=models.DateTimeField(default='2021-02-21 00:00:00', verbose_name='posted_date'),
            preserve_default=False,
        ),
    ]
