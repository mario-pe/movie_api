import requests
from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Movie, Comment
from .serializers import MovieSerializer, TitleMovieSerializer, CommentSerializer


class MoviesView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        title_serializer = TitleMovieSerializer(data=request.data)
        if title_serializer.is_valid():
            title = title_serializer.data['title']
            movie = Movie.objects.filter(title=title).first()
            if not movie:
                url = "http://www.omdbapi.com/?t={}&apikey=7755ccf0".format(title)
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    api_movie_data = r.content
                    movie_serializer = MovieSerializer(data=api_movie_data)
                    if movie_serializer.is_valid():
                        movie_serializer.save()
                        return Response(movie_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    Response(title_serializer,status=status.HTTP_404_NOT_FOUND)

            movie_serializer = MovieSerializer(data=model_to_dict(movie))
            if movie_serializer.is_valid(raise_exception=True):
                movie_serializer.save()
                return Response(movie_serializer.data, status=status.HTTP_201_CREATED)
        return Response(title_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class TopViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer