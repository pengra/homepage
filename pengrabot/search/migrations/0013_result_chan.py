# Generated by Django 2.1.7 on 2019-03-29 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0012_result_edu'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='chan',
            field=models.BooleanField(default=False),
        ),
    ]
