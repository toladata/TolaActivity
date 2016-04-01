from django.shortcuts import render
from .forms import FeedbackForm, RegistrationForm, NewUserRegistrationForm,NewTolaUserRegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from activitydb.models import ProjectAgreement, ProjectComplete, Program, SiteProfile, Sector,Country, FAQ, DocumentationApp, TolaUser, TolaSites
from indicators.models import CollectedData
from .tables import IndicatorDataTable
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q, Count
from tola.util import getCountry

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
        #transform to list if a submitted country
        selected_countries = [selected_countries]
        selected_countries_list = Country.objects.all().filter(id__in=selected_countries)



    getSectors = Sector.objects.all().exclude(program__isnull=True).select_related()

    #limit the programs by the selected sector
    if int(sector) == 0:
        getPrograms = Program.objects.all().prefetch_related('agreement','agreement__office').filter(funding_status="Funded", country__in=selected_countries).exclude(agreement__isnull=True)
        sectors = Sector.objects.all()
    else:
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=selected_countries, sector=sector).exclude(agreement__isnull=True)
        sectors = Sector.objects.all().filter(id=sector)

    #get data for just one program or all programs
    if int(program_id) == 0:
        getFilteredName=None
        #filter by all programs then filter by sector if found
        if int(sector) > 0:
            getSiteProfile = SiteProfile.objects.all().prefetch_related('country','district','province').filter(Q(Q(projectagreement__sector__in=sectors)), country__in=selected_countries)
            getSiteProfileIndicator = SiteProfile.objects.all().prefetch_related('country','district','province').filter(Q(collecteddata__program__country__in=selected_countries))
            agreement_total_count = ProjectAgreement.objects.all().filter(sector__in=sectors, program__country__in=selected_countries).count()
            complete_total_count = ProjectComplete.objects.all().filter(project_agreement__sector__in=sectors, program__country__in=selected_countries).count()
            agreement_approved_count = ProjectAgreement.objects.all().filter(approval='approved', sector__in=sectors, program__country__in=selected_countries).count()
            complete_approved_count = ProjectComplete.objects.all().filter(approval='approved', project_agreement__sector__in=sectors, program__country__in=selected_countries).count()
            agreement_open_count = ProjectAgreement.objects.all().filter(Q(Q(approval='open') | Q(approval="") | Q(approval=None)), sector__id__in=sectors, program__country__in=selected_countries).count()
            complete_open_count = ProjectComplete.objects.all().filter(Q(Q(approval='open') | Q(approval="") | Q(approval=None)), project_agreement__sector__in=sectors, program__country__in=selected_countries).count()
            agreement_wait_count = ProjectAgreement.objects.all().filter(Q(approval='in progress') & Q(Q(approval='in progress') | Q(approval=None) | Q(approval="")), sector__in=sectors, program__country__in=selected_countries).count()
            complete_wait_count = ProjectComplete.objects.all().filter(Q(approval='in progress') & Q(Q(approval='in progress') | Q(approval=None) | Q(approval="")), project_agreement__sector__in=sectors, program__country__in=selected_countries).count()
            getQuantitativeDataSums = CollectedData.objects.all().filter(Q(agreement__sector__in=sectors), indicator__key_performance_indicator=True, achieved__isnull=False, targeted__isnull=False, indicator__country__in=selected_countries).exclude(achieved=None,targeted=None).order_by('indicator__program','indicator__number').values('indicator__program__name','indicator__number','indicator__name','indicator__id').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))
        else:
            getSiteProfile = SiteProfile.objects.all().prefetch_related('country','district','province').filter(country__in=selected_countries)
            getSiteProfileIndicator = SiteProfile.objects.all().prefetch_related('country','district','province').filter(Q(collecteddata__program__country__in=selected_countries))
            agreement_total_count = ProjectAgreement.objects.all().filter(program__country__in=selected_countries).count()
            complete_total_count = ProjectComplete.objects.all().filter(program__country__in=selected_countries).count()
            agreement_approved_count = ProjectAgreement.objects.all().filter(approval='approved', program__country__in=selected_countries).count()
            complete_approved_count = ProjectComplete.objects.all().filter(approval='approved', program__country__in=selected_countries).count()
            agreement_open_count = ProjectAgreement.objects.all().filter(Q(Q(approval='open') | Q(approval="") | Q(approval=None)), program__country__in=selected_countries).count()
            complete_open_count = ProjectComplete.objects.all().filter(Q(Q(approval='open') | Q(approval="") | Q(approval=None)), program__country__in=selected_countries).count()
            agreement_wait_count = ProjectAgreement.objects.all().filter(Q(approval='in progress') & Q(Q(approval='in progress') | Q(approval=None) | Q(approval="")), program__country__in=selected_countries).count()
            complete_wait_count = ProjectComplete.objects.all().filter(Q(approval='in progress') & Q(Q(approval='in progress') | Q(approval=None) | Q(approval="")),program__country__in=selected_countries).count()
            getQuantitativeDataSums = CollectedData.objects.all().filter(Q(agreement__sector__isnull=True), indicator__key_performance_indicator=True, achieved__isnull=False, targeted__isnull=False, indicator__country__in=selected_countries).exclude(achieved=None,targeted=None).order_by('indicator__program','indicator__number').values('indicator__program__name','indicator__number','indicator__name','indicator__id').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))
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
        getSiteProfile = SiteProfile.objects.all().prefetch_related('country','district','province').filter(projectagreement__program__id=program_id)
        getSiteProfileIndicator = SiteProfile.objects.all().prefetch_related('country','district','province').filter(Q(collecteddata__program__id=program_id))
        getQuantitativeDataSums = CollectedData.objects.all().filter(indicator__key_performance_indicator=True, indicator__program__id=program_id,achieved__isnull=False).exclude(achieved=None,targeted=None).order_by('indicator__program','indicator__number').values('indicator__program__name','indicator__number','indicator__name','indicator__id').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))
    #Evidence and Objectives are for the global leader dashboard items and are the same every time
    count_evidence = CollectedData.objects.all().filter(indicator__isnull=False).values("indicator__country__country").annotate(evidence_count=Count('evidence', distinct=True) + Count('tola_table', distinct=True),indicator_count=Count('pk', distinct=True)).order_by('-evidence_count')
    getObjectives = CollectedData.objects.all().filter(indicator__strategic_objectives__isnull=False, indicator__country__in=selected_countries).exclude(achieved=None,targeted=None).order_by('indicator__strategic_objectives__name').values('indicator__strategic_objectives__name').annotate(indicators=Count('pk', distinct=True),targets=Sum('targeted'), actuals=Sum('achieved'))
    table = IndicatorDataTable(getQuantitativeDataSums)
    table.paginate(page=request.GET.get('page', 1), per_page=20)

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
                                          'selected_countries_list': selected_countries_list,
                                          'getSiteProfileIndicator': getSiteProfileIndicator
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
    privacy = TolaSites.objects.all().filter(id=1)
    if request.method == 'POST':
        uf = NewUserRegistrationForm(request.POST)
        tf = NewTolaUserRegistrationForm(request.POST)

        if uf.is_valid() * tf.is_valid():
            user = uf.save()
            user.groups.add(Group.objects.get(name='ViewOnly'))

            tolauser = tf.save(commit=False)
            tolauser.user = user
            tolauser.save()
            messages.error(request, 'Thank you, You have been registered as a new user.', fail_silently=False)
            return HttpResponseRedirect("/")
    else:
        uf = NewUserRegistrationForm()
        tf = NewTolaUserRegistrationForm()

    return render(request, "registration/register.html", {
        'userform': uf,'tolaform': tf, 'helper': NewTolaUserRegistrationForm.helper,'privacy':privacy
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


def logout_view(request):
    """
    Logout a user
    """
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/")

