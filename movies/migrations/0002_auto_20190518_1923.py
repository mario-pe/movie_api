# Generated by Django 2.2.1 on 2019-05-18 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateField(default='2019-05-18'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rated',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.CharField(max_length=20),
        ),
    ]