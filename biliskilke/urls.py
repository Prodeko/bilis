from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from bilis import views
from bilis import json

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("new/", views.new_player, name="new"),
    path("add/", views.add_result, name="add"),
    path("remove/", views.delete_last_result, name="remove"),
    path("delete/<player>", views.delete_player, name="delete"),
    path("set_rating_type/<rating_type>/", views.set_rating_type, name="set_rating_type"),
    path("players/", views.players, name="players"),
    path("player/<player>/", views.player, name="player"),
    path(
        "player/comparison/<player1>/<player2>/",
        views.comparison,
        name="comparison",
    ),
    path("ajax/player_network/", views.ajax_player_network, name="player_network"),
    path("upload/", views.upload_image, name="upload"),
    path("games/", views.games, name="games"),
    path(
        "chart/<player>/", views.chart, name="chart"
    ),  # TODO: remove dummy route and view
    path("ajax/games/", json.games, name="ajax_games"),
    path("ajax/players/", json.players, name="ajax_players"),
    path(
        "ajax/rating_time_series/<player>/",
        json.rating_time_series,
        name="rating_time_series",
    ),
]

if settings.DEBUG:
	urlpatterns += staticfiles_urlpatterns()
