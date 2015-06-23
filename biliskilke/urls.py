from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from bilis import views
from bilis import json
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^new/', views.new_player, name='new'),
    url(r'^add/', views.add_result, name='add'),
    url(r'^remove/', views.delete_last_result, name='remove'),
    url(r'^delete/(?P<player>\d+)', views.delete_player, name='delete'),
    url(r'^set_rating_type/(\w+)/', views.set_rating_type, name='set_rating_type'),
    url(r'^players/', views.players, name='players'),
    url(r'^player/(?P<player>\d+)', views.player, name='player'),
    url(r'^comparison/(?P<player1>\d+)/(?P<player2>\d+)', views.comparison, name='comparison'),
    url(r'^ajax/player_network/', views.ajax_player_network, name='player_network'),
    url(r'^upload/', views.upload_image, name='upload'),
    url(r'^games/', views.games, name='games'),
    url(r'^chart/(?P<player>\d+)', views.chart, name='chart'), #TODO: remove dummy route and view
    url(r'^ajax/games/', json.games, name='ajax_games'),
    url(r'^ajax/players/', json.players, name='ajax_players'),
    url(r'^ajax/rating_time_series/(?P<player>\d+)', json.rating_time_series, name='rating_time_series'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
