from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from bilis import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^new/', views.new_player, name='new'),
    url(r'^add/', views.add_result, name='add'),
    url(r'^players/', views.players, name='players'),
    url(r'^ajax/player_network/', views.ajax_player_network, name='player_network'),
    url(r'^upload/', views.upload_image, name='upload')
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
