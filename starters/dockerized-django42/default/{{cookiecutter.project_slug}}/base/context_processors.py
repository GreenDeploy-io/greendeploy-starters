from django.conf import settings


def settings_values(request):
    """
    Returns settings context variable to be used inside templates
    """
    return {
        # "DEBUG": settings.DEBUG,
    }


