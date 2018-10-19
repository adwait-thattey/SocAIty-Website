import hashlib

from django import template
import re

register = template.Library()


@register.filter
def strtosnake(incoming):
    """
    Converts an incoming string to slug. Also converts full to lowercase. Used to get event url
    :param incoming: Incoming string that is full event name
    :return: slug form of the same string
    """
    incoming = str(incoming)

    incoming = incoming.replace(' ', '_')
    return incoming


