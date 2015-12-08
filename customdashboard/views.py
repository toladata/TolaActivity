from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from activitydb.models import ProjectAgreement, CustomDashboard ,ProjectComplete, Program, SiteProfile, Sector,Country as ActivityCountry, Feedback, FAQ, DocumentationApp
from .models import ProjectStatus
from indicators.models import CollectedData
from djangocosign.models import UserProfile
from djangocosign.models import Country

from util import getCountry
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models import Q

from tola.util import getCountry

from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')

def DefaultCustomDashboard(request,id=0,sector=0,status=0):
    """
    # of agreements, approved, rejected, waiting, archived and total for dashboard
    """
    program_id = id

    countries = getCountry(request.user)
    getQuantitativeDataSums = CollectedData.objects.all().filter(indicator__program__id=program_id,achieved__isnull=False).exclude(achieved=None,targeted=None).order_by('indicator__number').values('indicator__number','indicator__name','indicator__id').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))
    getFilteredName=Program.objects.get(id=program_id)
    getProjectStatus = ProjectStatus.objects.all()

    getProjectsCount = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries).count()
    getBudgetEstimated = ProjectAgreement.objects.all().filter(program__id=program_id, program__country__in=countries).annotate(estimated=Sum('total_estimated_budget'))
    getAwaitingApprovalCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='awaiting approval', program__country__in=countries).count()
    getApprovedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='approved', program__country__in=countries).count()
    getRejectedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='rejected', program__country__in=countries).count()
    getInProgressCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='in progress', program__country__in=countries).count()

    getSiteProfile = SiteProfile.objects.all().filter(projectagreement__program__id=program_id, projectagreement__sector__id=sector)



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
                                                                     'getCustomDashboard': getCustomDashboard, 'getProjectsCount': getProjectsCount})