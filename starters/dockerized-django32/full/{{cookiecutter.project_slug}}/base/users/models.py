from base.fields import CaseInsensitiveEmailField
from django.utils.translation import gettext_lazy as _
from improved_user.model_mixins import AbstractUser


class User(AbstractUser):
    """
    Default custom user model for project.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # because want to override the RFC 5321 for case sensitivity
    # see https://django-improved-user.readthedocs.io/en/latest/email_warning.html
    email = CaseInsensitiveEmailField(_("email address"), max_length=254, unique=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})" if self.full_name else self.email
