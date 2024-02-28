def hostname_from_request(request):
    """
    Get domain from request, split on `:` to remove port
    """
    return request.get_host().split(":")[0].lower()


def id_next_action(request, dict_of_actions, default_url):
    """
    to handle multiple submit buttons in same form
    we assume POST
    """
    return next(
        (
            redirect_to_url
            for name, redirect_to_url in dict_of_actions.items()
            if name in request.POST
        ),
        default_url,
    )
