import requests

def getAppNews( appId, howMany, maxLength= 300 ):
    url = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={}&count={}&maxlength={}&format=json'.format( appId, howMany, maxLength )

    r = requests.get( url )

    return r.json()



