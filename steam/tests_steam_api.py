from django.test import TestCase

from steam import steam_api

class GetNewsForAppTest( TestCase ):
    """
        Tests steam_api.getNewsForApp()
    """

    appId = 730     # cs:go

    def test_not_found(self):
        appId = 1   # there's no app with this id

        self.assertRaises( steam_api.SteamApiError, steam_api.getNewsForApp, 1 )


    def test_returns_a_list(self):

        result = steam_api.getNewsForApp( self.appId )

        self.assertTrue( isinstance( result, list ) )