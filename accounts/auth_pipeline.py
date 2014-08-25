USER_FIELDS = ['username', 'email']


def update_profile( *args, **kwargs ):

    user = kwargs[ 'user' ]
    details = kwargs[ 'details' ]

    isNew = kwargs[ 'is_new' ]

    if isNew:
        steamId = details[ 'player' ][ 'steamid' ]

        user.steam_id = steamId
        user.save()

