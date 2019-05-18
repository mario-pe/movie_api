from datetime import datetime
from unittest import mock

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from movies.models import Movie, Comment
from movies.tests.factories import MovieFactory, CommentFactory, RatingsFactory
from movies.tests.data_test import correct_data, incorrect_data
from movies.views import MoviesView, CommentsViewSet, TopViewSet

factory = APIRequestFactory()


class MovieTests(TestCase):

    def setUp(self):
        MovieFactory.build().save()
        MovieFactory.build().save()
        MovieFactory.build().save()

    def test_should_return_list_of_all_movies_from_DB(self):
        request = factory.get('/movies/')
        view = MoviesView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), len(Movie.objects.all()))

    def test_should_return_movie_data_if_exist_in_DB(self):
        MovieFactory.build(title="Title_example").save()

        request = factory.post('/movies/', {"title": "Title_example"}, format='json')
        view = MoviesView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data.get('Title'), "Title_example")
        self.assertEqual(len(response.data.get('Ratings')), 0)

    def test_should_return_movie_and_related_ratings_data_if_exist_in_DB(self):
        MovieFactory.build(title="Title_foo").save()
        movie = Movie.objects.filter(title="Title_foo").first()
        RatingsFactory.build(movie_id=movie.pk).save()
        RatingsFactory.build(movie_id=movie.pk).save()

        request = factory.post('/movies/', {"title": "Title_foo"}, format='json')
        view = MoviesView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data.get('Title'), "Title_foo")
        self.assertEqual(len(response.data.get('Ratings')), 2)

    @mock.patch('movies.omdb_service.OmdbService.get_movie_data')
    def test_should_return_and_create_from_data_fetch_from_service(self, service):
        service.return_value = correct_data

        request = factory.post('/movies/', {"title": "Ramabo"}, format='json')
        view = MoviesView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data.get('Title'), "Rambo")
        self.assertEquals(len(Movie.objects.all()), 4)
        self.assertEqual(len(response.data.get('Ratings')), 3)

    @mock.patch('movies.omdb_service.OmdbService.get_movie_data')
    def test_should_return_response_status_404_if_move_title_not_exist_in_sevice(self, service):
        service.return_value = incorrect_data

        request = factory.post('/movies/', {"title": "Ramabo"}, format='json')
        view = MoviesView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data, {'Error': 'Movie not found!'})
        self.assertEquals(len(Movie.objects.all()), 3)

    @mock.patch('movies.omdb_service.OmdbService.get_movie_data')
    def test_should_return_response_status_404_if_title_not_exist_in_request_data(self, service):
        service.return_value = incorrect_data

        request = factory.post('/movies/', {"not_a_title": "Ramabo"}, format='json')
        view = MoviesView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEquals(response.data, {'Error': 'Data not valid! Request must contains \'title\' key.'})
        self.assertEquals(len(Movie.objects.all()), 3)

    @mock.patch('movies.omdb_service.OmdbService.get_movie_data')
    def test_should_return_response_status_200_if_part_of_title_was_given_of_existing_movie_in_DB(self, service):
        MovieFactory.build(title="Rambo").save()
        service.return_value = correct_data

        request = factory.post('/movies/', {"title": "Ram"}, format='json')
        view = MoviesView.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(Movie.objects.all()), 4)


class CommentsTests(TestCase):

    def setUp(self):
        CommentFactory.build()
        CommentFactory.build()
        CommentFactory.build()

    def test_should_return_all_comments_from_DB(self):
        request = factory.get('/comments/')
        view = CommentsViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), len(Comment.objects.all()))

    def test_should_return_all_comments_related_with_movie(self):
        MovieFactory.build(title="Title_foo").save()
        movie = Movie.objects.filter(title="Title_foo").first()
        CommentFactory.build(movie_id=movie.pk).save()
        CommentFactory.build(movie_id=movie.pk).save()

        request = factory.get('/comments?movie=1')
        view = CommentsViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 2)

    def test_should_create_new_comment(self):
        MovieFactory.build(title="Title_foo").save()
        request = factory.post("/comments/", {"content": "comment content", "movie": 1}, format='json')
        view = CommentsViewSet.as_view({"post": "create"})
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(len(Comment.objects.all()), 1)


class TopTests(TestCase):

    def setUp(self):
        MovieFactory.build().save()
        MovieFactory.build().save()
        MovieFactory.build().save()
        MovieFactory.build().save()
        MovieFactory.build().save()

        movies = Movie.objects.all()

        date_1 = datetime.strptime(str("2001-01-01"), "%Y-%m-%d")
        date_2 = datetime.strptime(str("2001-01-02"), "%Y-%m-%d")
        date_3 = datetime.strptime(str("2001-01-03"), "%Y-%m-%d")

        CommentFactory.build(movie_id=movies[0].pk, date=date_1).save()
        CommentFactory.build(movie_id=movies[0].pk, date=date_2).save()
        CommentFactory.build(movie_id=movies[0].pk, date=date_3).save()

        CommentFactory.build(movie_id=movies[1].pk, date=date_1).save()
        CommentFactory.build(movie_id=movies[1].pk, date=date_2).save()

        CommentFactory.build(movie_id=movies[2].pk, date=date_1).save()
        CommentFactory.build(movie_id=movies[2].pk, date=date_1).save()

        CommentFactory.build(movie_id=movies[3].pk, date=date_1).save()

    def test_should_return_sorted_films_by_comment_quatity(self):
        request = factory.get("/top?date_from=2001-01-01&date_to=2001-02-02")
        view = TopViewSet.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(len(Movie.objects.all()), 5)
        self.assertEqual(response.data[0].get('rank'), 1)
        self.assertEqual(response.data[1].get('rank'), 2)
        self.assertEqual(response.data[2].get('rank'), 2)
        self.assertEqual(response.data[3].get('rank'), 3)

    def test_should_return_response_with_status_code_400_when_dates_are_in_incorrect_format (self):
        request = factory.get("/top?date_from=2001/03/01&date_to=2001/02/02")
        view = TopViewSet.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data, {'Error': 'Incorrect dates'})

    def test_should_return_response_with_status_code_400_when_date_from_is_greater_than_date_to(self):
        request = factory.get("/top?date_from=2001-03-01&date_to=2001-02-02")
        view = TopViewSet.as_view()
        response = view(request)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data, {'Error': 'Incorrect dates'})
