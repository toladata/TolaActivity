from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.http import HttpResponse

from django.shortcuts import render
from workflow.models import ProjectAgreement, ProjectComplete, Program, SiteProfile,Country, TolaSites
from customdashboard.models import ProgramNarratives, JupyterNotebooks
from formlibrary.models import TrainingAttendance, Distribution, Beneficiary
from indicators.models import CollectedData, Indicator

from django.db.models import Sum
from django.db.models import Q

from tola.util import getCountry

from django.contrib.auth.decorators import login_required
import uuid
import requests
import json


class ProgramList(ListView):
    """
    List of Programs with links to the dashboards
    http://127.0.0.1:8000/customdashboard/program_list/0/
    """
    model = Program
    template_name = 'customdashboard/program_list.html'

    def get(self, request, *args, **kwargs):

        ## retrieve the coutries the user has data access for
        country = None
        countries = getCountry(request.user)
        country_list = Country.objects.all().filter(id__in=countries)
        if int(self.kwargs['pk']) == 0:
            getProgram = Program.objects.all().filter(country__in=countries)
        else:
            getProgram = Program.objects.all().filter(country__id=self.kwargs['pk'])
            country = Country.objects.get(id=self.kwargs['pk']).country

        program_list = []
        for program in getProgram:
            # get the percentage of indicators with data
            getInidcatorDataCount = Indicator.objects.filter(program__id=program.id).exclude(collecteddata__targeted=None).count()
            getInidcatorCount = Indicator.objects.filter(program__id=program.id).count()
            if getInidcatorCount > 0 and getInidcatorDataCount > 0:
                getInidcatorDataPercent = 100 * float(getInidcatorDataCount) / float(getInidcatorCount)
            else:
                getInidcatorDataPercent = 0

            program.indicator_data_percent = int(getInidcatorDataPercent)
            program.indicator_percent = int(100 - getInidcatorDataPercent)

            # get the percentage of projects with completes (tracking)
            getProjectAgreementCount = ProjectAgreement.objects.filter(program__id=program.id).count()
            getProjectCompleteCount = ProjectComplete.objects.filter(program__id=program.id).count()
            if getProjectAgreementCount > 0 and getProjectCompleteCount > 0:
                project_percent = 100 * float(getProjectCompleteCount) / float(getProjectAgreementCount)
            else:
                project_percent = 0

            # append the percentages to the program list
            program.project_percent = int(project_percent)
            program.project_agreement_percent = int(100 - project_percent)
            program_list.append(program)

        return render(request, self.template_name, {'getProgram': program_list, 'getCountry': country_list, 'country': country})


class InternalDashboard(ListView):
    """
    List of Programs with links to the dashboards
    Internal Dashboard user.is_authenticated can see all programs and links to internal dashboard
    http://127.0.0.1:8000/customdashboard/program_list/0/
    """
    model = Program
    template_name = 'customdashboard/program_list.html'

    def get(self, request, *args, **kwargs):
        getCountry = Country.objects.all()

        if int(self.kwargs['pk']) == 0:
            getProgram = Program.objects.all().filter(public_dashboard=0)
        else:
            getProgram = Program.objects.all().filter(public_dashboard=0, country__id=self.kwargs['pk'])

        return render(request, self.template_name, {'getProgram': getProgram, 'getCountry': getCountry})


@login_required(login_url='/accounts/login/')
def DefaultCustomDashboard(request,id=0,sector=0,status=0):
    """
    # of agreements, approved, rejected, waiting, archived and total for dashboard
    """
    program_id = id

    countries = getCountry(request.user)

    #transform to list if a submitted country
    selected_countries_list = Country.objects.all().filter(program__id=program_id)

    getQuantitativeDataSums = CollectedData.objects.filter(indicator__program__id=program_id,achieved__isnull=False, indicator__key_performance_indicator=True).exclude(achieved=None,targeted=None).order_by('indicator__number').values('indicator__number','indicator__name','indicator__id').annotate(targets=Sum('targeted'), actuals=Sum('achieved')).exclude(achieved=None,targeted=None)
    
    getFilteredName=Program.objects.get(id=program_id)
    
    getProjectsCount = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries).count()
    getBudgetEstimated = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries).annotate(estimated=Sum('total_estimated_budget'))
    getAwaitingApprovalCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='awaiting approval', program__country__in=countries).count()
    getApprovedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='approved', program__country__in=countries).count()
    getRejectedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='rejected', program__country__in=countries).count()
    getInProgressCount = ProjectAgreement.objects.all().filter(program__id=program_id).filter(Q(Q(approval='in progress') | Q(approval=None)), program__country__in=countries).count()
    nostatus_count = ProjectAgreement.objects.all().filter(program__id=program_id).filter(Q(Q(approval=None) | Q(approval=""))).count()
    print getInProgressCount


    getSiteProfile = SiteProfile.objects.all().filter(Q(projectagreement__program__id=program_id) | Q(collecteddata__program__id=program_id))
    getSiteProfileIndicator = SiteProfile.objects.all().filter(Q(collecteddata__program__id=program_id))

    if (status) =='Approved':
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries, approval='approved').prefetch_related('projectcomplete')
    elif(status) =='Rejected':
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries, approval='rejected').prefetch_related('projectcomplete')
    elif(status) =='In Progress':
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries, approval='in progress').prefetch_related('projectcomplete')
    elif(status) =='Awaiting Approval':
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries, approval='awaiting approval').prefetch_related('projectcomplete')
    else:
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries)

    get_project_completed = []
    getProjectsComplete = ProjectComplete.objects.all()
    for project in getProjects:
        for complete in getProjectsComplete:
            if complete.actual_budget != None:
                if project.id == complete.project_agreement_id:

                    get_project_completed.append(project)

    return render(request, "customdashboard/visual_dashboard.html", {'getSiteProfile':getSiteProfile, 'getBudgetEstimated': getBudgetEstimated, 'getQuantitativeDataSums': getQuantitativeDataSums,
                                                                     'country': countries, 'getAwaitingApprovalCount':getAwaitingApprovalCount,
                                                                     'getFilteredName': getFilteredName,'getProjects': getProjects, 'getApprovedCount': getApprovedCount,
                                                                     'getRejectedCount': getRejectedCount, 'getInProgressCount': getInProgressCount,'nostatus_count': nostatus_count,
                                                                     'getProjectsCount': getProjectsCount, 'selected_countries_list': selected_countries_list,
                                                                     'getSiteProfileIndicator': getSiteProfileIndicator, 'get_project_completed': get_project_completed})


def PublicDashboard(request,id=0):
    program_id = id
    getQuantitativeDataSums_2 = CollectedData.objects.all().filter(indicator__program__id=program_id,achieved__isnull=False).order_by('indicator__source').values('indicator__number','indicator__source','indicator__id')
    getQuantitativeDataSums = CollectedData.objects.all().filter(indicator__program__id=program_id,achieved__isnull=False).exclude(achieved=None,targeted=None).order_by('indicator__number').values('indicator__number','indicator__name','indicator__id').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))
    getIndicatorCount = Indicator.objects.all().filter(program__id=program_id).count()
    getIndicatorCountData = CollectedData.objects.all().filter(indicator__program__id=program_id,achieved__isnull=False).count()
    getIndicatorCountKPI = Indicator.objects.all().filter(program__id=program_id,key_performance_indicator=1).count()
    getProgram = Program.objects.all().get(id=program_id)
    try:
        getProgramNarrative = ProgramNarratives.objects.get(program_id=program_id)
    except ProgramNarratives.DoesNotExist:
        getProgramNarrative = None
    getProjects = ProjectComplete.objects.all().filter(program_id=program_id)
    getSiteProfile = SiteProfile.objects.all().filter(projectagreement__program__id=program_id)
    getSiteProfileIndicator = SiteProfile.objects.all().filter(Q(collecteddata__program__id=program_id))

    getProjectsCount = ProjectAgreement.objects.all().filter(program__id=program_id).count()
    getAwaitingApprovalCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='awaiting approval').count()
    getApprovedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='approved').count()
    getRejectedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='rejected').count()
    getInProgressCount = ProjectAgreement.objects.all().filter(Q(program__id=program_id) & Q(Q(approval='in progress') | Q(approval=None) | Q(approval=""))).count()

    nostatus_count = ProjectAgreement.objects.all().filter(Q(Q(approval=None) | Q(approval=""))).count()

    #get all countires
    countries = Country.objects.all().filter(program__id=program_id)

    #Trainings
    agreement_id_list = []
    training_id_list = []

    for p in getProjects:
        agreement_id_list.append(p.id)

    getTrainings = TrainingAttendance.objects.all().filter(project_agreement_id__in=agreement_id_list)

    getDistributions = Distribution.objects.all().filter(initiation_id__in=agreement_id_list)

    for t in getTrainings:
        training_id_list.append(t.id)

    getBeneficiaries = Beneficiary.objects.all().filter(training__in=training_id_list)

    get_project_completed = []

    getProjectsComplete = ProjectComplete.objects.all()
    for project in getProjects:
        for complete in getProjectsComplete:
            if complete.actual_budget != None:
                if project.id == complete.project_agreement_id:

                    get_project_completed.append(project)

    return render(request, "customdashboard/publicdashboard/public_dashboard.html", {'getProgram':getProgram,'getProjects':getProjects,
                                                                     'getSiteProfile':getSiteProfile,
                                                                     'countries': countries, 'getProgramNarrative': getProgramNarrative,
                                                                     'getAwaitingApprovalCount':getAwaitingApprovalCount,'getQuantitativeDataSums_2':getQuantitativeDataSums_2,
                                                                     'getApprovedCount': getApprovedCount,
                                                                     'getRejectedCount': getRejectedCount,
                                                                     'getInProgressCount': getInProgressCount,'nostatus_count': nostatus_count,
                                                                     'total_projects': getProjectsCount,
                                                                     'getIndicatorCount': getIndicatorCount,
                                                                     'getIndicatorCountData':getIndicatorCountData,
                                                                     'getIndicatorCountKPI': getIndicatorCountKPI,
                                                                     'getQuantitativeDataSums': getQuantitativeDataSums,
                                                                     'getSiteProfileIndicator': getSiteProfileIndicator, 'getSiteProfileIndicatorCount': getSiteProfileIndicator.count(), 'getBeneficiaries': getBeneficiaries, 'getDistributions': getDistributions, 'getTrainings': getTrainings, 'get_project_completed': get_project_completed})


"""
Extremely Customized dashboards
This section contains custom dashboards or one-off dashboard for demo, or specific
customer requests outside the scope of customized program dashboards
"""
def SurveyPublicDashboard(request,id=0):
    """
    DEMO only survey for Tola survey
    :return:
    """

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
    meaning = []
    join = []
    tola_is = []
    for item in data:
        print item['tola_is_a_pashto_word_meaning_']
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

    return render(request, "customdashboard/themes/survey_public_dashboard.html", {'meaning':meaningcount,'join':joincount,'tola_is':tolacount, 'countries': countries, 'dashboard':dashboard})


def SurveyTalkPublicDashboard(request,id=0):
    """
    DEMO only survey for Tola survey for use with public talks about TolaData
    Share URL to survey and data will be aggregated in tolatables
    then imported to this dashboard
    :return:
    """
    # get all countires
    countries = Country.objects.all()

    filter_url = "http://tables.toladata.io/api/silo/9/data/"

    headers = {'content-type': 'application/json',
               'Authorization': 'Token bd43de0c16ac0400bc404c6598a6fe0e4ce73aa2'}

    import ast
    response = requests.get(filter_url, headers=headers, verify=False)
    get_json = json.loads(json.dumps(response.content))
    data = ast.literal_eval(get_json)
    meaning = []
    join = []
    tola_is = []
    country_from = []
    for item in data['data']:
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

    return render(request, "customdashboard/themes/survey_talk_public_dashboard.html", {'meaning':meaningcount,'join':joincount,'tola_is':tolacount, 'country_from': country_from, 'countries': countries, 'dashboard':dashboard})


def ReportPublicDashboard(request,id=0):

    # get all countires
    countries = Country.objects.all()
    report = True

    return render(request, "customdashboard/themes/survey_public_dashboard.html", {'countries': countries, 'report':report})


def RRIMAPublicDashboard(request,id=0):
    """
    RRIMA custom dashboard TODO: Migrate this to the existing configurable dashboard
    :param request:
    :param id:
    :return:
    """
    ## retrieve program
    model = Program
    program_id = id
    getProgram = Program.objects.all().filter(id=program_id)


    ## retrieve the coutries the user has data access for
    countries = getCountry(request.user)

    #retrieve projects for a program
    getProjects = ProjectAgreement.objects.all()##.filter(program__id=1, program__country__in=1)

    pageText = {}
    pageText['pageTitle'] = "Refugee Response and Migration News"
    pageText['projectSummary'] = {}

    pageNews = JupyterNotebooks.objects.all().filter(very_custom_dashboard="RRIMA")

    pageMap = [{"latitude":39.9334, "longitude":32.8597, "location_name":"Ankara","site_contact":"Sonal Shinde, Migration Response Director, sshinde@mercycorps.org", "site_description":"Migration Response Coordination","region_name":"Turkey"},
        {"latitude":38.4237, "longitude":27.1428, "location_name":"Izmir","site_contact":"Tracy Lucas, Emergency Program Manager, ECHO Aegean Response, tlucas@mercycorps.org", "site_description":"Cash, Information Dissemination, Youth, Protection", "region_name":"Turkey"},
        {"latitude":37.0660, "longitude":37.3781, "location_name":"Gaziantep","site_contact":"Jihane Nami, Director of Programs Turkey, jnami@mercycorps.org", "site_description":"Cash, NFI, Shelter, Protection, Information Dissemination","region_name":"Turkey"},
        {"latitude":39.2645, "longitude":26.2777, "location_name":"Lesvos", "site_contact":"Chiara Bogoni, Island Emergency Program Manager, cbogoni@mercycorps.org", "site_description":"Cash, Youth Programs, Food","region_link":"Greece"},
        {"latitude":37.9838, "longitude":23.7275, "location_name":"Athens", "site_contact":"Josh Kreger, Team Leader - Greece, jkreger@mercycorps.org and Kaja Wislinska, Team Leader - Athens and Mainland, kwislinska@mercycorps.org","site_description":"Cash, Youth Psychosocial Support, Legal Support","region_link":"Greece","region_link":"Greece"},
        {"latitude":44.7866, "longitude":20.4489, "location_name":"Belgrade","site_contact":"Radovan Jovanovic, Team Leader - Balkans, rjovanovic@mercycorps.org","site_description":"SIM Card Distribution, Information Dissemination","region_name":"Balkans"}]
   # Borrowed data for bar graph
    colorPalettes = {
    'bright':['#82BC00','#C8C500','#10A400','#CF102E','#DB5E11','#A40D7A','#00AFA8','#1349BB','#FFD200 ','#FF7100','#FFFD00','#ABABAB','#7F7F7F','#7B5213','#C18A34'],
    'light':['#BAEE46','#FDFB4A','#4BCF3D','#F2637A','#FFA268','#C451A4','#4BC3BE','#5B7FCC','#9F54CC','#FFE464','#FFA964','#FFFE64','#D7D7D7','#7F7F7F','#D2A868','#FFD592']
    };

    return render(request, 'customdashboard/rrima_dashboard.html', 
        {'pageText': pageText, 'pageNews': pageNews, 'pageMap': pageMap, 'countries': countries })


def Notebook(request,id=0):
    """
    RRIMA custom dashboard TODO: Migrate this to the existing configurable dashboard
    :param request:
    :param id:
    :return:
    """
    getNotebook = JupyterNotebooks.objects.get(id=id)
    return render(request, "customdashboard/notebook.html", {'getNotebook':getNotebook})


def AnalyticsDashboard(request,id=0):
    """
    RRIMA custom dashboard TODO: Migrate this to the existing configurable dashboard
    :param request:
    :param id:
    :return:
    """
    ## retrieve program
    model = Program
    program_id = id
    getProgram = Program.objects.all().filter(id=program_id)

    ## retrieve the coutries the user has data access for
    countries = getCountry(request.user)

    #retrieve projects for a program
    getProjects = ProjectAgreement.objects.all()##.filter(program__id=1, program__country__in=1)

    ## retrieve data --  this is an example of a tola tables request
    ## TODO: with forms, allow user to select the table that populates related filter_url, right?
    ## TODO: this should allow for up to 3 data sources (one per chart)

    #detailed assessment: https://tola-tables.mercycorps.org/api/silo/1225/data/


    # filter_url = "http://tables.toladata.io/api/silo/9/data/"
    # headers = {'content-type': 'application/json',
    #            'Authorization': 'Token bd43de0c16ac0400bc404c6598a6fe0e4ce73aa2'}
    # response = requests.get(filter_url, headers=headers, verify=False)
    # get_json = json.loads(response.content)
    # data = get_json

    #Parse the JSON(s) into datasets that will feed the templates for this example 
    ## -- parsing might not be immediately relevant for live example 

    # dataset1 = []
    # key1 = 'what_country_were_you_in_last'  
    # for answer in data:
    #     dataset1.append(answer[key1])

    # dataset2 = []
    # key2 = 'tola_is_a_pashto_word_meaning_'  
    # for answer in data:
    #     dataset2.append(answer[key2])

    # dataset3 = []
    # key3 = 'thanks_for_coming_what_made_you_join_us_today_'  
    # for answer in data:
    #     dataset3.append(answer[key3])

    # Programmatically defined table titles  -- 
    # TODO: these should come from a form that allows text entry of what the charts should be called; 
    # form should have char limits on title length
    
    tableHeaders = {}
    tableHeaders['title1']= "Title 1"##key1.title##getProgram[0]
    tableHeaders['title2']= "Title 2"##key2.title
    tableHeaders['title3']= "Title 3"##key3.title
 
    #Programmatically defined data sets -- these should be (1) selected from a drop down.
    # TODO: open question --  how do we define which values in a table's data are going to be used?  
    # and how does that differ based on chart selection?  
    ## bar graph needs table information to resolve to 1-2 sets of numerical values

    tableData = {}
    tableData1= [1000,2000,3000]#dataset1 -- this data is nonumerical so using a hardcoded data set as a placeholder
    
    tableLabels2= ['Approved', 'Waiting', 'Rejected', 'In Progress']
    tableDataset2= [1000,1000,2000,3000]#dataset2

    tableLabels3= ['Eating','Drinking','Sleeping','Designing','Coding','Partying','Running']
    tableDataset3_1= [1,16,7,3,14,55,40]
    tableDataset3_2= [28,48,40,19,96,27,100]            

    table2= {
    "column_heading": "title for placeholder", 
    "labels": tableLabels2, 
    "data_set": tableDataset2, 
    "component_id" : "testBarId",
    "component_id_2" : "testBarId2"
    }#dataset3

    table3= {
    "column_heading": tableHeaders['title3'], 
    "labels": tableLabels3, 
    "first_data_set": tableDataset3_1, 
    "second_data_set": tableDataset3_2
    }#dataset3

    table4= {
    "column_heading": "title for placeholder", 
    "labels": tableLabels2, 
    "data_set": tableDataset2, 
    "component_id" : "testBarId2",
    }#dataset3

    colorPalettes = {
    'bright':['#82BC00','#C8C500','#10A400','#CF102E','#DB5E11','#A40D7A','#00AFA8','#1349BB','#FFD200 ','#FF7100','#FFFD00','#ABABAB','#7F7F7F','#7B5213','#C18A34'],
    'light':['#BAEE46','#FDFB4A','#4BCF3D','#F2637A','#FFA268','#C451A4','#4BC3BE','#5B7FCC','#9F54CC','#FFE464','#FFA964','#FFFE64','#D7D7D7','#7F7F7F','#D2A868','#FFD592']
    };
    
    return render(request, 'customdashboard/themes/analytics_dashboard.html', 
        {'colorPalettes': colorPalettes, 'tableData1': tableData1,'table4': table4,'table2': table2,'table3': table3,'tableHeaders': tableHeaders,'getProgram': getProgram, 'countries': countries, 'getProjects': getProjects})

def NewsDashboard(request,id=0):
    """
    RRIMA custom dashboard TODO: Migrate this to the existing configurable dashboard
    :param request:
    :param id:
    :return:
    """
    ## retrieve program
    model = Program
    program_id = id
    getProgram = Program.objects.all().filter(id=program_id)

    ## retrieve the coutries the user has data access for
    countries = getCountry(request.user)

    #retrieve projects for a program
    getProjects = ProjectAgreement.objects.all()##.filter(program__id=1, program__country__in=1)

    ## retrieve data --  this is an example of a tola tables request
    ## TODO: with forms, allow user to select the table that populates related filter_url, right?
    ## TODO: this should allow for up to 3 data sources (one per chart)

    #detailed assessment: https://tola-tables.mercycorps.org/api/silo/1225/data/


    # filter_url = "http://tables.toladata.io/api/silo/9/data/"
    # headers = {'content-type': 'application/json',
    #            'Authorization': 'Token bd43de0c16ac0400bc404c6598a6fe0e4ce73aa2'}
    # response = requests.get(filter_url, headers=headers, verify=False)
    # get_json = json.loads(response.content)
    # data = get_json

    #Parse the JSON(s) into datasets that will feed the templates for this example 
    ## -- parsing might not be immediately relevant for live example 

    # dataset1 = []
    # key1 = 'what_country_were_you_in_last'  
    # for answer in data:
    #     dataset1.append(answer[key1])

    # dataset2 = []
    # key2 = 'tola_is_a_pashto_word_meaning_'  
    # for answer in data:
    #     dataset2.append(answer[key2])

    # dataset3 = []
    # key3 = 'thanks_for_coming_what_made_you_join_us_today_'  
    # for answer in data:
    #     dataset3.append(answer[key3])

    # Programmatically defined table titles  -- 
    # TODO: these should come from a form that allows text entry of what the charts should be called; 
    # form should have char limits on title length
    
 
 
    #Programmatically defined data sets -- these should be (1) selected from a drop down.
    # TODO: open question --  how do we define which values in a table's data are going to be used?  
    # and how does that differ based on chart selection?  
    ## bar graph needs table information to resolve to 1-2 sets of numerical values

      
    pageNewsFeedOne = [
    {"date":"", "short_description":"text","link":"", "location": "[EU,Greece,US,etc.]"},
    {"date":"", "short_description":"text","link":"", "location": "[EU,Greece,US,etc.]"}
    ]

    pageText = {}
    pageText['pageTitle'] = "Refugee Response and Migration News"
    pageText['objectives'] = ["General", "Push/Pull", "Youth","Education", "Legal", "Health"]
    pageText['objectives_subtitles'] = ["General", "Push/Pull", "Youth","Education", "Legal", "Health"]
    pageText['projectSummary'] = {
        'title':"Project Description", 
        'excerpt': "The Refugee Response Information Management & Analysis Platform (RRIMA) is an interactive dashboarding tool that will allow Mercy Corps teams across the Aegean Response to feed their program data into a single platform, providing the ability to view trends and changes across multiple different programs and countries, making decisionmaking and rapid, adaptive management of programs more accurate, targeted and forward-thinking.",
        'full':["Formatted text"]
    }

    colorPalettes = {
    'bright':['#82BC00','#C8C500','#10A400','#CF102E','#DB5E11','#A40D7A','#00AFA8','#1349BB','#FFD200 ','#FF7100','#FFFD00','#ABABAB','#7F7F7F','#7B5213','#C18A34'],
    'light':['#BAEE46','#FDFB4A','#4BCF3D','#F2637A','#FFA268','#C451A4','#4BC3BE','#5B7FCC','#9F54CC','#FFE464','#FFA964','#FFFE64','#D7D7D7','#7F7F7F','#D2A868','#FFD592']
    };
    
    return render(request, 'customdashboard/themes/news_dashboard.html',
        {'colorPalettes': colorPalettes, 'pageNewsFeedOne': pageNewsFeedOne, 'pageText': pageText, 'getProgram': getProgram, 'countries': countries, 'getProjects': getProjects})


def NarrativeDashboard(request,id=0):
    """
    RRIMA custom dashboard TODO: Migrate this to the existing configurable dashboard
    :param request:
    :param id:
    :return:
    """
    ## retrieve program
    model = Program
    program_id = id
    getProgram = Program.objects.all().filter(id=program_id)

    ## retrieve the coutries the user has data access for
    countries = getCountry(request.user)

    #retrieve projects for a program
    getProjects = ProjectAgreement.objects.all()##.filter(program__id=1, program__country__in=1)


    pageText = {}
    pageText['pageTitle'] = "Refugee Response Information Management & Analysis (RRIMA)"
    pageText['objectives'] = ["Rapid Use Interface", "Data Analysis"]
    pageText['objectives_subtitles'] = ["Rapid Implementation; Nimble and Accessible User Interface","Data Analysis and Dissemination"]
    pageText['objectives_content'] = ["RRIMA will be a user-friendly dashboarding/data visualization tool that is quick to implement and requires little technical knowledge to use. ", "RRIMA will promote increased transparency and communications across teams, partners and external audiences.\n\nRRIMA will support teams' ability to articulate impact and trends across the whole Aegean Response."]
    pageText['projectSummary'] = {
        'title':"Project Description", 
        'excerpt': "The Refugee Response Information Management & Analysis Platform (RRIMA) is an interactive dashboarding tool that will allow Mercy Corps teams across the Aegean Response to feed their program data into a single platform, providing the ability to view trends and changes across multiple different programs and countries, making decisionmaking and rapid, adaptive management of programs more accurate, targeted and forward-thinking.",
        'full':[
            "In recent years, we have seen a phenomena of migration taking place originating from geographic areas spanning across North and East Africa, the Middle East and Central Asia flowing into and towards Europe.",
            "More than a million migrants and refugees crossed into Europe in 2015 - the vast majority of which traveled along the Aegean route from countries such as Syria, Afghanistan and Iraq through Turkey, Greece and the Balkans into Europe, seeking asylum. Approximately 74 percent of those are from the top 10 refugee-producing countries (including Syria, Afghanistan, and Iraq among others) and are likely meet the criteria for protected status under the 1951 Refugee Convention. The remaining 26 percent are migrants who are seeking safety, resources and/or a better life in Europe.", 
            "Mercy Corps is poised with field teams in active areas along the migration route, including the Turkey, Greece, Serbia and the Former Republic of Macedonia (FYROM). However, despite the fact that teams are gathering similar information and running parallel programming, communication and information flow is limited due to a lack of a unifying framework for analysis.", 
            "With ECHO funding, we have the opportunity to change that. ", 
            "The Refugee Response Information Management & Analysis Platform (RRIMA) is an interactive dashboarding tool that will allow Mercy Corps teams across the Aegean Response to feed their program data into a single platform, providing the ability to view trends and changes across multiple different programs and countries, making decisionmaking and rapid, adaptive management of programs more accurate, targeted and forward-thinking.", 
            "Working side by side with the Tola team and utilizing TolaData as the primary platform for data and information merging and management, the RRIMA and Tola partnership aims to:"], 
            'highlightList':["Centralize existing data sources.", "Identify trends within a given context.", "Analyze real-time data sets.", "Inform adaptive program delivery.", "Promote data sharing and learning."]   
    }
    pageText['timelineLinks'] = [{"date": "August 4-5","event": "Kick-Off Meeting (Izmir)","link": ""},{"date": "Aug 28 - Sept 9","event": "RRIMA Team in Izmir","link": ""},{"date": "October","event": "Prototype Presentation to ECHO","link": ""},{"date": "October - December","event": "Project Conclusion","link": ""}, {"date": "December","event": "Project Conclusion","link": ""}]

    pageImages = {}
    pageImages['leadimage_sourcelink'] = 'drive.google.com/a/mercycorps.org/file/d/0B8g-VJ-NXXHiMng0OVVla3FEMlE/view?usp=sharing'
    pageImages['title'] = 'Aegean Response Photos'
    pageImages['imageset'] = ["img/demo_images/image1.jpg","img/demo_images/image2.jpg","img/demo_images/image3.jpg","img/demo_images/image4.jpg","img/demo_images/image5.jpg","img/demo_images/image6.jpg","img/demo_images/image7.jpg","img/demo_images/image8.jpg"]

    pageNews = [{"link":"(?P<id>[0-9]+)/jupyter/1/", "title": "RRIMA Report, Vol. 1"},
        {"link":"(?P<id>[0-9]+)/jupyter/2/", "title": "RRIMA Report, Vol. 2"},
        {"link":"(?P<id>[0-9]+)/jupyter/3/", "title": "RRIMA Report, Vol. 3"},
        {"link":"(?P<id>[0-9]+)/jupyter/4/", "title": "RRIMA Report, Vol. 4"},
        {"link":"(?P<id>[0-9]+)/jupyter/5/", "title": "RRIMA Report, Vol. 5"},
        {"link":"(?P<id>[0-9]+)/jupyter/6/", "title": "RRIMA Report, Vol. 6"}]

    pageMap = [{"latitude":38.4237, "longitude":27.1428, "location_name":"Izmir","site_contact":"", "site_description":"Information we want to display", "region_name":"Turkey"},
        {"latitude":37.0660, "longitude":37.3781, "location_name":"Gaziantep","site_contact":"", "site_description":"Information we want to display","region_name":"Turkey"},
        {"latitude":39.2645, "longitude":26.2777, "location_name":"Lesvos", "site_contact":"Josh Kreger", "site_description":"Cash, NFIs, Information Dissemination, Wifi Hotspots, SIM Distribution, Shelter, Advocacy","region_link":"Greece"},
        {"latitude":37.1409, "longitude":26.8488, "location_name":"Leros", "site_contact":"Hicham Awad","site_description":"Cash, NFIs, Information Dissemination, Wifi Hotspots, SIM Distribution, Shelter, Advocacy","region_link":"Greece","region_link":"Greece"},
        {"latitude":36.8915, "longitude":27.2877, "location_name":"Kos", "site_contact":"Josh Kreger","site_description":"Cash, NFIs, Information Dissemination, Wifi Hotspots, SIM Distribution, Shelter, Advocacy","region_link":"Greece","region_link":"Greece"},
        {"latitude":37.9838, "longitude":23.7275, "location_name":"Athens", "site_contact":"Kaja Wislinska","site_description":"Cash, NFIs, Information Dissemination, Wifi Hotspots, SIM Distribution, Shelter, Advocacy","region_link":"Greece","region_link":"Greece"},
        {"latitude":41.1452, "longitude":22.4997, "location_name":"Gevgelija", "site_contact":"test","site_description":"Information we want to display","region_name":"Balkans"},
        {"latitude":42.2130, "longitude":21.7108, "location_name":"Tabanovce","site_contact":"test","site_description":"Information we want to display","region_name":"Balkans"},
        {"latitude":42.3092, "longitude": 21.6499, "location_name":"Presevo","site_contact":"test","site_description":"Information we want to display","region_name":"Balkans"},
        {"latitude":44.8416, "longitude":20.4958, "location_name":"Krnjaca","site_contact":"test","site_description":"Information we want to display","region_name":"Balkans"},
        {"latitude":45.1258, "longitude":19.2283, "location_name":"Sid","site_contact":"test","site_description":"Information we want to display","region_name":"Balkans"},
        {"latitude":46.1005, "longitude":19.6651, "location_name":"Subotica","site_contact":"test","site_description":"Information we want to display","region_name":"Balkans"}]
   # Borrowed data for bar graph
    colorPalettes = {
    'bright':['#82BC00','#C8C500','#10A400','#CF102E','#DB5E11','#A40D7A','#00AFA8','#1349BB','#FFD200 ','#FF7100','#FFFD00','#ABABAB','#7F7F7F','#7B5213','#C18A34'],
    'light':['#BAEE46','#FDFB4A','#4BCF3D','#F2637A','#FFA268','#C451A4','#4BC3BE','#5B7FCC','#9F54CC','#FFE464','#FFA964','#FFFE64','#D7D7D7','#7F7F7F','#D2A868','#FFD592']
    };

    return render(request, 'customdashboard/themes/rrima_narrative_dashboard.html', 
        {'pageText': pageText, 'pageNews': pageNews, 'pageImages': pageImages, 'pageMap': pageMap,'getProgram': getProgram, 'countries': countries, 'getProjects': getProjects}) #add data 


def MapDashboard(request,id=0):
    """
    RRIMA custom dashboard TODO: Migrate this to the existing configurable dashboard
    :param request:
    :param id:
    :return:
    """
    ## retrieve program
    model = Program
    program_id = id
    getProgram = Program.objects.all().filter(id=program_id)

    ## retrieve the coutries the user has data access for
    countries = getCountry(request.user)

    #retrieve projects for a program
    getProjects = ProjectAgreement.objects.all()##.filter(program__id=1, program__country__in=1)

    #example request
    # filter_url = "http://tables.toladata.io/api/silo/9/data/"
    # headers = {'content-type': 'application/json',
    #            'Authorization': 'Token bd43de0c16ac0400bc404c6598a6fe0e4ce73aa2'}
    # response = requests.get(filter_url, headers=headers, verify=False)
    # get_json = json.loads(response.content)
    # data = get_json


    #Parse the JSON(s) into datasets that will feed the templates for this example 
    ## -- parsing might not be immediately relevant for live example 

    #Programmatically defined table titles  -- 
    ## TODO: these should come from a form that allows text entry of what the charts should be called; 
    # form should have char limits on title length
    colorPalettes = {
    'bright':['#82BC00','#C8C500','#10A400','#CF102E','#DB5E11','#A40D7A','#00AFA8','#1349BB','#FFD200','#FF7100','#FFFD00','#ABABAB','#7F7F7F','#7B5213','#C18A34'],
    'bright1':['#82BC00','#C8C500','#1349BB','#10A400','#CF102E','#FF7100','#A40D7A','#00AFA8'],
    'bright2':['#82BC00','#C8C500 ','#10A400','#CF102E','#FF7100','#A40D7A','#00AFA8'],
    'bright3':['#82BC00','#C18A34','#CF102E','#A40D7A','#00AFA8'],
    'light':['#BAEE46','#FDFB4A','#4BCF3D','#F2637A','#FFA268','#C451A4','#4BC3BE','#5B7FCC','#9F54CC','#FFE464','#FFA964','#FFFE64','#D7D7D7','#7F7F7F','#D2A868','#FFD592']
    };

    tableData = {}
 
    tableLabels1= ['afghanistan','algeria','egypt','iran','iraq','pakistan','syria','other']
    tableDataset1= [63,1,1,5,81,4,515,31]#dataset2          

    tableLabels2= ['afghanistan','algeria','iran','iraq','pakistan','syria','other']
    tableDataset2= [22,1,4,52,4,242,31]#dataset2  

    tableLabels3= ['afghanistan','egypt','iraq','syria']
    tableDataset3= [30,1,1,122]#dataset2  

    table1= {
    "column_heading": "All Greece: Countries of Origin", 
    "labels": tableLabels1, 
    "data_set": tableDataset1, 
    "component_id" : "testBarId",
    "colors": colorPalettes['bright1'],
    }

    table2= {
    "column_heading": "Lesvos, Greece: Countries of Origin", 
    "labels": tableLabels2, 
    "data_set": tableDataset2, 
    "component_id" : "testBarId2",
    "colors": colorPalettes['bright2'],
    }

    table3= {
    "column_heading": "Filippiada, Greece: Countries of Origin", 
    "labels": tableLabels3, 
    "data_set": tableDataset3, 
    "component_id" : "testBarId3",
    "colors": colorPalettes['bright3'],
    }

    pageMap = []
    pageMap = [{"latitude":39.2645, "longitude":26.2777, "location_name":"Lesvos", "site_contact":"Josh Kreger", "site_description":"Cash, NFIs, Information Dissemination, Wifi Hotspots, SIM Distribution, Shelter, Advocacy","region_link":"Greece"},
        {"latitude":37.1409, "longitude":26.8488, "location_name":"Leros", "site_contact":"Hicham Awad","site_description":"Cash, NFIs, Information Dissemination, Wifi Hotspots, SIM Distribution, Shelter, Advocacy","region_link":"Greece","region_link":"Greece"},
        {"latitude":36.8915, "longitude":27.2877, "location_name":"Kos", "site_contact":"Josh Kreger","site_description":"Cash, NFIs, Information Dissemination, Wifi Hotspots, SIM Distribution, Shelter, Advocacy","region_link":"Greece","region_link":"Greece"},
        {"latitude":37.9838, "longitude":23.7275, "location_name":"Athens", "site_contact":"Kaja Wislinska","site_description":"Cash, NFIs, Information Dissemination, Wifi Hotspots, SIM Distribution, Shelter, Advocacy","region_link":"Greece","region_link":"Greece"}]


    return render(request, 'customdashboard/themes/map_dashboard.html', 
        {'pageMap':pageMap,'colorPalettes':colorPalettes,'table1': table1,'table2': table2,'table3': table3,'getProgram': getProgram, 'countries': countries, 'getProjects': getProjects}) 


def RRIMAJupyterView1(request,id=0):
    """
    RRIMA custom dashboard TODO: Migrate this to the existing configurable dashboard
    :param request:
    :param id:
    :return:
    """
    model = Program
    program_id = 1#id ##USE TURKEY PROGRAM ID HERE
    # getProgram = Program.objects.all().filter(id=program_id)

    ## retrieve the coutries the user has data access for
    countries = getCountry(request.user)
    with open('static/rrima.html') as myfile: data = "\n".join(line for line in myfile) 
    
    return HttpResponse(data)