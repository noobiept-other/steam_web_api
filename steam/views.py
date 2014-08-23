from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from steam import steam_api

import steam.utilities as utilities

def home( request ):

    context = {

    }

    utilities.get_message( request, context )

    return render( request, 'home.html', context )

def show_news( request ):

    aomId = 266840
    howMany = 3

    context = {
        'news': steam_api.getNewsForApp( aomId, howMany )
    }

    utilities.get_message( request, context )

    return render( request, 'news.html', context )


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

    #steamId = 76561198041365537 #test
    profile = steam_api.getPlayerSummaries( [ steamId ] )[ 0 ]

    friendsList = steam_api.getFriendList( steamId )

    friendsId = [ a[ 'steamid' ] for a in friendsList ]

        # get the names of the friends
    friendsProfiles = steam_api.getPlayerSummaries( friendsId )

    context = {
        'profile': profile,
        'steamId': steamId,
        'friendsProfile': friendsProfiles
    }

    utilities.get_message( request, context )

    return render( request, 'steam_profile.html', context )


def game_stats( request, steamId, appId ):

    stats = steam_api.getUserStatsForGame( steamId, appId )

    context = {
        'stats': stats
    }

    return render( request, 'game_stats.html', context )


def games_owned( request, steamId ):

    games = steam_api.getOwnedGames( steamId )

    context = {
        'games': games
    }

    return render( request, 'games_owned.html', context )