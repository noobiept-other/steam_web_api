from django import template

from datetime import datetime


register = template.Library()

@register.filter
def convert_timestamp( timestamp ):

    try:
        date = int( timestamp )

    except ValueError:
        return timestamp

    return datetime.fromtimestamp( date ).strftime( '%d-%m-%Y %H:%M:%S' )
