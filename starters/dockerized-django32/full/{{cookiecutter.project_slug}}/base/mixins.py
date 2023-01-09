class CaseInsensitiveFieldMixin:
    """[summary]
    Mixin to make django fields case insensitive
    Inspired by https://github.com/iamoracle/django_case_insensitive_field
    """

    def get_prep_value(self, value):

        return str(value).lower()

    def to_python(self, value):

        value = super().to_python(value)

        # Value can be None so check that it's a string before lowercasing.
        return value.lower() if isinstance(value, str) else value