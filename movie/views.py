from datetime import datetime
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from movie.models import Movie, Comment
from movie.omdb_service import OmdbService
from movie.serializers import CommentSerializer, MovieSerializer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets


class MoviesView(APIView):
    """
    get:
    Return a list of all movies stored in data base.

    post:
    Returns movie data with given title straight from database if a movie existing in data base
    or fatch movie data from external service and create a new movie instance.
    """
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(instance=movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = JSONParser().parse(request)
        title = data.get('title')
        if title:
            movie = Movie.objects.filter(title__iexact=title).first()
            if movie:
                movie_serializer = MovieSerializer(instance=movie)
                return Response(movie_serializer.data, status=status.HTTP_200_OK)
            else:
                api_movie_data = OmdbService.get_movie_data(title)
                movie = Movie.objects.filter(title=api_movie_data.get('Title')).first()
                if movie:
                    return Response(api_movie_data, status=status.HTTP_200_OK)
                movie_serializer = MovieSerializer(data=api_movie_data)
                if movie_serializer.is_valid():
                    # movie_serializer.save()
                    return Response(movie_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(message_generator("Movie not found!"), status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(message_generator("Data not valid! Request must contains \'title\' key."), status=status.HTTP_404_NOT_FOUND)


class CommentsViewSet(viewsets.ModelViewSet):
    """
    get:
    Return a list of all the existing comments.

    post:
    Create a new comment instance.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('movie',)


class TopViewSet(APIView):
    """
    get:
    Return a sorted list of most comment movies in given date period.
    Necessary to function are two queryparams: date_from, date_to.
    """
    def get(self, request):
        date_from = request.query_params.get('date_from')
        date_to =request.query_params.get('date_to')
        if date_testing(date_from, date_to):
            comented_films = Comment.objects.values('movie').filter(date__range=[date_from, date_to]).annotate(total=Count('pk')).order_by('movie').order_by('-total')
            movie_rank = movie_rank_generator(comented_films)
            return Response(movie_rank, status=status.HTTP_200_OK)
        return Response(message_generator('Incorrect dates'), status=status.HTTP_400_BAD_REQUEST)


def date_testing(date_from, date_to):
    """
    Method checks if dates has correct format and validate period of time between dates.

    :param:date_from: string
    :param:date_to: string
    :return:Boolean value, true if dates are correct otherwise false.
    """
    if date_from and date_to:
        date_format="%Y-%m-%d"
        try:
            date_from = datetime.strptime(str(date_from), date_format)
            date_to = datetime.strptime(str(date_to), date_format)
        except ValueError:
            return False
        delta = date_to - date_from
        if delta.days >= 0:
            return True
        return False


def movie_rank_generator(commented_movies):
    """
    Method retrive a list that contains dictionaries with movie id and number of comments and add ranking position as rank.

    :param commented_movies: list
    :return: return processed list or empty list if there was
    """
    rank = 0
    temp_total = 0
    for movie in commented_movies:
        if temp_total == movie['total']:
            movie['rank'] = rank
        else:
            rank += 1
            movie['rank'] = rank
            temp_total = movie['total']
    return commented_movies


def message_generator(message):
    """
    Generate dictionaty with 'Error' key and message value.

    :param message: str
    :return: dictionary
    """
    return {"Error": message}

