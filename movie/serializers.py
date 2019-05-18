from movies.models import Comment, Movie, Ratings
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    """Comment model serializer"""

    class Meta:
        model = Comment
        fields = ['id', 'content', 'movie']


class RatingsSerializer(serializers.ModelSerializer):
    """Ratings model serializer"""

    Source = serializers.CharField(source='source')
    Value = serializers.CharField(source='value')

    class Meta:
        model = Ratings
        fields = ['Source', 'Value']


class MovieSerializer(serializers.ModelSerializer):
    """Movie model serializer """

    Title = serializers.CharField(source='title')
    Year = serializers.CharField(source='year')
    Rated = serializers.CharField(source='rated')
    Released = serializers.CharField(source='released')
    Runtime = serializers.CharField(source='runtime')
    Genre = serializers.CharField(source='genre')
    Director = serializers.CharField(source='director')
    Writer = serializers.CharField(source='writer')
    Actors = serializers.CharField(source='actors')
    Plot = serializers.CharField(source='plot')
    Language = serializers.CharField(source='language')
    Country = serializers.CharField(source='country')
    Awards = serializers.CharField(source='awards')
    Poster = serializers.CharField(source='poster')
    Metascore = serializers.CharField(source='metascore')
    Type = serializers.CharField(source='type')
    BoxOffice = serializers.CharField(source='boxOffice')
    Production = serializers.CharField(source='production')
    Website = serializers.CharField(source='website')
    Response = serializers.CharField(source='response')
    Ratings = RatingsSerializer(many=True, source='ratings')

    class Meta:
        model = Movie
        fields = ['pk', 'Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer', 'Actors', 'Plot',
                  'Metascore', 'Language', 'Country', 'Awards', 'Poster', 'imdbRating', 'imdbVotes', 'imdbID', 'Type', 'DVD',
                  'BoxOffice', 'Production', 'Website', 'Response', 'Ratings']

    def create(self, validated_data):
        """
        Method create movie object and related ratings objects

        :param: validated_data
        :return: movie instance
        """
        ratings_data = validated_data.pop('ratings')
        movie = Movie.objects.create(**validated_data)
        for rating_data in ratings_data:
            Ratings.objects.create(movie=movie, **rating_data)
        return movie



