from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    url( r'^logout$', 'django.contrib.auth.views.logout', name= 'logout' ),
    url( r'^user/(?P<steamId>\d+)$', 'accounts.views.user_page', name= 'user_page' ),
    url( r'^user/(?P<steamId>\d+)/(?P<whatToShow>\w+)$', 'accounts.views.user_page', name= 'user_page_specify' ),
    url( r'^send_message/(?P<username>\w+)$', 'accounts.views.send_private_message', name= 'send_message' ),
    url( r'^check_message/$', 'accounts.views.check_message', name='check_message' ),
    url( r'^check_message/(?P<messageId>\w+)$', 'accounts.views.open_message', name= 'open_message' ),
    url( r'^remove_message/(?P<messageId>\w+)$', 'accounts.views.remove_message', name= 'remove_message' ),
    url( r'^set_moderator/(?P<username>\w+)$', 'accounts.views.set_moderator', name= 'set_moderator' ),
)
