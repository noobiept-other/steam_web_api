from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlencode

from steam import steam_api, utilities

def home( request, whatToShow= None ):

    news = []
    context = {}
    user = request.user

    if user.is_authenticated():

        if whatToShow == 'owned':
            apps = user.get_games_owned()
            context[ 'show_owned_apps' ] = True

        else:
            apps = user.get_games_played()
            context[ 'show_recently_played' ] = True

        howMany = 2

        for aGame in apps[ 'games' ]:
            gameName = aGame[ 'name' ]
            gameIcon = aGame[ 'img_icon_url' ]
            gameId = aGame[ 'appid' ]

            gameNews = steam_api.getNewsForApp( gameId, howMany, 300 )

            for new in gameNews:

                new[ 'gameName' ] = gameName
                new[ 'gameId' ] = gameId
                new[ 'gameIcon' ] = gameIcon
                news.append( new )



        def sortNews( a ):
            return a[ 'date' ]

        news.sort( key= sortNews, reverse= True )

    context[ 'news' ] = news


    utilities.get_message( request, context )

    return render( request, 'home.html', context )



def app_list( request ):

    context = {
        'apps': steam_api.getAppList()
    }

    utilities.get_message( request, context )

    return render( request, 'app_list.html', context )




@login_required
def game( request, appId, whatToShow= None ):

    steamId = request.user.steam_id
    context = {
        'appId': appId
    }

    try:
        if whatToShow == 'stats':
            context[ 'stats' ] = steam_api.getUserStatsForGame( steamId, appId )
            context[ 'show_stats' ] = True

        elif whatToShow == 'global_achievements':
            context[ 'global_achievements' ] = steam_api.getGlobalAchievementPercentagesForApp( appId )
            context[ 'show_global_achievements' ] = True

        else:
            context[ 'game_info' ] = steam_api.appDetails( [ appId ] )[ str( appId ) ][ 'data' ]
            context[ 'current_players' ] = steam_api.getNumberOfCurrentPlayers( appId )
            context[ 'show_game_info' ] = True


    except steam_api.SteamApiError:

        values = {
            'url': request.path_info,
            'reason': "Failed to get the information from steam."
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