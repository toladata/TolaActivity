from django.views.generic.list import ListView

from django.shortcuts import render
from activitydb.models import ProjectAgreement, ProjectComplete, CustomDashboard, Program, SiteProfile,Country, TolaSites
from customdashboard.models import OverlayGroups, OverlayNarratives
from .models import ProjectStatus, Gallery
from indicators.models import CollectedData

from django.db.models import Sum
from django.db.models import Q

from tola.util import getCountry

from django.contrib.auth.decorators import login_required
import requests
import json

@login_required(login_url='/accounts/login/')

def DefaultCustomDashboard(request,id=0,sector=0,status=0):
    """
    # of agreements, approved, rejected, waiting, archived and total for dashboard
    """
    program_id = id

    countries = getCountry(request.user)

    #transform to list if a submitted country
    selected_countries_list = Country.objects.all().filter(program__id=program_id)

    getQuantitativeDataSums = CollectedData.objects.all().filter(indicator__program__id=program_id,achieved__isnull=False, indicator__key_performance_indicator=True).exclude(achieved=None,targeted=None).order_by('indicator__number').values('indicator__number','indicator__name','indicator__id').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))
    getFilteredName=Program.objects.get(id=program_id)
    getProjectStatus = ProjectStatus.objects.all()

    getProjectsCount = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries).count()
    getBudgetEstimated = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries).annotate(estimated=Sum('total_estimated_budget'))
    getAwaitingApprovalCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='', program__country__in=countries).count()
    getApprovedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='approved', program__country__in=countries).count()
    getRejectedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='rejected', program__country__in=countries).count()
    getInProgressCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='in progress', program__country__in=countries).count()

    getSiteProfile = SiteProfile.objects.all().filter(Q(projectagreement__program__id=program_id) | Q(collecteddata__program__id=program_id))
    getSiteProfileIndicator = SiteProfile.objects.all().filter(Q(collecteddata__program__id=program_id))


    if (status) =='Approved':
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries,approval='approved')
    elif(status) =='Rejected':
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries,approval='rejected')
    elif(status) =='In Progress':
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries,approval='in progress')
    elif(status) =='Awaiting Approval':
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries,approval='awaiting approval')
    else:
        getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries)

    getCustomDashboard = CustomDashboard.objects.all()



    return render(request, "customdashboard/visual_dashboard.html", {'getSiteProfile':getSiteProfile, 'getBudgetEstimated': getBudgetEstimated, 'getQuantitativeDataSums': getQuantitativeDataSums,
                                                                     'country': countries, 'getProjectStatus': getProjectStatus, 'getAwaitingApprovalCount':getAwaitingApprovalCount,
                                                                     'getFilteredName': getFilteredName,'getProjects': getProjects, 'getApprovedCount': getApprovedCount,
                                                                     'getRejectedCount': getRejectedCount, 'getInProgressCount': getInProgressCount,
                                                                     'getCustomDashboard': getCustomDashboard, 'getProjectsCount': getProjectsCount, 'selected_countries_list': selected_countries_list,
                                                                     'getSiteProfileIndicator': getSiteProfileIndicator})


def PublicDashboard(request,id=0):
    program_id = id
    getQuantitativeDataSums_2 = CollectedData.objects.all().filter(indicator__key_performance_indicator=True, indicator__program__id=program_id,achieved__isnull=False).order_by('indicator__source').values('indicator__number','indicator__source','indicator__id')
    getQuantitativeDataSums = CollectedData.objects.all().filter(indicator__key_performance_indicator=True, indicator__program__id=program_id,achieved__isnull=False).exclude(achieved=None,targeted=None).order_by('indicator__number').values('indicator__number','indicator__name','indicator__id').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))
    getProgram = Program.objects.all().get(id=program_id)
    getOverlayGroups = OverlayGroups.objects.all()
    getOverlayNarrative = OverlayNarratives.objects.all()
    getProjects = ProjectComplete.objects.all().filter(program_id=program_id)
    getSiteProfile = SiteProfile.objects.all().filter(projectagreement__program__id=program_id)
    getSiteProfileIndicator = SiteProfile.objects.all().filter(Q(collecteddata__program__id=program_id))

    getProjectsCount = ProjectAgreement.objects.all().filter(program__id=program_id).count()
    getAwaitingApprovalCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='awaiting approval').count()
    getApprovedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='approved').count()
    getRejectedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='rejected').count()
    getInProgressCount = ProjectAgreement.objects.all().filter(Q(program__id=program_id) & Q(Q(approval='in progress') | Q(approval=None) | Q(approval=""))).count()

    #get all countires
    countries = Country.objects.all().filter(program__id=program_id)

    return render(request, "publicdashboard/public_dashboard.html", {'getProgram':getProgram,'getProjects':getProjects,
                                                                     'getSiteProfile':getSiteProfile, 'getOverlayGroups':getOverlayGroups,
                                                                     'countries': countries, 'getOverlayNarrative': getOverlayNarrative,
                                                                     'awaiting':getAwaitingApprovalCount,'getQuantitativeDataSums_2':getQuantitativeDataSums_2,
                                                                     'approved': getApprovedCount,
                                                                     'rejected': getRejectedCount,
                                                                     'in_progress': getInProgressCount,
                                                                     'total_projects': getProjectsCount,
                                                                     'getQuantitativeDataSums': getQuantitativeDataSums,
                                                                     'getSiteProfileIndicator': getSiteProfileIndicator})


def SurveyPublicDashboard(request,id=0):

    # get all countires
    countries = Country.objects.all()

    filter_url = "https://tola-tables.mercycorps.org/api/silo/430/data/"
    token = TolaSites.objects.get(site_id=1)
    if token.tola_tables_token:
        headers = {'content-type': 'application/json',
                   'Authorization': 'Token ' + token.tola_tables_token}
    else:
        headers = {'content-type': 'application/json'}
        print "Token Not Found"

    response = requests.get(filter_url, headers=headers, verify=False)
    get_json = json.loads(response.content)
    data = get_json
    # print data
    meaning = []
    join = []
    tola_is = []
    for item in data:
        meaning.append(item['tola_is_a_pashto_word_meaning_'])
        # multiple choice
        join.append(list(x for x in item['thanks_for_coming_what_made_you_join_us_today_'].split()))
        # multiple choice
        tola_is.append(list(x for x in item['tola_is_a_system_for_'].split()))
    """
    meaning: all_or_complet,peaceful,global,i_give_up
    join: tola_is_a_myst, i_like_beer,to_meet_the_team,not_sure_what_
    tola_is: adaptive_manag an_indicator_t a_data_managem option_4 all_of_the_abo
    """
    meaningcount = {}
    meaningcount['peaceful'] = 0
    meaningcount['is_global'] = 0
    meaningcount['i_give_up'] = 0
    meaningcount['all_or_complete'] = 0
    for answer in meaning:
        if answer == "all_or_complet":
            meaningcount['all_or_complete'] = meaningcount['all_or_complete'] + 1
        if answer == "global":
            meaningcount['is_global'] = meaningcount['is_global'] + 1
        if answer == "i_give_up":
            meaningcount['i_give_up'] = meaningcount['i_give_up'] + 1
        if answer == "peaceful":
            meaningcount['peaceful'] = meaningcount['peaceful'] + 1

    joincount = {}
    joincount['tola_is_a_mystery'] = 0
    joincount['i_like_beer'] = 0
    joincount['to_meet_the_team'] = 0
    joincount['not_sure'] = 0
    for answer in join:
        if "tola_is_a_myst" in answer:
            joincount['tola_is_a_mystery'] = joincount['tola_is_a_mystery'] + 1
        if "i_like_beer" in answer:
            joincount['i_like_beer'] = joincount['i_like_beer'] + 1
        if "to_meet_the_team" in answer:
            joincount['to_meet_the_team'] = joincount['to_meet_the_team'] + 1
        if "not_sure_what_" in answer:
            joincount['not_sure'] = joincount['not_sure'] + 1

    tolacount = {}
    tolacount['adaptive_manag'] = 0
    tolacount['an_indicator_t'] = 0
    tolacount['a_data_managem'] = 0
    tolacount['option_4'] = 0
    tolacount['all_of_the_abo'] = 0
    for answer in tola_is:
        if "adaptive_manag" in answer:
            tolacount['adaptive_manag'] = tolacount['adaptive_manag'] + 1
        if "an_indicator_t" in answer:
            tolacount['an_indicator_t'] = tolacount['an_indicator_t'] + 1
        if "a_data_managem" in answer:
            tolacount['a_data_managem'] = tolacount['a_data_managem'] + 1
        if "option_4" in answer:
            tolacount['option_4'] = tolacount['option_4'] + 1
        if "all_of_the_abo" in answer:
            tolacount['all_of_the_abo'] = tolacount['all_of_the_abo'] + 1

    dashboard = True

    return render(request, "publicdashboard/survey_public_dashboard.html", {'meaning':meaningcount,'join':joincount,'tola_is':tolacount, 'countries': countries, 'dashboard':dashboard})


def SurveyTalkPublicDashboard(request,id=0):

    # get all countires
    countries = Country.objects.all()

    filter_url = "http://tables.toladata.io/api/silo/9/data/"

    headers = {'content-type': 'application/json',
               'Authorization': 'Token bd43de0c16ac0400bc404c6598a6fe0e4ce73aa2'}


    response = requests.get(filter_url, headers=headers, verify=False)
    get_json = json.loads(response.content)
    data = get_json
    # print data
    meaning = []
    join = []
    tola_is = []
    country_from = []
    for item in data:
        meaning.append(item['tola_is_a_pashto_word_meaning_'])
        # multiple choice
        join.append(list(x for x in item['thanks_for_coming_what_made_you_join_us_today_'].split()))
        # multiple choice
        tola_is.append(list(x for x in item['tola_is_a_system_for_'].split()))
        # country
        country_from.append(item['what_country_were_you_in_last'])
    """
    meaning: all_or_complet,peaceful,global,i_give_up
    join: tola_is_a_myst, i_like_a_good_power_point,data_is_king,not_sure_what_
    tola_is: adaptive_manag an_indicator_t a_data_managem option_4 all_of_the_abo
    """
    meaningcount = {}
    meaningcount['peaceful'] = 0
    meaningcount['is_global'] = 0
    meaningcount['i_give_up'] = 0
    meaningcount['all_or_complete'] = 0
    for answer in meaning:
        if answer == "all_or_complet":
            meaningcount['all_or_complete'] = meaningcount['all_or_complete'] + 1
        if answer == "global":
            meaningcount['is_global'] = meaningcount['is_global'] + 1
        if answer == "i_give_up":
            meaningcount['i_give_up'] = meaningcount['i_give_up'] + 1
        if answer == "peaceful":
            meaningcount['peaceful'] = meaningcount['peaceful'] + 1

    joincount = {}
    joincount['tola_is_a_mystery'] = 0
    joincount['i_like_power_point_templates'] = 0
    joincount['data_is_king'] = 0
    joincount['not_sure'] = 0
    for answer in join:
        if "tola_is_a_mystery" in answer:
            joincount['tola_is_a_mystery'] = joincount['tola_is_a_mystery'] + 1
        if "i_like_power_point_templates" in answer:
            joincount['i_like_power_point_templates'] = joincount['i_like_power_point_templates'] + 1
        if "data_is_king" in answer:
            joincount['data_is_king'] = joincount['data_is_king'] + 1
        if "not_sure_what_" in answer:
            joincount['not_sure'] = joincount['not_sure'] + 1

    tolacount = {}
    tolacount['adaptive_manag'] = 0
    tolacount['an_indicator_t'] = 0
    tolacount['a_data_managem'] = 0
    tolacount['option_4'] = 0
    tolacount['all_of_the_abo'] = 0
    for answer in tola_is:
        if "adaptive_manag" in answer:
            tolacount['adaptive_manag'] = tolacount['adaptive_manag'] + 1
        if "an_indicator_t" in answer:
            tolacount['an_indicator_t'] = tolacount['an_indicator_t'] + 1
        if "a_data_managem" in answer:
            tolacount['a_data_managem'] = tolacount['a_data_managem'] + 1
        if "option_4" in answer:
            tolacount['option_4'] = tolacount['option_4'] + 1
        if "all_of_the_abo" in answer:
            tolacount['all_of_the_abo'] = tolacount['all_of_the_abo'] + 1

    dashboard = True

    return render(request, "publicdashboard/survey_talk_public_dashboard.html", {'meaning':meaningcount,'join':joincount,'tola_is':tolacount, 'country_from': country_from, 'countries': countries, 'dashboard':dashboard})


def ReportPublicDashboard(request,id=0):

    # get all countires
    countries = Country.objects.all()
    report = True

    return render(request, "publicdashboard/survey_public_dashboard.html", {'countries': countries, 'report':report})


def Gallery(request,id=0):
    program_id = id
    getProgram = Program.objects.all().filter(id=program_id)
    getGallery = Gallery.objects.all().filter(program_name__id=program_id)
    return render(request, "gallery/gallery.html", {'getGallery':getGallery, 'getProgram':getProgram})


class ProgramList(ListView):
    """
    Documentation
    """
    model = Program
    template_name = 'customdashboard/program_list.html'

    def get(self, request, *args, **kwargs):
        getCountry = Country.objects.all()

        if int(self.kwargs['pk']) == 0:
            getProgram = Program.objects.all().filter(dashboard_name__is_public=1)
        else:
            getProgram = Program.objects.all().filter(dashboard_name__is_public=1, country__id=self.kwargs['pk'])

        return render(request, self.template_name, {'getProgram': getProgram, 'getCountry': getCountry})


class InternalDashboard(ListView):
    """
    Internal Dashboard for user.is_authenticated
    """
    model = Program
    template_name = 'customdashboard/internal_dashboard.html'

    def get(self, request, *args, **kwargs):
        getCountry = Country.objects.all()

        if int(self.kwargs['pk']) == 0:
            getProgram = Program.objects.all().filter(dashboard_name__is_public=0)
        else:
            getProgram = Program.objects.all().filter(dashboard_name__is_public=0, country__id=self.kwargs['pk'])

        return render(request, self.template_name, {'getProgram': getProgram, 'getCountry': getCountry})

