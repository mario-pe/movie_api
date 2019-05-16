from rest_framework import serializers
from .models import Comment, Movie, Ratings


class TitleMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['title']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'movie']


class RatingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ratings
        fields = ['source', 'value']


class MovieSerializer(serializers.ModelSerializer):
    ratings = RatingsSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        ratings_data = validated_data.pop('ratings')
        movie = Movie.objects.create(**validated_data)
        for rating_data in ratings_data:
            Ratings.objects.create(movie=movie, **rating_data)
        return movie



