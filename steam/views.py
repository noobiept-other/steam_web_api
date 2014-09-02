from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlencode

from steam import steam_api, utilities

def home( request ):

    news = []

    if request.user.is_authenticated():
        gamesOwned = request.user.get_games_played()
        howMany = 2

        for game in gamesOwned[ 'games' ]:
            gameName = game[ 'name' ]
            gameIcon = game[ 'img_icon_url' ]
            gameId = game[ 'appid' ]

            gameNews = steam_api.getNewsForApp( gameId, howMany )

            for new in gameNews:

                new[ 'gameName' ] = gameName
                new[ 'gameId' ] = gameId
                new[ 'gameIcon' ] = gameIcon
                news.append( new )



        def sortNews( a ):
            return a[ 'date' ]

        news.sort( key= sortNews, reverse= True )

    context = {
        'news': news
    }

    utilities.get_message( request, context )

    return render( request, 'home.html', context )



def app_list( request ):

    context = {
        'apps': steam_api.getAppList()
    }

    utilities.get_message( request, context )

    return render( request, 'app_list.html', context )


def global_achievement_percentages( request, appId ):

    context = {
        'achievements': steam_api.getGlobalAchievementPercentagesForApp( appId )
    }

    utilities.get_message( request, context )

    return render( request, 'global_achievement_percentages.html', context )


def steam_profile( request, steamId ):

    profile = steam_api.getPlayerSummaries( [ steamId ] )[ 0 ]

    friendsList = steam_api.getFriendList( steamId )

    friendsId = [ a[ 'steamid' ] for a in friendsList ]

        # get the names of the friends
    friendsProfiles = steam_api.getPlayerSummaries( friendsId )
    recentlyPlayedGames = steam_api.getRecentlyPlayedGames( steamId )

    context = {
        'profile': profile,
        'steamId': steamId,
        'friendsProfile': friendsProfiles,
        'recentlyPlayedGames': recentlyPlayedGames
    }

    utilities.get_message( request, context )

    return render( request, 'steam_profile.html', context )


@login_required
def game( request, appId, whatToShow= None ):

    steamId = request.user.steam_id
    context = {
        'appId': appId
    }

    try:
        if whatToShow == 'stats':
            context[ 'stats' ] = steam_api.getUserStatsForGame( steamId, appId )

        else:
            context[ 'game_info' ] = steam_api.appDetails( [ appId ] )[ str( appId ) ][ 'data' ]

    except ValueError:

        values = {
            'url': request.path_info,
            'reason': "Failed to get the user's stats for the game."
        }
        url = '{}?{}'.format( reverse( 'steam_api_failed' ), urlencode( values ) )

        return HttpResponseRedirect( url )

    return render( request, 'game.html', context )



def steam_api_failed( request ):

    context = {
        'url': request.GET[ 'url' ],
        'reason': request.GET[ 'reason' ]
    }

    return render( request, 'steam_api_failed.html', context )