# Generated by Django 2.1.7 on 2019-03-30 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0018_query_last_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='reddit',
            field=models.BooleanField(default=False),
        ),
    ]
