# Generated by Django 2.1.7 on 2019-03-29 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0013_result_chan'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
