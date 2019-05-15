# Generated by Django 2.2.1 on 2019-05-15 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('rated', models.IntegerField()),
                ('released', models.DateField()),
                ('runtime', models.CharField(max_length=8)),
                ('genre', models.CharField(max_length=50)),
                ('director', models.CharField(max_length=100)),
                ('writer', models.CharField(max_length=200)),
                ('actors', models.CharField(max_length=200)),
                ('plot', models.TextField()),
                ('language', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('awards', models.CharField(max_length=100)),
                ('poster', models.URLField()),
                ('imdbRating', models.FloatField()),
                ('imdbVotes', models.CharField(max_length=15)),
                ('imdbID', models.CharField(max_length=15)),
                ('type', models.CharField(max_length=20)),
                ('DVD', models.DateField()),
                ('boxOffice', models.CharField(max_length=30)),
                ('production', models.CharField(max_length=50)),
                ('website', models.URLField()),
                ('response', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Raitings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=10)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
            ],
        ),
    ]
