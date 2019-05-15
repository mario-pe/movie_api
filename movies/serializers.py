from rest_framework import serializers
from .models import Movie, Comment


class MovieSerializer(serializers.ModelSerializer):
    released = serializers.DateField(format='%d-%b-%Y', input_formats=['%d-%b-%Y',])
    DVD = serializers.DateField(format='%d-%b-%Y', input_formats=['%d-%b-%Y',])

    class Meta:
        model = Movie
        fields = "__all__"


class TitleMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['title']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'movie']
