from django.conf.urls import url
from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'comments', views.CommentsViewSet)
router.register('top', views.TopViewSet)

urlpatterns = [
    path('', include(router.urls)),
    url('movies/', views.MoviesView.as_view(), name='movie'),
]

