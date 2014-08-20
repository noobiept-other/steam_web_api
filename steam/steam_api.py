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



def getGlobalAchievementPercentagesForApp( appId ):
    """
    :param appId:
    :return:
        [
            {
                "name"   : str,
                "percent : int
            }
        ]
    """

    url = 'http://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid={}&format=json'.format( appId )

    r = requests.get( url )

    return r.json()[ 'achievementpercentages' ][ 'achievements' ]




def getPlayerSummaries( steamIds ):
    """

    :param steamIds: list of 64-bit steam IDs
    :return:
        [
            {
                "steamid": str (of an int),
                "communityvisibilitystate": int,
                "profilestate": int,
                "personaname": str,
                "lastlogoff": int (unix timestamp),
                "commentpermission": int,
                "profileurl": str (url),
                "avatar": str (url),
                "avatarmedium": str (url),
                "avatarfull": str (url),
                "personastate": int,
                "primaryclanid": int,
                "timecreated": int ,
                "personastateflags": int
            },
            (...)
        ]
    """

    idsStr = ','.join( str( a ) for a in steamIds )
    steamKey = settings.STEAM_API_KEY

    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}&format=json'.format( steamKey, idsStr )

    r = requests.get( url )

    return r.json()[ 'response' ][ 'players' ]



def getFriendList( steamId, relationship= 'friend' ):
    """

    :param steamId:
    :param relationship: 'all' or 'friend'
    :return:
        [
            {
                "steamid": int,
                "relationship": str,
                "friend_since": int (unix timestamp)
            },
            (...)
        ]
    """

    url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={}&steamid={}&relationship={}&format=json'.format( settings.STEAM_API_KEY, steamId, relationship )

    r = requests.get( url )

    return r.json()[ 'friendslist' ][ 'friends' ]


def getPlayerAchievements( steamId, appId, language= 'english' ):
    """
    :param steamId:
    :param appId:
    :param language:
    :return:
        {
            "steamID": str (of a number),
            "gameName": str,
            "achievements":
                [
                    {
                        "apiname": str,
                        "achieved": int (0 or 1)
                    },
                    (...)
                ],
            "success": bool
        }
    """

    url = 'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={}&key={}&steamid={}&format=json&l={}'.format( appId, settings.STEAM_API_KEY, steamId, language )

    r = requests.get( url )

    return r.json()[ 'playerstats' ]


def getUserStatsForGame( steamId, appId, language= 'english' ):
    """
    :param steamId:
    :param appId:
    :param language:
    :return:
        {
            "steamID": str (of a number),
            "gameName": str,
            "stats":
                [
                    {
                        "name": str,
                        "value": int
                    },
                    (...)
                ],
            "achievements":
                [
                    {
                        "name": str,
                        "achieved": int (0 or 1)
                    },
                    (...)
                ]
        }
    """

    url = 'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={}&key={}&steamid={}&format=json&l={}'.format( appId, settings.STEAM_API_KEY, steamId, language )

    r = requests.get( url )

    return r.json()[ 'playerstats' ]

#HERE need to test below this
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