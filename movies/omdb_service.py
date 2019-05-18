from movie.settings import OMDB_API_KEY
import requests


class OmdbService:

    def get_movie_data(title):
        """
        Method fatch movie data from omdb service

        :param title: title of movie data to fatch
        :return: Dictionaty with movie data or None if service have not information about given title
        """

        url = 'http://www.omdbapi.com/?t={}&apikey={}'.format(title, OMDB_API_KEY)
        timeout_seconds = 10
        response = requests.get(url, timeout=timeout_seconds)
        if response.status_code == 200:
            return response.json()