def get_username( strategy, details, user= None, *args, **kwargs ):
    """
        Use the 'steamid' as the account username.
    """
    if not user:
        username = details[ 'player' ][ 'steamid' ]

    else:
        username = strategy.storage.user.get_username( user )

    return { 'username': username }