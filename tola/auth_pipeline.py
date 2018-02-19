import logging

from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.conf import settings

from social_core.pipeline.partial import partial

from workflow.models import (Country, TolaUser, TolaSites, Organization)

logger = logging.getLogger(__name__)


def redirect_after_login(strategy, *args, **kwargs):
    redirect = strategy.session_get('redirect_after_login')
    strategy.session_set('next', redirect)


@partial
def check_user(strategy, details, backend, user=None, *args, **kwargs):
    """
    Redirect the user to the registration page, if we haven't found
    a user account yet.
    """
    if user:
        return {'is_new': False}
    try:
        user = User.objects.get(first_name=details['first_name'],
                                last_name=details['last_name'],
                                email=details['email'])
        return {
            'is_new': True,
            'user': user
        }
    except User.DoesNotExist:
        current_partial = kwargs.get('current_partial')
        query_params = 'cus_fname={}&cus_lname={}&cus_email={}&' \
                       'organization_uuid={}&partial_token={}'.format(
                        details['first_name'], details['last_name'],
                        details['email'], details['organization_uuid'],
                        current_partial.token)

        redirect_url = '/accounts/register/?{}'.format(query_params)
        return HttpResponseRedirect(redirect_url)


def auth_allowed(backend, details, response, *args, **kwargs):
    """
    Verifies that the current auth process is valid. Emails,
    domains whitelists and organization domains are applied (if defined).
    """
    allowed = False
    static_url = settings.STATIC_URL

    # Get whitelisted domains and emails defined in the settings
    whitelisted_emails = backend.setting('WHITELISTED_EMAILS', [])
    whitelisted_domains = backend.setting('WHITELISTED_DOMAINS', [])

    # Get the whitelisted domains defined in the TolaSites
    site = get_current_site(None)
    tola_site = TolaSites.objects.get(site=site)
    if tola_site and tola_site.whitelisted_domains:
        tola_domains = ','.join(tola_site.whitelisted_domains.split())
        tola_domains = tola_domains.split(',')
        whitelisted_domains += tola_domains

    try:
        email = details['email']
    except KeyError:
        logger.warning('No email was passed in the details.')
        allowed = False
    else:
        domain = email.split('@', 1)[1]
        if whitelisted_emails or whitelisted_domains:
            allowed = (email in whitelisted_emails or domain in
                       whitelisted_domains)

        # Check if the user email domain matches with one of the org oauth
        # domains and add the organization uuid in the details
        if not allowed:
            try:
                org_uuid = Organization.objects.values_list(
                    'organization_uuid', flat=True).get(
                    oauth_domains__contains=[domain])
                details.update({'organization_uuid': org_uuid})
                allowed = True
            except Organization.DoesNotExist:
                pass
            except Organization.MultipleObjectsReturned as e:
                logger.warning('There is more than one Organization with '
                               'the domain {}.\n{}'.format(domain, e))

    if not allowed:
        return render_to_response('unauthorized.html',
                                  context={'STATIC_URL': static_url})
