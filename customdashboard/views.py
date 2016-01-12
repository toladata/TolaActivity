from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView

from django.shortcuts import render
from django.contrib import auth
from activitydb.models import ProjectAgreement, CustomDashboard ,ProjectComplete, Program, SiteProfile, Sector,Country as ActivityCountry, Feedback, FAQ, DocumentationApp
from .models import ProjectStatus, Gallery
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
    getAwaitingApprovalCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='', program__country__in=countries).count()
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



def PublicDashboard(request,id=0):
    program_id = id
    getQuantitativeDataSums_2 = CollectedData.objects.all().filter(indicator__program__id=program_id,achieved__isnull=False).order_by('indicator__source').values('indicator__number','indicator__source','indicator__id')
    getQuantitativeDataSums = CollectedData.objects.all().filter(indicator__program__id=program_id,achieved__isnull=False).exclude(achieved=None,targeted=None).order_by('indicator__number').values('indicator__number','indicator__name','indicator__id').annotate(targets=Sum('targeted'), actuals=Sum('achieved'))
    getProgram = Program.objects.all().get(id=program_id)
    getProjects = ProjectAgreement.objects.all().filter(program_id=program_id)
    getSiteProfile = SiteProfile.objects.all().filter(projectagreement__program__id=program_id)

    getProjectsCount = ProjectAgreement.objects.all().filter(program__id=program_id).count()
    getAwaitingApprovalCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='awaiting approval').count()
    getApprovedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='approved').count()
    getRejectedCount = ProjectAgreement.objects.all().filter(program__id=program_id, approval='rejected').count()
    getInProgressCount = ProjectAgreement.objects.all().filter(Q(program__id=program_id) & Q(Q(approval='in progress') | Q(approval=None) | Q(approval=""))).count()

    #get all countires
    countires = ActivityCountry.objects.all()

    return render(request, "publicdashboard/public_dashboard.html", {'getProgram':getProgram,'getProjects':getProjects,
                                                                     'getSiteProfile':getSiteProfile,
                                                                     'countries': countires,
                                                                     'awaiting':getAwaitingApprovalCount,'getQuantitativeDataSums_2':getQuantitativeDataSums_2,
                                                                     'approved': getApprovedCount,
                                                                     'rejected': getRejectedCount,
                                                                     'in_progress': getInProgressCount,
                                                                     'total_projects': getProjectsCount,
                                                                     'getQuantitativeDataSums': getQuantitativeDataSums})


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

