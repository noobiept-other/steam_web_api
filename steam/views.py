from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlencode
from django.conf import settings

from steam import steam_api, utilities


def home( request, whatToShow= None ):

    news = []
    context = {}
    user = request.user

    if user.is_authenticated:

        if whatToShow == 'owned':
            apps = user.get_games_owned()
            count = apps[ 'game_count' ]
            context[ 'show_owned_apps' ] = True

        else:
            apps = user.get_games_played()
            count = apps[ 'total_count' ]
            context[ 'show_recently_played' ] = True

        howMany = 2

        if count != 0:

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



def game( request, appId, whatToShow= None ):

    context = {
        'appId': appId
    }

    try:
        if whatToShow == 'stats':

            if request.user.is_authenticated:

                steamId = request.user.username
                context[ 'show_stats' ] = True
                context[ 'stats' ] = steam_api.getUserStatsForGame( steamId, appId )

                achievements = context[ 'stats' ].get( 'achievements' )

                if achievements:
                    _update_achievements( appId, achievements )

            else:
                return HttpResponseRedirect( settings.LOGIN_URL + '?next=' + reverse( 'game_specify', args= [ appId, whatToShow ] ) )

        elif whatToShow == 'global_achievements':
            context[ 'show_global_achievements' ] = True
            context[ 'global_achievements' ] = steam_api.getGlobalAchievementPercentagesForApp( appId )

            _update_achievements( appId, context[ 'global_achievements' ] )

        elif whatToShow == 'news':
            context[ 'show_news' ] = True
            context[ 'news' ] = steam_api.getNewsForApp( appId, 10, 500 )

        else:
            context[ 'show_game_info' ] = True
            context[ 'game_info' ] = steam_api.appDetails( [ appId ] )[ str( appId ) ][ 'data' ]
            context[ 'current_players' ] = steam_api.getNumberOfCurrentPlayers( appId )


    except steam_api.SteamApiError:
        utilities.set_message( request, 'No statistics available.' )


    utilities.get_message( request, context )
    return render( request, 'game.html', context )


def find_by_id( request ):
    """
        Specify a steam id, to show that account information page.
    """
    context = {}
    utilities.get_message( request, context )

    return render( request, 'find_by_id.html', context )


def _update_achievements( appId, achievements ):
    """
        Update the achievements information (with the game's schema information).
    """
    gameSchema = steam_api.getSchemaForGame( appId )
    schemaAchievements = {}

    availableStats = gameSchema.get( 'availableGameStats' )
    if not availableStats:
        return

    availableAchievements = availableStats.get( 'achievements' )
    if not availableAchievements:
        return

    for achievement in availableAchievements:
        schemaAchievements[ achievement[ 'name' ] ] = achievement

    for achievement in achievements:
        try:
            schemaInfo = schemaAchievements[ achievement[ 'name' ] ]

        except KeyError:
            pass

        else:
            achievement.update( schemaInfo )