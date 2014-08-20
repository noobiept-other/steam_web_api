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