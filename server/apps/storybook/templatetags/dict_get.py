# apps/storybook/templatetags/dict_get.py

from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """
    Returns the value for the given key from the dictionary d.
    If the key doesn't exist, returns None.
    """
    try:
        return d.get(key)
    except Exception:
        return None
