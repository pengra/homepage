# Generated by Django 2.1.7 on 2019-03-26 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20190325_0719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=200, unique=True)),
                ('occurances', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='tag',
            name='results',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='words',
        ),
        migrations.RemoveField(
            model_name='url',
            name='domain',
        ),
        migrations.RemoveField(
            model_name='word',
            name='nexts',
        ),
        migrations.RemoveField(
            model_name='result',
            name='links_to',
        ),
        migrations.RemoveField(
            model_name='result',
            name='links_to_domains',
        ),
        migrations.RemoveField(
            model_name='result',
            name='scanned',
        ),
        migrations.RemoveField(
            model_name='result',
            name='words',
        ),
        migrations.AddField(
            model_name='result',
            name='grabbed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='badges',
            field=models.ManyToManyField(related_name='pages', to='search.Badge'),
        ),
        migrations.AlterField(
            model_name='result',
            name='url',
            field=models.URLField(unique=True),
        ),
        migrations.DeleteModel(
            name='Domain',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.DeleteModel(
            name='URL',
        ),
        migrations.DeleteModel(
            name='Word',
        ),
        migrations.AddField(
            model_name='query',
            name='results',
            field=models.ManyToManyField(related_name='queries', to='search.Result'),
        ),
    ]