# Generated by Django 2.1.7 on 2019-04-02 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0022_auto_20190401_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='blacklist',
            field=models.BooleanField(default=False),
        ),
    ]
