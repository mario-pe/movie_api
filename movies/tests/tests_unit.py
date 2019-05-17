from django.test import TestCase

from movies.views import date_testing, movie_rank_generator


class DataTestingTests(TestCase):

    def test_should_return_true_when_dates_are_correct(self):
        date_from = "2001-01-01"
        date_to = "2001-01-05"

        result = date_testing(date_from, date_to)

        self.assertTrue(result)

    def test_should_return_false_when_date_from_is_greater_than_date_to(self):
        date_from = "2001-01-05"
        date_to = "2001-01-01"

        result = date_testing(date_from, date_to)

        self.assertFalse(result)

    def test_should_return_false_when_date_is_in_wrong_format(self):
        date_from = "01-05-2001"
        date_to = "2001-01-01"

        result = date_testing(date_from, date_to)

        self.assertFalse(result)


class MovieRankGeneratorTests(TestCase):

    def test_should_return_list_of_dictionaries_with_ranking(self):
        data = [{'movie': 4, 'total': 1}, {'movie': 2, 'total': 2}, {'movie': 3, 'total': 2},
                {'movie': 1, 'total': 3}]

        result = movie_rank_generator(data)

        self.assertEqual(result, [{'movie': 4, 'total': 1, 'rank': 1}, {'movie': 2, 'total': 2, 'rank': 2}, {'movie': 3, 'total': 2, 'rank': 2}, {'movie': 1, 'total': 3, 'rank': 3}])

    def test_should_return_empty_list_if_data_set_is_empty(self):
        data = []

        result = movie_rank_generator(data)

        self.assertEqual(result, [])