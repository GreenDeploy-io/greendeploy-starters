from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now

DEFAULT_CHOICES_NAME = "STATUS"


# new pypi for ltree and then new StatusField that's ltree based


class StatusField(models.CharField):
    """
    A CharField that looks for a ``STATUS`` class-attribute and
    automatically uses that as ``choices``. The first option in
    ``STATUS`` is set as the default.

    Also has a default max_length so you don't have to worry about
    setting that.

    Also features a ``no_check_for_status`` argument to make sure
    South can handle this field when it freezes a model.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 100)
        self.check_for_status = not kwargs.pop("no_check_for_status", False)
        self.choices_name = kwargs.pop("choices_name", DEFAULT_CHOICES_NAME)
        super().__init__(*args, **kwargs)

    def prepare_class(self, sender, **kwargs):
        if not sender._meta.abstract and self.check_for_status:
            assert hasattr(
                sender, self.choices_name
            ), f"To use StatusField, the model '{sender.__name__}' must have a {self.choices_name} choices class attribute."
            self.choices = getattr(sender, self.choices_name)
            if not self.has_default():
                self.default = tuple(getattr(sender, self.choices_name))[0][
                    0
                ]  # set first as default

    def contribute_to_class(self, cls, name):
        models.signals.class_prepared.connect(self.prepare_class, sender=cls)
        # we don't set the real choices until class_prepared (so we can rely on
        # the STATUS class attr being available), but we need to set some dummy
        # choices now so the super method will add the get_FOO_display method
        self.choices = [(0, "dummy")]
        super().contribute_to_class(cls, name)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["no_check_for_status"] = True
        return name, path, args, kwargs


class MonitorField(models.DateTimeField):
    """
    A DateTimeField that monitors another field on the same model and
    sets itself to the current date/time whenever the monitored field
    changes.

    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("default", now)
        monitor = kwargs.pop("monitor", None)
        if not monitor:
            raise TypeError(f'{self.__class__.__name__} requires a "monitor" argument')
        self.monitor = monitor
        when = kwargs.pop("when", None)
        if when is not None:
            when = set(when)
        self.when = when
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.monitor_attname = f"_monitor_{name}"
        models.signals.post_init.connect(self._save_initial, sender=cls)
        super().contribute_to_class(cls, name)

    def get_monitored_value(self, instance):
        return getattr(instance, self.monitor)

    def _save_initial(self, sender, instance, **kwargs):
        if self.monitor in instance.get_deferred_fields():
            # Fix related to issue #241 to avoid recursive error on double monitor fields
            return
        setattr(instance, self.monitor_attname, self.get_monitored_value(instance))

    def pre_save(self, model_instance, add):
        value = now()
        previous = getattr(model_instance, self.monitor_attname, None)
        current = self.get_monitored_value(model_instance)
        if previous != current and (self.when is None or current in self.when):
            setattr(model_instance, self.attname, value)
            self._save_initial(model_instance.__class__, model_instance)
        return super().pre_save(model_instance, add)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["monitor"] = self.monitor
        if self.when is not None:
            kwargs["when"] = self.when
        return name, path, args, kwargs


class BusinessIdentifierField(models.CharField):
    default_validators = [
        RegexValidator(
            regex=r"^[1-9a-zA-Z_.-]+$",
            message="Business ID must be alphanumeric, dots, hyphens, and underscores only.",
        )
    ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 255)
        super().__init__(*args, **kwargs)
