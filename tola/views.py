from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from tola.forms import RegistrationForm, NewUserRegistrationForm, NewTolaUserRegistrationForm, BookmarkForm
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from workflow.models import TolaUser,TolaSites, TolaBookmarks, FormGuidance, Organization
from indicators.models import CollectedData, Indicator

from django.shortcuts import get_object_or_404, redirect
from django.db.models import Sum, Q, Count
from tola.util import getCountry
from django.contrib.auth.models import Group

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import json
from feed.serializers import TolaUserSerializer, OrganizationSerializer

@login_required(login_url='/accounts/login/')
def index(request, selected_countries=None, id=0, sector=0):
    if request.user.is_authenticated():
        try:
            getSite = TolaSites.objects.get(name="TolaData")
            template = getSite.front_end_url
            return HttpResponseRedirect(template, content_type="application/x-www-form-urlencoded")
        except TolaSites.DoesNotExist as e:
            template = "index.html"
            return render(request, template)
    else:
        return redirect('register')


def register(request):
    """
    Register a new User profile using built in Django Users Model
    """
    privacy = ""
    org_error = False
    getSite = TolaSites.objects.get(name="TolaData")
    check_org = None

    if getSite:
        template = getSite.front_end_url
        privacy = getSite.privacy_disclaimer

    if request.method == 'POST':
        uf = NewUserRegistrationForm(request.POST)
        tf = NewTolaUserRegistrationForm(request.POST)

        # Get the Org and check to make sure it's real
        org = request.POST.get('org')
        print org
        try:
            check_org = Organization.objects.get(name=org)
        except Organization.DoesNotExist:
            # bad org name so ask them to check again
            messages.error(request, 'The Organization you entered was not found.', fail_silently=False)
            # reset org
            tf = NewTolaUserRegistrationForm()
            return render(request, "registration/register.html", {
                'userform': uf, 'tolaform': tf, 'helper': NewTolaUserRegistrationForm.helper, 'privacy': privacy,
                'org_error': True
            })

        # copy new post and alter with new org value
        new_post = request.POST.copy()
        new_post['organization'] = check_org
        # set new instances of form objects to validate
        user_form = NewUserRegistrationForm(new_post)
        tola_form = NewTolaUserRegistrationForm(new_post)

        if user_form.is_valid() * tola_form.is_valid():

            user = user_form.save()
            user.groups.add(Group.objects.get(name='ViewOnly'))

            tolauser = tola_form.save(commit=False)
            tolauser.user = user
            tolauser.organization = check_org
            tolauser.save()
            messages.error(request, 'Thank you, You have been registered as a new user.', fail_silently=False)
            # register user and redirect them to front end or home page depending on config
            if getSite:
                return HttpResponseRedirect("/accounts/login/")
            else:
                return HttpResponseRedirect("/")
    else:
        uf = NewUserRegistrationForm()
        tf = NewTolaUserRegistrationForm()


    return render(request, "registration/register.html", {
        'userform': uf,'tolaform': tf, 'helper': NewTolaUserRegistrationForm.helper,'privacy': privacy, 'org_error': False
    })


def profile(request):
    """
    Update a User profile using built in Django Users Model if the user is logged in
    otherwise redirect them to registration version
    """
    if request.user.is_authenticated():
        obj = get_object_or_404(TolaUser, user=request.user)
        form = RegistrationForm(request.POST or None, instance=obj,initial={'username': request.user})

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
        getUser = TolaUser.objects.all().filter(user=request.user)
        getBookmarks = TolaBookmarks.objects.all().filter(user=getUser)

        return render(request, self.template_name, {'getBookmarks':getBookmarks})


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
    Logout a user
    """
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")


def check_view(request):
    return HttpResponse("Hostname "+request.get_host())


def dev_view(request):
    """
    For DEV only update Tables with Activity data
    URL /dev_loader
    :param request:
    :return:
    """
    if request.user.is_authenticated() and request.user.username == "tola" and request.user.is_staff:
        from tola.tables_sync import update_level1, update_level2
        # update TolaTables with WorkflowLevel1 and WorkflowLevel2 data
        message = {"attempt": "Running Tables Loader"}

        print "Running Script..."

        try:
            update_level1()
            message['level1'] = "Level1 Success"
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            message['level1'] = '%s (%s)' % (e.message, type(e))

        try:
            update_level2()
            message['level2'] = "Level2 Success"
        except Exception as e:
            print '%s (%s)' % (e.message, type(e))
            message['level2'] = '%s (%s)' % (e.message, type(e))

        return render(request, "dev.html", {'message': message})
    else:
        # log person
        print request.user.is_authenticated()
        print request.user.username
        print request.user.is_staff
        redirect_url = '/'
        return HttpResponseRedirect(redirect_url)


from oauth2_provider.views.generic import ProtectedResourceView

def oauth_user_view(request):
    return HttpResponse("Hostname "+request.get_host())


class OAuth_User_Endpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):

        user = request.user
        body = {
            'username': user.username,
            'email': user.email,
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,

        }
        tola_user = TolaUser.objects.all().filter(user=user)
        if len(tola_user) == 1:
            body["tola_user"] = TolaUserSerializer(instance=tola_user[0], context={'request': request}).data
            body["organization"] = OrganizationSerializer(instance=tola_user[0].organization, context={'request': request}).data

        return HttpResponse(json.dumps(body))
