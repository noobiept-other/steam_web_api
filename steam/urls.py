from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url( r'^$', 'steam.views.home', name= 'home' ),
    url( r'^app_list$', 'steam.views.app_list', name= 'app_list' ),
    url( r'^global_achievement_percentages/(?P<appId>\d+)$', 'steam.views.global_achievement_percentages', name= 'global_achievement_percentages' ),
    url( r'^steam_profile/(?P<steamId>\d+)$', 'steam.views.steam_profile', name= 'steam_profile' ),
    url( r'^game/(?P<appId>\d+)$', 'steam.views.game', name= 'game' ),
    url( r'^game/(?P<appId>\d+)/(?P<whatToShow>\w+)$', 'steam.views.game', name= 'game_specify' ),

    url( r'^steam_api_failed$', 'steam.views.steam_api_failed', name= 'steam_api_failed' ),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url( '', include( 'social.apps.django_app.urls', namespace= 'social' ) ),

    url( r'^accounts/', include( 'accounts.urls', namespace= 'accounts', app_name= 'accounts' ) ),

    url( r'^admin/', include( admin.site.urls ) ),
)
