from django.db import models

DATE_INPUT_FORMATS = ['%d-%m-%Y']


class Movie(models.Model):
    title = models.CharField(max_length=50)
    year = models.IntegerField()
    rated = models.IntegerField()
    released = models.DateField() #25 Jan 2008
    runtime = models.CharField(max_length=8)
    genre = models.CharField(max_length=50)
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=200)
    actors = models.CharField(max_length=200)
    plot = models.TextField()
    language = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    awards = models.CharField(max_length=100)
    poster = models.URLField()
    imdbRating = models.FloatField()
    imdbVotes = models.CharField(max_length=15) #"200,799",
    imdbID = models.CharField(max_length=15)
    type = models.CharField(max_length=20)
    DVD = models.DateField()  #25 Jan 2008
    boxOffice = models.CharField(max_length=30)
    production = models.CharField(max_length=50)
    website = models.URLField()
    response = models.BooleanField() # to moze być haczyk


class Comment(models.Model):
    content = models.TextField(default='')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Raitings(models.Model):
    source = models.CharField(max_length=50)
    value = models.CharField(max_length=10)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)