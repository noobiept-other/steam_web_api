"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
"""
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [

    url( r'^$', 'steam.views.home', name= 'home' ),
    url( r'^home/(?P<whatToShow>\w+)$', 'steam.views.home', name= 'home_specify' ),
    url( r'^app_list$', 'steam.views.app_list', name= 'app_list' ),
    url( r'^find_by_id$', 'steam.views.find_by_id', name= 'find_by_id' ),
    url( r'^game/(?P<appId>\d+)$', 'steam.views.game', name= 'game' ),
    url( r'^game/(?P<appId>\d+)/(?P<whatToShow>\w+)$', 'steam.views.game', name= 'game_specify' ),


    url( '', include( 'social.apps.django_app.urls', namespace= 'social' ) ),
    url( r'^accounts/', include( 'accounts.urls', namespace= 'accounts', app_name= 'accounts' ) ),
    url( r'^admin/', include( admin.site.urls ) ),
]
