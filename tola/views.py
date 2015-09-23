from django.shortcuts import render
from .forms import FeedbackForm, RegistrationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from activitydb.models import ProjectAgreement, ProjectProposal, ProjectComplete, Program, Community, Sector,Country as ActivityCountry, Feedback, FAQ, Documentation
from indicators.models import CollectedData
from djangocosign.models import UserProfile
from djangocosign.models import Country
from .tables import IndicatorDataTable
from util import getCountry
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models import Q

from tola.util import getCountry

from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def index(request,id=0,sector=0):
    """
    Home page
    get count of proposals and agreements approved and total for dashboard
    """
    program_id = id
    countries = getCountry(request.user)
    getSectors = Sector.objects.all().exclude(program__isnull=True).select_related()

    if int(sector) == 0:
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries).exclude(proposal__isnull=True)
        sectors = Sector.objects.all()
    else:
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries, sector=sector).exclude(proposal__isnull=True)
        sectors = Sector.objects.all().filter(id=sector)

    if int(program_id) == 0:
        getFilteredName=None
        agreement_total_count = ProjectAgreement.objects.all().filter(sector__in=sectors, program__country__in=countries).count()
        complete_total_count = ProjectComplete.objects.all().filter(project_agreement__sector__in=sectors, program__country__in=countries).count()
        agreement_approved_count = ProjectAgreement.objects.all().filter(approval='approved', sector__in=sectors, program__country__in=countries).count()
        complete_approved_count = ProjectComplete.objects.all().filter(approval='approved', project_agreement__sector__in=sectors, program__country__in=countries).count()
        agreement_open_count = ProjectAgreement.objects.all().filter(approval='open', sector__id__in=sectors, program__country__in=countries).count()
        complete_open_count = ProjectComplete.objects.all().filter(Q(Q(approval='open') | Q(approval="")), project_agreement__sector__in=sectors, program__country__in=countries).count()
        agreement_wait_count = ProjectAgreement.objects.all().filter(approval='in progress', sector__in=sectors, program__country__in=countries).count()
        complete_wait_count = ProjectComplete.objects.all().filter(approval='in progress', project_agreement__sector__in=sectors, program__country__in=countries).count()
        if int(sector) > 0:
            getCommunity = Community.objects.all().filter(Q(Q(projectagreement__sector__in=sectors)), country__in=countries)
        else:
            getCommunity = Community.objects.all().filter(country__in=countries)
        getQuantitativeDataSums = CollectedData.objects.all().filter(Q(Q(agreement__sector__in=sectors)|Q(agreement__sector__isnull=True)), indicator__country__in=countries).order_by('indicator__number').values('indicator__number','indicator__name').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))

    else:
        getFilteredName=Program.objects.get(id=program_id)
        agreement_total_count = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries).count()
        complete_total_count = ProjectComplete.objects.all().filter(program__id=program_id, program__country__in=countries).count()
        agreement_approved_count = ProjectAgreement.objects.all().filter(program__id=program_id, approval='approved', program__country__in=countries).count()
        complete_approved_count = ProjectComplete.objects.all().filter(program__id=program_id, approval='approved', program__country__in=countries).count()
        agreement_open_count = ProjectAgreement.objects.all().filter(program__id=program_id, approval='open', program__country__in=countries).count()
        complete_open_count = ProjectComplete.objects.all().filter(Q(Q(approval='open') | Q(approval="")), program__id=program_id, program__country__in=countries).count()
        agreement_wait_count = ProjectAgreement.objects.all().filter(program__id=program_id, approval='in progress', program__country__in=countries).count()
        complete_wait_count = ProjectComplete.objects.all().filter(program__id=program_id, approval='in progress', program__country__in=countries).count()
        getCommunity = Community.objects.all().filter(projectagreement__program__id=program_id, projectagreement__sector__id=sector)
        getQuantitativeDataSums = CollectedData.objects.all().filter(indicator__program__id=program_id).order_by('indicator__number').values('indicator__number','indicator__name').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))

    table = IndicatorDataTable(getQuantitativeDataSums)
    table.paginate(page=request.GET.get('page', 1), per_page=20)

    return render(request, "index.html", {'agreement_total_count':agreement_total_count,\
                                          'agreement_approved_count':agreement_approved_count,\
                                          'agreement_open_count':agreement_open_count,\
                                          'agreement_wait_count':agreement_wait_count,\
                                          'complete_open_count':complete_open_count,\
                                          'complete_approved_count':complete_approved_count,'complete_total_count':complete_total_count,\
                                          'complete_wait_count':complete_wait_count,\
                                          'programs':getPrograms,'getCommunity':getCommunity,'country': countries,'getFilteredName':getFilteredName,'getSectors':getSectors,\
                                          'sector': sector, 'table': table, 'getQuantitativeDataSums':getQuantitativeDataSums
                                          })

def contact(request):
    """
    Feedback form
    """
    form = FeedbackForm(initial={'submitter': request.user})

    if request.method == 'POST':
        form = FeedbackForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            messages.error(request, 'Thank you', fail_silently=False)
        else:
            messages.error(request, 'Invalid', fail_silently=False)
            print form.errors

    return render(request, "contact.html", {'form': form, 'helper': FeedbackForm.helper})


def faq(request):
    """
    Get FAQ and display them on template
    """

    getFAQ = FAQ.objects.all()

    return render(request, 'faq.html', {'getFAQ': getFAQ})


def documentation(request):
    """
    Get Documentation and display them on template
    """

    getDocumentation = Documentation.objects.all()

    return render(request, 'documentation.html', {'getDocumentation': getDocumentation})


def register(request):
    """
    Register a new User profile using built in Django Users Model
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })


def profile(request):
    """
    Update a User profile using built in Django Users Model if the user is logged in
    otherwise redirect them to registration version
    """
    if request.user.is_authenticated():
        obj = get_object_or_404(UserProfile, user=request.user)
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


def logout_view(request):
    """
    Logout a user
    """
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")

