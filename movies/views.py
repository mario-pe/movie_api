import requests
from django.db.models import Count
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Movie, Comment
from .serializers import MovieSerializer, TitleMovieSerializer, CommentSerializer


class MoviesView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(instance=movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        title_serializer = TitleMovieSerializer(data=request.data)
        if title_serializer.is_valid():
            title = title_serializer.data['title']
            movie = Movie.objects.filter(title__iexact=title).first()
            if movie:
                movie_serializer = MovieSerializer(instance=movie)
                return Response(movie_serializer.data, status=status.HTTP_200_OK)
            else:
                url = "http://www.omdbapi.com/?t={}&apikey=7755ccf0".format(title)
                api_response = requests.get(url, timeout=10)
                if api_response.status_code == 200 and api_response.json().get('Response') == 'True':
                    api_movie_data = api_response.json()
                    data = data_converter(api_movie_data)
                    movie_serializer = MovieSerializer(data=data)
                    if movie_serializer.is_valid(raise_exception=True):
                        movie_serializer.save()
                        return Response(movie_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    error_response_dict = { "Error": "Movie not found!"} # ładniej to zrobic
                    return Response(error_response_dict, status=status.HTTP_404_NOT_FOUND)

#jeden taki ModelViewSet troche głuio wyglada  sam nie wiem zostawic czy zmienic na normalne APIView
#w urls.py w zasadzie tylko dla tego widoku jest router.register(r'comments', views.CommentsViewSet)

#kiedys mi ktos powiedzial ze dobry programista to leniwy programista wydaje sie że mam zadatki na dobrego

#powiedz co sądzisz
class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class TopViewSet(APIView):
    def get(self, request, date_from, date_to):
        if date_testing(date_from, date_to):
            comented_films = Comment.objects.all().values('movie').filter(date__range=[date_from, date_to]).annotate(total=Count('pk')).order_by('movie').order_by('-total')
            movie_rank = movie_rank_generator(comented_films)
            return Response(movie_rank, status=status.HTTP_201_CREATED)

        return Response('hujowe daty synek ',status=status.HTTP_400_BAD_REQUEST)


def date_testing(date_from, date_to):
    if date_from and date_to:
        date_format = "%Y-%m-%d"
        date_from = datetime.strptime(str(date_from), date_format)
        date_to = datetime.strptime(str(date_to), date_format)
        delta = date_to - date_from
        if delta.days >= 0:
            return True
        return False


def movie_rank_generator(commented_movies):
    if commented_movies:
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


# taki mapper to taki sredni ale nie mialem pomyslu na lepszy

# dlaczego tak cudujesz Mariusz?
# a no bo w modelu pola są z małej liter a z servicu przychodza duze na początku z duzymi literami chciałem isc do przodu bo bałem sie ze zapis zagniezdzonych obiektów mnie zabije
# skoro sytuacja wydaje sie opanowana to jutro poszukam czy da sie przmapowac w serializerze czy cos mądrzejszego z tym zrobic

# jesli cos ci przyjdzie do głowy wal smiał


def data_converter(api_data): #jakos to zwalidować
    data = {}
    data['title'] = api_data.get('Title')
    data['year'] = int(api_data.get('Year'))
    data['rated'] = api_data.get('Rated')
    data['released'] = api_data.get('Released')
    data['runtime'] = api_data.get('Runtime')
    data['genre'] = api_data.get('Genre')
    data['director'] = api_data.get('Director')
    data['writer'] = api_data.get('Writer')
    data['actors'] = api_data.get('Actors')
    data['plot'] = api_data.get('Plot')
    data['language'] = api_data.get('Language')
    data['country'] = api_data.get('Country')
    data['awards'] = api_data.get('Awards')
    data['poster'] = api_data.get('Poster')
    data['imdbRating'] = api_data.get('imdbRating')
    data['imdbVotes'] = api_data.get('imdbVotes')
    data['imdbID'] = api_data.get('imdbID')
    data['type'] = api_data.get('Type')
    data['DVD'] = api_data.get('DVD')  # 25 Jan 2008
    data['boxOffice'] = api_data.get('BoxOffice')
    data['production'] = api_data.get('Production')
    data['website'] = api_data.get('Website')
    data['response'] = bool(api_data.get('Response'))
    data['ratings'] = ratings_converter_compreh(api_data)
    return data

# ktorą wybrać jesli zostane przy tym rozwiązaniu?


def ratings_converter_classic_for(api_data):
    converted_ratings_list = []
    if len(api_data.get('Ratings')) > 0: # oddzielna metoda
        ratings = api_data.get('Ratings')
        for rating in ratings:
            r_dict = {}
            for key, value in rating.items():
                r_dict[key.lower()] = value
            converted_ratings_list.append(r_dict)
        return converted_ratings_list
    else:
        return converted_ratings_list


def ratings_converter_compereh_for(api_data):
    converted_ratings_list = []
    if len(api_data.get('Ratings')) > 0:
        ratings = api_data.get('Ratings')
        for r in ratings:
            converted_ratings_list.append({k.lower(): v for k, v in r.items})
        return
    else:
        return converted_ratings_list


def ratings_converter_compreh(api_data):
    converted_ratings_list = []
    if len(api_data.get('Ratings')) > 0:
        ratings = api_data.get('Ratings')
        return [{k.lower(): v for k, v in r.items()} for r in ratings ]
    else:
        return converted_ratings_list
