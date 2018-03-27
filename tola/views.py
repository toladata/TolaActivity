import json
import os
from urlparse import urljoin
import warnings
import requests
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from oauth2_provider.views.generic import ProtectedResourceView

from social_django.utils import load_strategy
from chargebee import APIError, InvalidRequestError, Subscription

from tola import DEMO_BRANCH
from tola.track_sync import register_user
from tola.forms import RegistrationForm, NewUserRegistrationForm, \
    NewTolaUserRegistrationForm, BookmarkForm
from workflow.models import (Organization, TolaSites, TolaUser, TolaBookmarks,
                             FormGuidance, ROLE_VIEW_ONLY, TolaSites)

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if settings.TOLA_ACTIVITY_URL and settings.TOLA_TRACK_URL:
            extra_context = {
                'tolaactivity_url': settings.TOLA_ACTIVITY_URL,
                'tolatrack_url': settings.TOLA_TRACK_URL,
            }
        else:  # CE only
            warnings.warn(
                "TolaSite.front_end_url and TolaSite.tola_tables_url are "
                "deprecated. Please, set instead TOLA_ACTIVITY_URL and "
                "TOLA_TRACK_URL values in settings", DeprecationWarning)
            tola_site = TolaSites.objects.get(name="TolaData")
            extra_context = {
                'tolaactivity_url': tola_site.front_end_url,
                'tolatrack_url': tola_site.tola_tables_url,
            }
        context.update(extra_context)
        return context


class RegisterView(View):
    template_name = 'registration/register.html'

    def _get_context_data(self, params, **kwargs):
        context = {}
        try:  # CE only
            privacy_disclaimer = TolaSites.objects.values_list(
                'privacy_disclaimer', flat=True).get(name="TolaData")
        except TolaSites.DoesNotExist:
            privacy_disclaimer = ''
        context['privacy_disclaimer'] = privacy_disclaimer

        if kwargs:
            context.update(kwargs)

        # Auto fill some fields based on query parameters and set partial token
        if params:
            if 'organization_uuid' in params:
                org_uuid = params.get('organization_uuid', '')
                org_name = Organization.objects.values_list(
                    'name', flat=True).get(organization_uuid=org_uuid)
            else:
                org_name = params.get('cus_company', '')
            first_name = params.get('cus_fname', '')
            last_name = params.get('cus_lname', '')
            email = params.get('cus_email', '')
            context['form_tolauser'] = NewTolaUserRegistrationForm(org=org_name)
            context['form_user'] = NewUserRegistrationForm(
                first_name=first_name, last_name=last_name, email=email)
        return context

    def _get_chargebee_data(self, params, **kwargs):
        context = {}
        context.update(kwargs)
        org_name = params.get('cus_company', '')
        sub_id = params.get('sub_id', '')

        if not org_name and not sub_id:
            return context

        # Check subscription id and
        # Create an organization defined on ChargeBee
        try:
            result = Subscription.retrieve(sub_id)
        except InvalidRequestError:
            logger.info('The given subscription id ({}) is not valid.'.format(
                sub_id))
        except APIError as e:
            logger.warn(e)
        else:
            subscription = result.subscription
            if subscription.status in ['active', 'in_trial']:
                org = Organization.objects.get_or_create(name=org_name)[0]
                org.chargebee_subscription_id = sub_id
                org.save()
        return context

    def get(self, request, *args, **kwargs):
        extra_context = {
            'form_user': NewUserRegistrationForm(),
            'form_tolauser': NewTolaUserRegistrationForm(),
        }
        if (request.GET.get('sub_id', None) and
                os.getenv('APP_BRANCH') != DEMO_BRANCH):
            extra_context = self._get_chargebee_data(
                request.GET, **extra_context)
        context = self._get_context_data(request.GET, **extra_context)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        register_form = request.POST.copy()

        # Check if an organization uuid was given and create the user
        # associate with that organization
        if 'org' not in register_form:
            org_name = ''
            if 'organization_uuid' in request.GET:
                org_uuid = request.GET.get('organization_uuid', '')
                org_name = Organization.objects.values_list(
                    'name', flat=True).get(organization_uuid=org_uuid)
            elif 'cus_company' in request.GET:
                org_name = request.GET.get('cus_company', '')
            register_form.appendlist('org', org_name)
        partial_token = request.GET.get('partial_token', '')

        # Create the user and tola user django forms for validation
        form_user = NewUserRegistrationForm(register_form)
        form_tolauser = NewTolaUserRegistrationForm(register_form)

        if form_user.is_valid() and form_tolauser.is_valid():
            user = form_user.save()
            user.groups.add(Group.objects.get(name=ROLE_VIEW_ONLY))

            tolauser = form_tolauser.save(commit=False)
            tolauser.user = user
            tolauser.organization = form_tolauser.cleaned_data.get('org')
            tolauser.name = ' '.join([user.first_name, user.last_name]).strip()
            tolauser.save()
            register_form.appendlist('tola_user_uuid', tolauser.tola_user_uuid)
            register_user(register_form, tolauser)
            messages.error(
                request,
                'Thank you, You have been registered as a new user.',
                fail_silently=False)
            if partial_token:
                strategy = load_strategy()
                partial = strategy.partial_load(partial_token)
                return redirect('social:complete', backend=partial.backend)
            return HttpResponseRedirect(reverse('login'))

        context = self._get_context_data(request.GET, **{
            'form_user': form_user,
            'form_tolauser': form_tolauser,
        })
        return render(request, self.template_name, context)


def profile(request):
    """
    Update a User profile using built in Django Users Model if the user is logged in
    otherwise redirect them to registration version
    """
    if request.user.is_authenticated():
        obj = get_object_or_404(TolaUser, user=request.user)
        form = RegistrationForm(request.POST or None, instance=obj, initial={'username': request.user})

        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.error(request, 'Your profile has been updated.', fail_silently=False)

        return render(request, "registration/profile.html", {
            'form': form, 'helper': RegistrationForm.helper
        })
    else:
        return HttpResponseRedirect("/accounts/register")


class BookmarkList(ListView):
    """
    Bookmark Report filtered by project
    """
    model = TolaBookmarks
    template_name = 'registration/bookmark_list.html'

    def get(self, request, *args, **kwargs):
        get_user = TolaUser.objects.all().filter(user=request.user)
        get_bookmarks = TolaBookmarks.objects.all().filter(user=get_user)

        return render(request, self.template_name, {'getBookmarks': get_bookmarks})


class BookmarkCreate(CreateView):
    """
    Using Bookmark Form for new bookmark per user
    """
    model = TolaBookmarks
    template_name = 'registration/bookmark_form.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Bookmarks")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(BookmarkCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(BookmarkCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):

        initial = {
            'user': self.request.user,
        }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Bookmark Created!')
        latest = TolaBookmarks.objects.latest('id')
        redirect_url = '/bookmark_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = BookmarkForm


class BookmarkUpdate(UpdateView):
    """
    Bookmark Form Update an existing site profile
    """
    model = TolaBookmarks
    template_name = 'registration/bookmark_form.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Bookmarks")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(BookmarkUpdate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):

        initial = {
            'user': self.request.user,
        }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Bookmark Updated!')
        latest = TolaBookmarks.objects.latest('id')
        redirect_url = '/bookmark_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = BookmarkForm


class BookmarkDelete(DeleteView):
    """
    Bookmark Form Delete an existing bookmark
    """
    model = TolaBookmarks
    template_name = 'registration/bookmark_confirm_delete.html'
    success_url = "/bookmark_list"

    def dispatch(self, request, *args, **kwargs):
        return super(BookmarkDelete, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Bookmark Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = BookmarkForm


def logout_view(request):
    """
    Logout a user in activity and track
    """
    # Redirect to track, so the user will
    # be logged out there as well
    if request.user.is_authenticated:
        logout(request)
        url_subpath = 'accounts/logout/'
        url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
        return HttpResponseRedirect(url)

    return HttpResponseRedirect("/")


def check_view(request):
    return HttpResponse("Hostname " + request.get_host())


def oauth_user_view(request):
    return HttpResponse("Hostname "+request.get_host())


class OAuthUserEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        pass


class TolaTrackSiloProxy(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        headers = {
            "content-type": "application/json",
            'Authorization': 'Token {}'.format(settings.TOLA_TRACK_TOKEN),
        }

        tola_user_uuid = TolaUser.objects.values_list(
            'tola_user_uuid', flat=True).get(user=request.user)

        url_subpath = 'api/silo'
        url_base = urljoin(settings.TOLA_TRACK_URL, url_subpath)
        url = '{}?user_uuid={}'.format(url_base, tola_user_uuid)

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return HttpResponse(response.content)
        else:
            reason = 'URL: {}. Responded with status code {}'.format(
                url, response.status_code)
            return HttpResponse(status=502, reason=reason)


class TolaTrackSiloDataProxy(ProtectedResourceView):
    def get(self, request, silo_id, *args, **kwargs):
        headers = {
            "content-type": "application/json",
            'Authorization': 'Token {}'.format(settings.TOLA_TRACK_TOKEN),
        }

        url_subpath = 'api/silo/{}/data'.format(silo_id)
        url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return HttpResponse(response.content)
        else:
            reason = 'URL: {}. Responded with status code {}'.format(
                url, response.status_code)
            return HttpResponse(status=502, reason=reason)
