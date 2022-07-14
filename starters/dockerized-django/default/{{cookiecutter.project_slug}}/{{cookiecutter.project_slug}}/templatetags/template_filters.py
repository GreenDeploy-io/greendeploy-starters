import datetime

from django import template

register = template.Library()

# Common filters

@register.filter(name="to_desired_date_format")
def to_desired_date_format(date_time_str, str_format):
    """
    take in datetime as str then display in different format
    """
    return datetime.datetime.strptime(date_time_str, "%Y-%m-%d").strftime(str_format)


@register.simple_tag
def if_search_in_string_print_that(search, string, print_that, default_print=""):
    """
    if search in string, print that
    """
    return print_that if search in string else default_print

@register.simple_tag
def if_this_str_eq_other_str_print_that(this_str, other_str, print_that, default_print=""):
    """
    if this_str same as other_str, print that
    """
    return print_that if this_str == other_str else default_print


@register.filter
def dictitem(dictionary, key):
    """
    dictionary.get(key)
    """
    return dictionary.get(key)

@register.filter
def member(obj, name):
    """
    apply getattr on object
    """
    return getattr(obj, name, None)

# end of Common filters
