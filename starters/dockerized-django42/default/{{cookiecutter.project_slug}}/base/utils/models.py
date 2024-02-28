from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .fields import MonitorField, StatusField


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


class StatusModel(models.Model):
    """
    An abstract base class model with a ``status`` field that
    automatically uses a ``STATUS`` class attribute of choices, a
    ``status_changed`` date-time field that records when ``status``
    was last modified, and an automatically-added manager for each
    status that returns objects with that status only.

    """

    status = StatusField(_("status"))
    status_changed = MonitorField(_("status changed"), monitor="status")

    def save(self, *args, **kwargs):
        """
        Overriding the save method in order to make sure that
        status_changed field is updated even if it is not given as
        a parameter to the update field argument.
        """
        update_fields = kwargs.get("update_fields", None)
        if update_fields and "status" in update_fields:
            kwargs["update_fields"] = set(update_fields).union({"status_changed"})

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
