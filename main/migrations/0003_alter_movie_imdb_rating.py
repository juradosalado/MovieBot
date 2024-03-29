# Generated by Django 4.1.7 on 2023-03-16 18:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_authors_movie_actors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='imdb_rating',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
    ]
