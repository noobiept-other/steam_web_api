from django.conf import settings

import requests


    # below are the exceptions that can be raised
class SteamApiError( Exception ):
    """
        Wrong id's for example.
    """
    pass



def getNewsForApp( appId: int, howMany: int= None, maxLength: int= None ) -> list:
    """
    :param appId: the id of the application
    :param howMany (optional): limit how many news to return
    :param maxLength (optional): 0 to return the full content,  otherwise it limits the length of the content returned.
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

    url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={}&format=json'.format( appId )

    if howMany is not None:
        url += '&count={}'.format( howMany )

    if maxLength is not None:
        url += '&maxlength={}'.format( maxLength )

    r = requests.get( url )

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'appnews' ][ 'newsitems' ]

    except KeyError:
        raise SteamApiError( "Missing 'appnews.newsitems' key." )

    return result


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

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'applist' ][ 'apps' ][ 'app' ]

    except KeyError:
        raise SteamApiError( "Missing 'applist.apps.app' key." )

    return result



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

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'achievementpercentages' ][ 'achievements' ]

    except KeyError:
        raise SteamApiError( "Missing 'achievementpercentages.achievements' key." )

    return result



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
                "timecreated": int,
                "personastateflags": int
            },
            (...)
        ]
    """

    idsStr = ','.join( str( a ) for a in steamIds )
    steamKey = settings.STEAM_API_KEY

    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}&format=json'.format( steamKey, idsStr )

    r = requests.get( url )

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'response' ][ 'players' ]

    except KeyError:
        raise SteamApiError( "Missing 'response.players' key." )

    return result



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

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'friendslist' ][ 'friends' ]

    except KeyError:
        raise SteamApiError( "Missing 'friendslist.friends' key." )

    return result


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

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'playerstats' ]

    except KeyError:
        raise SteamApiError( "Missing 'playerstats' key." )

    return result


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

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'playerstats' ]

    except KeyError:
        raise SteamApiError( "Missing 'playerstats' key." )

    return result


def getOwnedGames( steamId, filterApps= None ):
    """
    :param steamId:
    :return:
        {
            "game_count": int,
            "games":
                [
                    {
                        "appid": int,
                        "name": str,
                        "playtime_forever": int,    # number of minutes played on record
                        "img_icon_url": str,
                        "img_logo_url": str,
                        "has_community_visible_stats": bool     # if there's a stats page with achievements or other game stats for this game
                    },
                    (...)
                ]
        }
    """

    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json&include_appinfo=1&include_played_free_games=1'.format( settings.STEAM_API_KEY, steamId )

    if filterApps is not None:
        url = '{}&input_json={{"appids_filter":{}}}'.format( url, str( filterApps ) )

    r = requests.get( url )

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'response' ]

    except KeyError:
        raise SteamApiError( "Missing 'response' key." )

    try:
        games = result[ 'games' ]

    except KeyError:
        pass

    else:
        _update_image_urls( games )

    return result



def getRecentlyPlayedGames( steamId, count= None ):
    """
    :param steamId:
    :param count:
    :return:
        {
            "total_count": int,
            "games":
                [
                    {
                        "appid": int,
                        "name": str,
                        "playtime_2weeks": int,     # total of minutes played last 2 weeks
                        "playtime_forever": int,    # total of minutes played on record
                        "img_icon_url": str,
                        "img_logo_url": str
                    },
                    (...)
                ]
        }
    """

    url = 'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key={}&steamid={}&format=json'.format( settings.STEAM_API_KEY, steamId )

    if count is not None:
        url = '{}&count={}'.format( url, count )

    r = requests.get( url )

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'response' ]

    except KeyError:
        raise SteamApiError( "Missing 'response' key." )

    try:
        games = result[ 'games' ]

    except KeyError:
        pass

    else:
        _update_image_urls( games )

    return result


def isPlayingSharedGame( steamId, appId ):
    """
    :param steamId:
    :param appId:
    :return:
        {
            "lender_steamid": str (an id)
        }

        The id of the lender of the game, or 0 if the game is owned by the account.
    """
    url = 'http://api.steampowered.com/IPlayerService/IsPlayingSharedGame/v0001/?key={}&steamid={}&appid_playing={}&format=json'.format( settings.STEAM_API_KEY, steamId, appId )

    r = requests.get( url )

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'response' ]

    except KeyError:
        raise SteamApiError( "Missing 'response' key." )

    return result


def getNumberOfCurrentPlayers( appId ):
    """
    :param appId: int
    :return: int
    """

    url = 'http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid={}'.format( appId )

    r = requests.get( url )

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'response' ][ 'player_count' ]

    except KeyError:
        raise SteamApiError( "Missing 'response.player_count' key." )

    return result


def getSteamLevel( steamId ):
    """
    :param steamId: int
    :return: int
    """

    url = 'http://api.steampowered.com/IPlayerService/GetSteamLevel/v1?key={}&steamid={}'.format( settings.STEAM_API_KEY, steamId )

    r = requests.get( url )

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'response' ][ 'player_level' ]

    except KeyError:
        raise SteamApiError( "Missing 'response.player_level' key." )

    return result



def getBadges( steamId ):
    """
    :param steamId: int
    :return:
        {
            "player_xp": int,
            "player_level": 13,
            "player_xp_needed_to_level_up": int,
            "player_xp_needed_current_level": int,
            "badges":
                [
                    {
                        "badgeid": int,
                        "level": int,
                        "completion_time": int,
                        "xp": int,
                        "scarcity": int,
                        "communityitemid": str (of an int),     # optional
				        "border_color": int,        # optional
				        "scarcity": int             # optional
                    },
                    (...)
                ]
        }
    """

    url = 'http://api.steampowered.com/IPlayerService/GetBadges/v1?key={}&steamid={}'.format( settings.STEAM_API_KEY, steamId )

    r = requests.get( url )

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    try:
        result = r.json()[ 'response' ]

    except KeyError:
        raise SteamApiError( "Missing 'response' key." )

    return result



def _update_image_urls( theList ):
    """
        Some methods of the steam api return a 'img_icon_url' and 'img_logo_url' with just the image's name, not the full url, so this function updates the dictionaries in the list with the full url

    :param theList:
    :return:
    """

    for app in theList:
        appId = app[ 'appid' ]

        app[ 'img_icon_url' ] = 'http://media.steampowered.com/steamcommunity/public/images/apps/{}/{}.jpg'.format( appId, app[ 'img_icon_url' ] )
        app[ 'img_logo_url' ] = 'http://media.steampowered.com/steamcommunity/public/images/apps/{}/{}.jpg'.format( appId, app[ 'img_logo_url' ] )



def appDetails( appIds ):
    """
    :param appIds: list of ids
    :return:
        {
            "appId":
                {
                    "success": bool,
                    "data":
                        {
                            "type": str,    # game/movie/demo
                            "name": str,
                            "steam_appid": int,
                            "required_age: int,
                            "dlc": str[] (list of ids)  # optional
                            "detailed_description": str (html),
                            "about_the_game": str (html),
                            "fullgame":     # optional (for movies/demos)
                                {
                                    "appid": str,
                                    "name": str
                                },
                            "supported_languages": str (html),
                            "header_image": str (url),
                            "website": str (url),
                            "pc_requirements":
                                {
                                    "minimum": str (html),
                                    "recommended": str (html)
                                },
                            "mac_requirements":
                                {
                                    "minimum": str,
                                    "recommended": str
                                },
                            "linux_requirements":
                                {
                                    "minimum": str,
                                    "recommended": str
                                },
                            "developers": str[],
                            "publishers": str[],
                            "demos":        # optional
                                {
                                    "appid": str,
                                    "description": str
                                },
                            "price_overview":   # optional (omitted if free-to-play)
                                {
                                    "currency": str,
                                    "initial": str,
                                    "final": str,
                                    "discount_percent": int
                                },
                            "packages": str[],
                            "package_groups":
                                [
                                    {
                                        "name": str,    # default/subscriptions
                                        "title": str,
                                        "description": str,
                                        "selection_text": str,
                                        "save_text": str,
                                        "display_type": str (of an int),
                                        "is_recurring_subscription": str (of bool),
                                        "subs":
                                            [
                                                {
                                                    "packageid": str (of int),
                                                    "percent_savings_text: str,
                                                    "percent_savings": int,
                                                    "option_text": str,
                                                    "option_description" str,
                                                    "can_get_free_license": str (of int)
                                                },
                                                (...)
                                            ]
                                    },
                                    (...)
                                ],
                            "platforms":
                                {
                                    "windows": bool,
                                    "mac" bool,
                                    "linux": bool
                                },
                            "metacritic":   # optional
                                {
                                    "score": int,
                                    "url": str (url)
                                },
                            "categories":
                                [
                                    {
                                        "id": str (of an int),
                                        "description": str
                                    },
                                    (...)
                                ],
                            "genres":
                                [
                                    {
                                        "id": str (of an int),
                                        "description": str
                                    },
                                    (...)
                                ],
                            "screenshots":
                                [
                                    {
                                        "id": int,
                                        "path_thumbnail": str (url),
                                        "path_full": str (url)
                                    },
                                    (...)
                                ],
                            "movies":
                                [
                                    {
                                        "id": str (of an int),
                                        "name": str,
                                        "thumbnail": str (url),
                                        "webm":
                                            {
                                                "480": str (url),
                                                "max": str (url)
                                                (...)
                                            },
                                        "highlight": bool
                                    },
                                    (...)
                                ],
                            "recommendations":
                                {
                                    "total": int
                                },
                            "release_date":
                                {
                                    "coming_soon": bool,
                                    "date": str
                                },
                            "support_info":
                                {
                                    "url": str,
                                    "email": str
                                }
                        }
                },

            "anotherAppId: (...)
        }

    """

    convertedToStr = [ str( a ) for a in appIds ]

    url = 'http://store.steampowered.com/api/appdetails/?appids={}'.format( ','.join( convertedToStr ) )

    r = requests.get( url )

    if r.status_code != 200:
        raise SteamApiError( "Status code: {} -- Content: {}".format( r.status_code, r.content ) )

    data = r.json()

        # check we if it was successful
    for appId, info in data.items():
        if info[ 'success' ] == False:
            raise SteamApiError( "Wasn't successful." )


        # fix pricing (for whatever reason, the values returned don't have a dot (for example 399 instead of 3.99)
    for key, value in data.items():

        try:
            priceOverview = value[ 'data' ][ 'price_overview' ]

        except KeyError:    # free-to-play application, doesn't have 'price_overview' key
            continue

        priceOverview[ 'initial' ] /= 100
        priceOverview[ 'final' ] /= 100


    return data


def getFriendsSummaries( steamId ):
    """
        Get a list with the friends account information.
    """
    friends = getFriendList( steamId )

    friendsId = [ a[ 'steamid' ] for a in friends ]

    return getPlayerSummaries( friendsId )