from unittest import mock
from unittest.mock import Mock

from django.test import TestCase

from movie.omdb_service import OmdbService
from movie.tests.data_test import correct_data, incorrect_data


class OmdbServiceTest(TestCase):

    def test_should_return_data_if_response_status_is_200(self):

        result = OmdbService.get_movie_data('rambo')

        self.assertDictEqual(result, correct_data)

    def test_should_return_dictionary_with_incorect_data_when_movie_does_not_exist_in_service(self):

        result = OmdbService.get_movie_data('title_doesnt_exist')

        self.assertEquals(result, incorrect_data)

    @mock.patch('requests.get')
    def test_should_return_empty_dictionary_if_respons_status_code_is_defferent_than_200(self, mock_get):
        mock_resp = Mock(status_code=400)
        mock_get.return_value = mock_resp

        result = OmdbService.get_movie_data('title_doesnt_exist')

        self.assertEquals(result, {})