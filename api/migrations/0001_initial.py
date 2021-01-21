# Generated by Django 3.1.4 on 2021-01-21 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('code', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('cnt', models.BigIntegerField()),
                ('construction', models.CharField(max_length=64)),
                ('listedDate', models.DateTimeField()),
                ('lastPrice', models.CharField(max_length=64)),
                ('state', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'stock',
            },
        ),
    ]
