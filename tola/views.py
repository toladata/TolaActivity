from django.shortcuts import render
from .forms import FeedbackForm, RegistrationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from activitydb.models import ProjectAgreement, ProjectComplete, Program, SiteProfile, Sector,Country as ActivityCountry, Feedback, FAQ, DocumentationApp
from indicators.models import CollectedData
from djangocosign.models import UserProfile
from djangocosign.models import Country
from .tables import IndicatorDataTable
from util import getCountry
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q, Count
import collections
from tola.util import getCountry
from settings.local import REPORT_SERVER

from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def index(request,selected_countries=None,id=0,sector=0):
    """
    Home page
    get count of agreements approved and total for dashboard
    """
    program_id = id
    user_countries = getCountry(request.user)
    if not selected_countries:
        selected_countries = user_countries
        selected_countries_list = None
    else:
        selected_countries_list = ActivityCountry.objects.all().filter(id__in=selected_countries)

    getSectors = Sector.objects.all().exclude(program__isnull=True).select_related()

    #limit the programs by the selected sector
    if int(sector) == 0:
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=selected_countries).exclude(agreement__isnull=True)
        sectors = Sector.objects.all()
    else:
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=selected_countries, sector=sector).exclude(agreement__isnull=True)
        sectors = Sector.objects.all().filter(id=sector)

    #get data for just one program or all programs
    if int(program_id) == 0:
        getFilteredName=None
        #filter by all programs then filter by sector if found
        if int(sector) > 0:
            getSiteProfile = SiteProfile.objects.all().filter(Q(Q(projectagreement__sector__in=sectors)), country__in=selected_countries)
            agreement_total_count = ProjectAgreement.objects.all().filter(sector__in=sectors, program__country__in=selected_countries).count()
            complete_total_count = ProjectComplete.objects.all().filter(project_agreement__sector__in=sectors, program__country__in=selected_countries).count()
            agreement_approved_count = ProjectAgreement.objects.all().filter(approval='approved', sector__in=sectors, program__country__in=selected_countries).count()
            complete_approved_count = ProjectComplete.objects.all().filter(approval='approved', project_agreement__sector__in=sectors, program__country__in=selected_countries).count()
            agreement_open_count = ProjectAgreement.objects.all().filter(Q(Q(approval='open') | Q(approval="") | Q(approval=None)), sector__id__in=sectors, program__country__in=selected_countries).count()
            complete_open_count = ProjectComplete.objects.all().filter(Q(Q(approval='open') | Q(approval="") | Q(approval=None)), project_agreement__sector__in=sectors, program__country__in=selected_countries).count()
            agreement_wait_count = ProjectAgreement.objects.all().filter(Q(approval='in progress') & Q(Q(approval='in progress') | Q(approval=None) | Q(approval="")), sector__in=sectors, program__country__in=selected_countries).count()
            complete_wait_count = ProjectComplete.objects.all().filter(Q(approval='in progress') & Q(Q(approval='in progress') | Q(approval=None) | Q(approval="")), project_agreement__sector__in=sectors, program__country__in=selected_countries).count()
            getQuantitativeDataSums = CollectedData.objects.all().filter(Q(agreement__sector__in=sectors), achieved__isnull=False, targeted__isnull=False, indicator__country__in=selected_countries).exclude(achieved=None,targeted=None).order_by('indicator__number').values('indicator__number','indicator__name','indicator__id').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))
        else:
            getSiteProfile = SiteProfile.objects.all().filter(country__in=selected_countries)
            agreement_total_count = ProjectAgreement.objects.all().filter(program__country__in=selected_countries).count()
            complete_total_count = ProjectComplete.objects.all().filter(program__country__in=selected_countries).count()
            agreement_approved_count = ProjectAgreement.objects.all().filter(approval='approved', program__country__in=selected_countries).count()
            complete_approved_count = ProjectComplete.objects.all().filter(approval='approved', program__country__in=selected_countries).count()
            agreement_open_count = ProjectAgreement.objects.all().filter(Q(Q(approval='open') | Q(approval="") | Q(approval=None)), program__country__in=selected_countries).count()
            complete_open_count = ProjectComplete.objects.all().filter(Q(Q(approval='open') | Q(approval="") | Q(approval=None)), program__country__in=selected_countries).count()
            agreement_wait_count = ProjectAgreement.objects.all().filter(Q(approval='in progress') & Q(Q(approval='in progress') | Q(approval=None) | Q(approval="")), program__country__in=selected_countries).count()
            complete_wait_count = ProjectComplete.objects.all().filter(Q(approval='in progress') & Q(Q(approval='in progress') | Q(approval=None) | Q(approval="")),program__country__in=selected_countries).count()
            getQuantitativeDataSums = CollectedData.objects.all().filter(Q(agreement__sector__isnull=True), achieved__isnull=False, targeted__isnull=False, indicator__country__in=selected_countries).exclude(achieved=None,targeted=None).order_by('indicator__number').values('indicator__number','indicator__name','indicator__id').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))
    else:
        getFilteredName=Program.objects.get(id=program_id)
        agreement_total_count = ProjectAgreement.objects.all().filter(program__id=program_id).count()
        complete_total_count = ProjectComplete.objects.all().filter(program__id=program_id).count()
        agreement_approved_count = ProjectAgreement.objects.all().filter(program__id=program_id, approval='approved').count()
        complete_approved_count = ProjectComplete.objects.all().filter(program__id=program_id, approval='approved').count()
        agreement_open_count = ProjectAgreement.objects.all().filter(program__id=program_id, approval='open').count()
        complete_open_count = ProjectComplete.objects.all().filter(Q(Q(approval='open') | Q(approval="")), program__id=program_id).count()
        agreement_wait_count = ProjectAgreement.objects.all().filter(Q(program__id=program_id), Q(approval='in progress') & Q(Q(approval='in progress') | Q(approval=None) | Q(approval=""))).count()
        complete_wait_count = ProjectComplete.objects.all().filter(Q(program__id=program_id), Q(approval='in progress') & Q(Q(approval='in progress') | Q(approval=None) | Q(approval=""))).count()
        getSiteProfile = SiteProfile.objects.all().filter(projectagreement__program__id=program_id)
        getQuantitativeDataSums = CollectedData.objects.all().filter(indicator__program__id=program_id,achieved__isnull=False).exclude(achieved=None,targeted=None).order_by('indicator__number').values('indicator__number','indicator__name','indicator__id').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))
    #Evidence and Objectives are for the global leader dashboard items and are the same every time
    count_evidence = CollectedData.objects.all().filter(indicator__isnull=False).values("indicator__country__country").annotate(evidence_count=Count('evidence', distinct=True),indicator_count=Count('pk', distinct=True)).order_by('-evidence_count')
    getObjectives = CollectedData.objects.all().filter(indicator__strategic_objectives__isnull=False, indicator__country__in=selected_countries).exclude(achieved=None,targeted=None).order_by('indicator__strategic_objectives__name').values('indicator__strategic_objectives__name').annotate(indicators=Count('pk', distinct=True),targets=Sum('targeted'), actuals=Sum('achieved'))
    table = IndicatorDataTable(getQuantitativeDataSums)
    table.paginate(page=request.GET.get('page', 1), per_page=20)
    print selected_countries_list
    return render(request, "index.html", {'agreement_total_count':agreement_total_count,\
                                          'agreement_approved_count':agreement_approved_count,\
                                          'agreement_open_count':agreement_open_count,\
                                          'agreement_wait_count':agreement_wait_count,\
                                          'complete_open_count':complete_open_count,\
                                          'complete_approved_count':complete_approved_count,'complete_total_count':complete_total_count,\
                                          'complete_wait_count':complete_wait_count,\
                                          'programs':getPrograms,'getSiteProfile':getSiteProfile,'countries': user_countries,'selected_countries':selected_countries,'getFilteredName':getFilteredName,'getSectors':getSectors,\
                                          'sector': sector, 'table': table, 'getQuantitativeDataSums':getQuantitativeDataSums,\
                                          'count_evidence':count_evidence,
                                          'getObjectives':getObjectives,
                                          'selected_countries_list': selected_countries_list
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

    getDocumentation = DocumentationApp.objects.all()

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

