from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse

from steam import steam_api

class Account( AbstractUser ):

    steam_id = models.IntegerField( unique= True, blank= True, null= True )
    is_moderator = models.BooleanField( default= False )

    def get_url(self):
        return reverse( 'accounts:user_page', args= [ self.username ] )

    def get_user_social_auth(self):
        return self.social_auth.filter( provider= 'steam' )[ 0 ]

    def get_steam_extra_data(self):
        """
        :return:
            {
            'communityvisibilitystate': int, (0 or 1)
            'personaname': str,
            'personastate': int (0 or 1),
            'avatarfull': str (url),
            'steamid': str (of an int),
            'profileurl': str (url),
            'profilestate': int (0 or 1),
            'avatarmedium': str (url),
            'lastlogoff': int (unix timestamp),
            'commentpermission': int,
            'avatar': str (url)
            }
        """
        return self.get_user_social_auth().extra_data[ 'player' ]

    def get_friends(self):
        friends = steam_api.getFriendList( self.steam_id )

        friendsId = [ a[ 'steamid' ] for a in friends ]

        return steam_api.getPlayerSummaries( friendsId )

    def get_games_played(self):
        return steam_api.getRecentlyPlayedGames( self.steam_id )

    def get_games_owned(self):
        return steam_api.getOwnedGames( self.steam_id )


class PrivateMessage( models.Model ):

    receiver = models.ForeignKey( settings.AUTH_USER_MODEL )
    sender = models.ForeignKey( settings.AUTH_USER_MODEL, related_name= 'sender' )
    title = models.TextField( max_length= 100 )
    content = models.TextField( max_length= 500 )
    date_created = models.DateTimeField( help_text= 'Date Created', default= lambda: timezone.localtime( timezone.now() ) )

    def __unicode__(self):
        return self.title

    def get_url(self):
        return reverse( 'accounts:open_message', args= [ self.id ] )