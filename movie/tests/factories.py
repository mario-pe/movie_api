from datetime import datetime

import factory

from movie.models import Movie, Ratings, Comment


class MovieFactory(factory.Factory):
    class Meta:
        model = Movie

    title = factory.Sequence(lambda a: "Title_{}".format(a + 1))
    year = factory.Sequence(lambda a: "200{}".format(a + 1))
    rated = factory.Sequence(lambda a: "R_{}".format(a + 1))
    released = factory.Sequence(lambda a: "25 Jan 200{}".format(a + 1))
    runtime = factory.Sequence(lambda a: "6{} min".format(a + 1))
    genre = factory.Sequence(lambda a: "Genre_{}".format(a + 1))
    director = factory.Sequence(lambda a: "Directo_{}".format(a + 1))
    writer = factory.Sequence(lambda a: "Writer_{}".format(a + 1))
    actors = factory.Sequence(lambda a: "Actor_{}".format(a + 1))
    plot = factory.Sequence(lambda a: "Plot_{}".format(a + 1))
    language = factory.Sequence(lambda a: "Language_{}".format(a + 1))
    country = factory.Sequence(lambda a: "Country_{}".format(a + 1))
    awards = factory.Sequence(lambda a: "Oscar_{}".format(a + 1))
    poster = factory.Sequence(lambda a: "www.posert_{}.com".format(a + 1))
    metascore = factory.Sequence(lambda a: "1{}".format(a + 1))
    imdbRating = factory.Sequence(lambda a: "1{}.0".format(a + 1))
    imdbVotes = factory.Sequence(lambda a: "100,{}99".format(a + 1))
    imdbID = factory.Sequence(lambda a: "tt046241{}".format(a + 1))
    type = factory.Sequence(lambda a: "movie_{}".format(a + 1))
    DVD = factory.Sequence(lambda a: "25 Jan 200{}".format(a + 1))
    boxOffice = factory.Sequence(lambda a: "$42,724,42{}".format(a + 1))
    production = factory.Sequence(lambda a: "Production_{}".format(a + 1))
    website = factory.Sequence(lambda a: "www.example_{}.com".format(a + 1))
    response = True


class RatingsFactory(factory.Factory):
    class Meta:
        model = Ratings

    source = "Internet Movie Database"
    value = 7.0/10
    movie = factory.RelatedFactory(MovieFactory)


class CommentFactory(factory.Factory):
    class Meta:
        model = Comment

    date = datetime.strptime(str("2001-01-02"), "%Y-%m-%d")
    content = factory.Sequence(lambda a: "Content_{}".format(a + 1))
    movie = factory.RelatedFactory(MovieFactory)
