from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from accounts.forms import PrivateMessageForm
from accounts.models import PrivateMessage
from accounts.decorators import must_be_staff, must_be_moderator

from steam import utilities
from steam import steam_api


def user_page( request, steamId= None, whatToShow= None ):
    """
        The user page has information about an user account.
        Also where you can change some settings (like the password).

        The steam account (specified by the steam id) may or not be registered in this website.
    """
    userModel = get_user_model()

    if not steamId:
        steamId = request.GET.get( 'steamid' )

    steamId = int( steamId )
    context = {
        'steamId': steamId
    }

    try:
        user = userModel.objects.get( username= steamId )

    except userModel.DoesNotExist:
        playerSummaries = steam_api.getPlayerSummaries( [ steamId ] )

        if len( playerSummaries ) == 0:
            previous = request.GET.get( 'previous' )

            if previous:
                utilities.set_message( request, 'Account not found.' )
                return HttpResponseRedirect( previous )

            else:
                raise Http404( "Account not found." )

        context.update({
            'steamInfo': playerSummaries[ 0 ]
        })

    else:
        context.update({
            'pageUser': user,
            'unreadMessages': user.how_many_unread_messages(),
            'steamInfo': user.get_steam_extra_data()
        })

    try:
        if whatToShow == 'friends':
            context[ 'show_friends' ] = True
            context[ 'friends' ] = steam_api.getFriendsSummaries( steamId )

        elif whatToShow == 'games_owned':
            context[ 'show_games_owned' ] = True
            context[ 'games_owned' ] = steam_api.getOwnedGames( steamId )

        else:
            context[ 'show_games_played' ] = True
            context[ 'games_played' ] = steam_api.getRecentlyPlayedGames( steamId )

        # means the account is set to private
    except steam_api.SteamApiError:
        utilities.set_message( request, 'Account is private!' )

    utilities.get_message( request, context )

    return render( request, 'accounts/user_page.html', context )


@login_required
def message_send( request, username ):
    """
        Send a private message to another user.
    """
    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( 'Invalid username.' )


    if request.method == 'POST':
        form = PrivateMessageForm( request.POST )

        if form.is_valid():

            title = form.cleaned_data[ 'title' ]
            content = form.cleaned_data[ 'content' ]
            message = PrivateMessage( receiver= user, sender= request.user, title= title, content= content )
            message.save()

            utilities.set_message( request, 'Message sent to {}!'.format( user ) )

            return HttpResponseRedirect( user.get_url() )

    else:
        form = PrivateMessageForm()

    context = {
        'form': form,
        'receiver': user
    }

    return render( request, 'accounts/send_message.html', context )


@login_required
def message_all( request ):

    messages = request.user.privatemessage_set.all()

    context = {
        'messages': messages
    }

    utilities.get_message( request, context )

    return render( request, 'accounts/check_messages.html', context )


@login_required
def message_open( request, messageId ):
    """
        Open a particular private message.
    """
    try:
        message = request.user.privatemessage_set.get( id= messageId )

    except PrivateMessage.DoesNotExist:
        raise Http404( "Couldn't find that message." )

    if not message.has_been_read:
        message.has_been_read = True
        message.save( update_fields= [ 'has_been_read' ] )

    context = {
        'private_message': message
    }

    return render( request, 'accounts/open_message.html', context )


@login_required
def message_remove_confirm( request, messageId ):
    """
        Confirm the message removal.
    """
    try:
        message = request.user.privatemessage_set.get( id= messageId )

    except PrivateMessage.DoesNotExist:
        raise Http404( "Didn't find the message." )

    else:
        context = {
            'private_message': message
        }

        return render( request, 'accounts/remove_message.html', context )


@login_required
def message_remove( request, messageId ):
    """
        Remove a private message.
    """
    try:
        message = request.user.privatemessage_set.get( id= messageId )

    except PrivateMessage.DoesNotExist:
        raise Http404( "Message doesn't exist." )

    message.delete()
    utilities.set_message( request, 'Message removed!' )

    return HttpResponseRedirect( reverse( 'accounts:message_all' ) )


@must_be_staff
def set_moderator_confirm( request, username ):
    """
        Confirm giving/removing moderator rights to/from an user.
    """
    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    else:
        context = {
            'user_to_change': user
        }
        return render( request, 'accounts/change_moderator.html', context )


@must_be_staff
def set_moderator( request, username ):
    """
        Give/remove moderator rights from an account.
    """
    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    user.is_moderator = not user.is_moderator
    user.save()

    if user.is_moderator:
        message = "'{}' is now a moderator.".format( user )

    else:
        message = "'{}' is not a moderator anymore.".format( user )

    utilities.set_message( request, message )

    return HttpResponseRedirect( user.get_url() )


@must_be_staff
def remove_user_confirm( request, username ):
    """
        Confirm an user removal.
    """
    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    context = {
        'user_to_remove': user
    }

    return render( request, 'accounts/remove_user.html', context )


@must_be_staff
def remove_user( request, username ):
    """
        Remove an user account (also removes everything associated with it).
    """
    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    else:
        utilities.set_message( request, "'{}' user removed!".format( user ) )
        user.delete()

        return HttpResponseRedirect( reverse( 'home' ) )


@must_be_moderator
def disable_user_confirm( request, username ):
    """
        Confirm the enabling/disabling of an user account.
    """
    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    else:
        context = {
            'user_to_disable': user
        }

        return render( request, 'accounts/disable_user.html', context )


@must_be_moderator
def disable_user( request, username ):
    """
        Enable/disable an user account.
        If the account is disabled, the user won't be able to login.
    """
    userModel = get_user_model()

    try:
        user = userModel.objects.get( username= username )

    except userModel.DoesNotExist:
        raise Http404( "User doesn't exist." )

    else:
        value = not user.is_active

            # only other staff users can enable/disable staff users
        if user.is_staff:
            if request.user.is_staff:
                user.is_active = value
                user.save()

            else:
                return HttpResponseForbidden( "Can't disable a staff member." )

        else:
            user.is_active = value
            user.save()


        if value:
            message = "'{}' account is now active.".format( user )

        else:
            message = "'{}' account is now disabled.".format( user )

        utilities.set_message( request, message )

        return HttpResponseRedirect( user.get_url() )
