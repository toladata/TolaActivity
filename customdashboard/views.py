from django.views.generic.list import ListView

from django.shortcuts import render
from activitydb.models import ProjectAgreement, ProjectComplete, CustomDashboard, Program, SiteProfile,Country, TolaSites
from customdashboard.models import OverlayGroups, OverlayNarratives, JupyterNotebooks
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
    getAwaitingApprovalCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='awaiting approval', program__country__in=countries).count()
    getApprovedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='approved', program__country__in=countries).count()
    getRejectedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='rejected', program__country__in=countries).count()
    getInProgressCount = ProjectAgreement.objects.all().filter(Q(Q(approval='in progress') | Q(approval="") | Q(approval=None)),program__id=program_id, program__country__in=countries).count()

    getSiteProfile = SiteProfile.objects.all().filter(Q(projectagreement__program__id=program_id) | Q(collecteddata__program__id=program_id))
    getSiteProfileIndicator = SiteProfile.objects.all().filter(Q(collecteddata__program__id=program_id))

    if (status) =='Approved':
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries, approval='approved')
    elif(status) =='Rejected':
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries, approval='rejected')
    elif(status) =='In Progress':
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries, approval='in progress')
    elif(status) =='Awaiting Approval':
       getProjects = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries, approval='awaiting approval')
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

def RRIMAPublicDashboard(request,id=0):

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
    pageText['timelineLinks'] = [{"date": "August 4-5","event": "Kick-Off Meeting (Izmir)","link": "https://docs.google.com/document/d/1luuWETSpsZcyRR_pOoZYxF-2P1KripTWLfGCBaXP2Z4/edit"},
    {"date": "Aug 28 - Sept 9","event": "RRIMA Team in Izmir","link": ""},
    {"date": "October","event": "Prototype Presentation to ECHO","link": ""},
    {"date": "October - December","event": "RRIMA Reports Released; Testing of Data Visualization Prototype","link": ""}, 
    {"date": "December","event": "Project Conclusion","link": ""}]

    pageImages = {}
    pageImages['leadimage_sourcelink'] = 'drive.google.com/a/mercycorps.org/file/d/0B8g-VJ-NXXHiMng0OVVla3FEMlE/view?usp=sharing'
    pageImages['title'] = 'Aegean Response Photos'
    pageImages['imageset'] = ["img/rrima_images/image1.jpg","img/rrima_images/image2.jpg","img/rrima_images/image3.jpg","img/rrima_images/image4.jpg","img/rrima_images/image5.jpg","img/rrima_images/image6.jpg","img/rrima_images/image7.jpg","img/rrima_images/image8.jpg"]

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
        {'pageText': pageText, 'pageNews': pageNews, 'pageImages': pageImages, 'pageMap': pageMap,'getProgram': getProgram, 'countries': countries, 'getProjects': getProjects}) #add data 



def Gallery(request,id=0):
    program_id = id
    getProgram = Program.objects.all().filter(id=program_id)
    getGallery = Gallery.objects.all().filter(program_name__id=program_id)
    return render(request, "gallery/gallery.html", {'getGallery':getGallery, 'getProgram':getProgram})


def Notebook(request,id=0):
    getNotebook = JupyterNotebooks.objects.get(id=id)
    return render(request, "customdashboard/notebook.html", {'getNotebook':getNotebook})


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

