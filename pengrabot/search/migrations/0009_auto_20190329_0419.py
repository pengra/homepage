# Generated by Django 2.1.7 on 2019-03-29 04:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0008_result_newsapi'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='newsapi',
            new_name='news',
        ),
    ]