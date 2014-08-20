from django.conf import settings

import requests


def getNewsForApp( appId, howMany, maxLength= 300 ):
    """
    :param appId:
    :param howMany:
    :param maxLength:
    :return:
        [
            {
                "gid"             : int,
                "title"           : str,
                "url"             : str,
                "is_external_url" : bool,
                "author"          : str,
                "contents"        : str,
                "feedlabel"       : str,
                "date"            : int (unix timestamp),
                "feedname"        : str
            },
            (...)
        ]
    """

    url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={}&count={}&maxlength={}&format=json'.format( appId, howMany, maxLength )

    r = requests.get( url )

    return r.json()[ 'appnews' ][ 'newsitems' ]


def getAppList():
    """
    :return:
        [
            {
                "appid" : int,
                "name"  : str
            },
            (...)
        ]
    """

    url = 'http://api.steampowered.com/ISteamApps/GetAppList/v0001/'

    r = requests.get( url )

    return r.json()[ 'applist' ][ 'apps' ][ 'app' ]

#HERE need to test below this


def getGlobalAchievementPercentagesForApp( appId ):

    url = 'http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={}&format=json'.format( appId )

    r = requests.get( url )

    return r.json()


def getGlobalStatsForGame( appId, achievementsNames ):

    count = len( achievementsNames )
        #HERE name[0], name[1], etc
    url = 'http://api.steampowered.com/ISteamUserStats/GetGlobalStatsForGame/v0001/?format=json&appid={}&count={}&name[0]={}'.format( appId, count, achievementsNames[ 0 ] )

    r = requests.get( url )

    return r.json()


def getPlayerSummaries( steamIds ):
    """

    :param steamIds: list of 64-bit steam IDs
    :return:
    """

    idsStr = ','.join( steamIds )
    steamKey = settings.STEAM_API_KEY

    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}&format=json'.format( steamKey, idsStr )

    r = requests.get( url )

    return r.json()


def getFriendList( steamId, relationship= 'friend' ):
    """

    :param steamId:
    :param relationship: 'all' or 'friend'
    :return:
    """

    url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship={}&format=json'.format( settings.STEAM_API_KEY, steamId, relationship )

    r = requests.get( url )

    return r.json()

#HERE optional language parameter
def getPlayerAchievements( steamId, appId ):

    url = 'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={}&key={}&steamid={}&format=json'.format( appId, settings.STEAM_API_KEY, steamId )

    r = requests.get( url )

    return r.json()

#HERE optional language parameter
def getUserStatsForGame( steamId, appId ):

    url = 'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={}&key={}&steamid={}&format=json'.format( appId, settings.STEAM_API_KEY, steamId )

    r = requests.get( url )

    return r.json()


def getOwnedGames( steamId ):
    #HERE some extra arguments
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json'.format( settings.STEAM_API_KEY, steamId )

    r = requests.get( url )

    return r.json()



def getRecentlyPlayedGames( steamId, count ):   #HERE count optional

    url = 'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={}&steamid={}&format=json'.format( settings.STEAM_API_KEY, steamId )

    r = requests.get( url )

    return r.json()


def isPlayingSharedGame( steamId, appId ):

    url = 'http://api.steampowered.com/IPlayerService/IsPlayingSharedGame/v0001/?key={}&steamid={}&appid_playing={}&format=json'.format( settings.STEAM_API_KEY, steamId, appId )

    r = requests.get( url )

    return r.json()