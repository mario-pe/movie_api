from unittest import mock
from unittest.mock import Mock

from django.test import TestCase

from movies.omdb_service import OmdbService
from movies.tests.data_test import correct_data, incorrect_data


class OmdbServiceTest(TestCase):

    @mock.patch('requests.get')
    def test_should_return_data_if_response_status_is_200(self, mock_get):
        mock_resp = Mock(status_code=200)
        mock_get.return_value = mock_resp
        mock_get.return_value.json.return_value = correct_data
        result = OmdbService.get_movie_data('title')

        self.assertDictEqual(result, correct_data)

    @mock.patch('requests.get')
    def test_should_return_None_if_response_status_is_diffrent_than_200(self, mock_get):
        mock_resp = Mock(status_code=404)
        mock_get.return_value = mock_resp
        result = OmdbService.get_movie_data('title')

        self.assertEquals(result, None)