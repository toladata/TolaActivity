from django.contrib.sites.shortcuts import get_current_site

from django.conf import settings
from django.shortcuts import render_to_response

from workflow.models import Country, TolaUser, TolaSites, Organization


def redirect_after_login(strategy, *args, **kwargs):
    redirect = strategy.session_get('redirect_after_login')
    strategy.session_set('next',redirect)


def user_to_tola(backend, user, response, *args, **kwargs):

    # Add a google auth user to the tola profile
    default_country = Country.objects.first()
    default_organization = Organization.objects.first()
    userprofile, created = TolaUser.objects.get_or_create(user=user)

    # Do not set default values for existing TolaUser
    if created:
        userprofile.country = default_country
        userprofile.organization = default_organization
        userprofile.name = response.get('displayName')
        userprofile.email = response.get('emails["value"]')
        userprofile.save()


def auth_allowed(backend, details, response, *args, **kwargs):
    """
    The same social-core auth_allowed method but fetching and
    adding white-listed domains from TolaSites
    """
    emails = backend.setting('WHITELISTED_EMAILS', [])
    domains = backend.setting('WHITELISTED_DOMAINS', [])

    site = get_current_site(None)
    tola_site = TolaSites.objects.get(site=site)
    if tola_site and tola_site.whitelisted_domains:
        tola_domains = ','.join(tola_site.whitelisted_domains.split())
        tola_domains = tola_domains.split(',')
        domains += tola_domains
    email = details.get('email')
    allowed = False
    if email and (emails or domains):
        domain = email.split('@', 1)[1]
        allowed = email in emails or domain in domains

    if not allowed:
        static_url = settings.STATIC_URL
        return render_to_response('unauthorized.html',
                                  context={'STATIC_URL': static_url})
