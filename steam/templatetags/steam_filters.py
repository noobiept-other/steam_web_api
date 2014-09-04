from django import template
from django.contrib.humanize.templatetags import humanize

from datetime import datetime


register = template.Library()

@register.filter
def convert_timestamp( timestamp ):

    try:
        date = int( timestamp )

    except ValueError:
        return timestamp

    return humanize.naturaltime( datetime.fromtimestamp( date ) )


@register.filter
def full_time( minutes ):
    """
        Converts minutes to days/hours/minutes

    :param minutes:
    :return: str
    """

    try:
        minutes = int( minutes )

    except ValueError:
        return minutes


        # we work in minutes
    hour = 60
    day = 24 * hour

    hourCount = 0
    dayCount = 0

        # count the days
    while minutes >= day:
        dayCount += 1
        minutes -= day

        # count the hours
    while minutes >= hour:
        hourCount += 1
        minutes -= hour


    def addUnit( dateStr, value, unit ):

        if value != 0:
            if value > 1:
                unit += 's'

            return '{} {} {}'.format( dateStr, value, unit )

        else:
            return dateStr


    time = addUnit( '', dayCount, 'day' )
    time = addUnit( time, hourCount, 'hour' )
    time = addUnit( time, minutes, 'minute' )

    return time
