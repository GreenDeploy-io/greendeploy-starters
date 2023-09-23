from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text

from organizations.models import Domain


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def format_email_subject(self, subject):
        domain = Domain.objects.get_domain_from_request(self.request) or get_current_site(self.request)
        return f"[{domain.name}] {force_text(subject)}"

    def send_mail(self, template_prefix, email, context):
        context['current_site'] = Domain.objects.get_domain_from_request(context.get('request')) or context['current_site']
        super().send_mail(template_prefix, email, context)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
