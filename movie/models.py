from datetime import datetime

from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=50, unique=True)
    year = models.CharField(max_length=20)
    rated = models.CharField(max_length=20)
    released = models.CharField(max_length=20)
    runtime = models.CharField(max_length=8)
    genre = models.CharField(max_length=50)
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=200)
    actors = models.CharField(max_length=200)
    plot = models.TextField()
    language = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    awards = models.CharField(max_length=100)
    poster = models.CharField(max_length=200)
    metascore = models.CharField(max_length=10)
    imdbRating = models.CharField(max_length=10)
    imdbVotes = models.CharField(max_length=15)
    imdbID = models.CharField(max_length=15)
    type = models.CharField(max_length=20)
    DVD = models.CharField(max_length=20)
    boxOffice = models.CharField(max_length=30)
    production = models.CharField(max_length=50)
    website = models.CharField(max_length=200)
    response = models.BooleanField()


class Ratings(models.Model):
    source = models.CharField(max_length=50)
    value = models.CharField(max_length=10)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')


class Comment(models.Model):
    content = models.TextField(default='')
    date = models.DateField(default=datetime.now().strftime("%Y-%m-%d"))
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


