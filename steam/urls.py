from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

import steam.views


urlpatterns = [

    url( r'^$', steam.views.home, name= 'home' ),
    url( r'^home/(?P<whatToShow>\w+)$', steam.views.home, name= 'home_specify' ),
    url( r'^app_list$', steam.views.app_list, name= 'app_list' ),
    url( r'^find_by_id$', steam.views.find_by_id, name= 'find_by_id' ),
    url( r'^game/(?P<appId>\d+)$', steam.views.game, name= 'game' ),
    url( r'^game/(?P<appId>\d+)/(?P<whatToShow>\w+)$', steam.views.game, name= 'game_specify' ),


    url( '', include( 'social.apps.django_app.urls', namespace= 'social' ) ),
    url( r'^accounts/', include( 'accounts.urls', namespace= 'accounts', app_name= 'accounts' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
]


    # Serve static files when debug false
if not settings.DEBUG:
    urlpatterns += [
        url( r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT } ),
    ]
