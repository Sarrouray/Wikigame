from django.urls import path
from . import views
from .views import wiki_game_view

#URLConf
urlpatterns = [
    path('', wiki_game_view, name='wiki_game'),
]


urlpatterns = [
    path('', wiki_game_view, name='wiki_game_view'),  # La vue sera accessible à l'URL 'wikigame/'
]
