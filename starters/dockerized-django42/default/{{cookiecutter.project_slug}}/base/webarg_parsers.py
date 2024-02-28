from benedict import benedict
from webargs.djangoparser import DjangoParser


class LineItemFriendlyParser(DjangoParser):
    """
    Note that Parser.pre_load is run after location loading
    but before Schema.load is called.
    It can therefore be called on multiple types of
    mapping objects, including MultiDictProxy,
    depending on what the location loader returns.
    read https://webargs.readthedocs.io/en/latest/advanced.html#parser-pre-load

    This parser handles nested query args. It expects nested levels
    delimited by a period and then deserializes the form args into a
    nested dict.


    For example, the URL query params `?name.first=John&name.last=Boone`
    will yield the following dict:

        {
            'name': {
                'first': 'John',
                'last': 'Boone',
            }
        }
    """

    def pre_load(self, location_data, *, schema, req, location):
        if location == "form" and "csrfmiddlewaretoken" in location_data:
            data = self.clean_up_line_items(location_data=location_data)
            # because second so use data, else MUST use location_data
            data = self.remove_csrf(location_data=data)
            return data
        return location_data

    def clean_up_line_items(self, location_data):
        """
        `location_data` in the `form` case is a MultiDictProxy of an immutable django QueryDict
        coerce to a dict to make it mutable
        """
        bd = benedict()
        data = dict(location_data)
        for key, value in sorted(list(data.items())):
            if "." in key:
                bd[key] = value
                del data[key]

        # join back
        for key, value in bd.items():
            data[key] = list(value.values())
        return data

    def remove_csrf(self, location_data):
        """
        `location_data` in the `form` case is a MultiDictProxy of an immutable django QueryDict
        coerce to a dict to make it mutable
        """
        data = dict(location_data)
        data.pop("csrfmiddlewaretoken")
        return data
