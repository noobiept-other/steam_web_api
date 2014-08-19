from django import template

from datetime import datetime


register = template.Library()

@register.filter
def convert_timestamp( timestamp ):

    return datetime.fromtimestamp( int( timestamp ) ).strftime( '%d-%m-%Y %H:%M:%S' )
