from django.test import TestCase

from movie.omdb_service import OmdbService
from movie.tests.data_test import correct_data, incorrect_data


class OmdbServiceTest(TestCase):

    def test_should_return_data_if_response_status_is_200(self):

        result = OmdbService.get_movie_data('rambo')

        self.assertDictEqual(result, correct_data)

    def test_should_return_empty_dictionary_if_response_status_is_diffrent_than_200(self):

        result = OmdbService.get_movie_data('title_doesnt_exist')

        self.assertEquals(result, incorrect_data)