from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides selfupdating
    ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PersonStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_by`` and ``modified_by`` fields.
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        editable=False,
        related_name="created_%(app_label)s_%(class)s",
        related_query_name="query_created_%(app_label)s_%(class)ss",
        on_delete=models.CASCADE,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        editable=False,
        related_name="last_edited_%(app_label)s_%(class)s",
        related_query_name="query_last_edited_%(app_label)s_%(class)ss",
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    @property
    def activity_actor_attr(self):
        return self.modified_by or self.created_by


class CreatedModel(models.Model):
    """
    An abstract base class model that provides selfupdating
    ``created`` field ONLY
    """

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UndeletableModel(models.Model):
    """
    An abstract base class model that disallows delete
    probably needs another that disallows delete depending on conditions
    """

    def delete(self):
        pass

    class Meta:
        abstract = True
