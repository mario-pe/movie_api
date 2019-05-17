import requests
from movie.settings import OMDB_API_KEY


class OmdbService:

    def get_movie_data(title):
        url = 'http://www.omdbapi.com/?t={}&apikey={}'.format(title, OMDB_API_KEY)
        timeout_seconds = 10
        response = requests.get(url, timeout=timeout_seconds)
        if response.status_code == 200:
            return response.json()