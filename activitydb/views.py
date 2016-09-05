from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Program, Country, Province, AdminLevelThree, District, ProjectAgreement, ProjectComplete, SiteProfile, \
    Documentation, Monitor, Benchmarks, TrainingAttendance, Beneficiary, Distribution, Budget, ApprovalAuthority, Checklist, ChecklistItem, \
    Stakeholder, Contact, FormGuidance, CustomDashboard, DashboardComponent, ComponentDataSource, DashboardTheme
from indicators.models import CollectedData, ExternalService
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone

import pytz

from .forms import ProjectAgreementForm, ProjectAgreementSimpleForm, ProjectAgreementCreateForm, ProjectCompleteForm, ProjectCompleteSimpleForm, ProjectCompleteCreateForm, DocumentationForm, \
    SiteProfileForm, MonitorForm, BenchmarkForm, TrainingAttendanceForm, BeneficiaryForm, DistributionForm, BudgetForm, FilterForm, \
    QuantitativeOutputsForm, ChecklistItemForm, StakeholderForm, ContactForm, CustomDashboardCreateForm, CustomDashboardForm, CustomDashboardModalForm, \
    CustomDashboardMapForm, DashboardThemeCreateForm, DashboardThemeForm, DashboardComponentCreateForm, DashboardComponentForm, ComponentDataSourceForm, \
    ComponentDataSourceCreateForm
import pytz
import logging
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q
from tables import ProjectAgreementTable
from django_tables2 import RequestConfig
from filters import ProjectAgreementFilter
import json
import ast
import requests
import urllib
import logging

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.sites.shortcuts import get_current_site

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from tola.util import getCountry, emailGroup
from mixins import AjaxableResponseMixin
from export import ProjectAgreementResource
from django.core.exceptions import PermissionDenied

APPROVALS = (
    ('in_progress', 'in progress'),
    ('awaiting_approval', 'awaiting approval'),
    ('approved', 'approved'),
    ('rejected', 'rejected'),
)

from datetime import datetime
from dateutil.relativedelta import relativedelta


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def group_required(*group_names, **url):
    # Requires user membership in at least one of the groups passed in.
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
            raise PermissionDenied
        return False
    return user_passes_test(in_groups)


def group_excluded(*group_names, **url):
    # If user is in the group passed in permission denied
    def in_groups(u):
        if u.is_authenticated():
            if not bool(u.groups.filter(name__in=group_names)):
                return True
            raise PermissionDenied
        return False

    return user_passes_test(in_groups)


class ProjectDash(ListView):

    template_name = 'activitydb/projectdashboard_list.html'

    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
        project_id = int(self.kwargs['pk'])

        if project_id == 0:
            getAgreement = None
            getComplete = None
            getChecklist = None
            getDocumentCount = 0
            getCommunityCount = 0
            getTrainingCount = 0
            getDistributionCount = 0
            getChecklistCount = 0
        else:
            getAgreement = ProjectAgreement.objects.get(id=project_id)
            try:
                getComplete = ProjectComplete.objects.get(project_agreement__id=self.kwargs['pk'])
            except ProjectComplete.DoesNotExist:
                getComplete = None
            getDocumentCount = Documentation.objects.all().filter(project_id=self.kwargs['pk']).count()
            getCommunityCount = SiteProfile.objects.all().filter(projectagreement__id=self.kwargs['pk']).count()
            getTrainingCount = TrainingAttendance.objects.all().filter(project_agreement_id=self.kwargs['pk']).count()
            getDistributionCount = Distribution.objects.all().filter(initiation_id=self.kwargs['pk']).count()
            getChecklistCount = ChecklistItem.objects.all().filter(checklist__agreement_id=self.kwargs['pk']).count()
            getChecklist = ChecklistItem.objects.all().filter(checklist__agreement_id=self.kwargs['pk'])

        if int(self.kwargs['pk']) == 0:
            getProgram =Program.objects.all().filter(funding_status="Funded", country__in=countries).distinct()
        else:
            getProgram =Program.objects.get(agreement__id=self.kwargs['pk'])

        return render(request, self.template_name, {'getProgram': getProgram, 'getAgreement': getAgreement,'getComplete': getComplete,
                                                    'getPrograms':getPrograms, 'getDocumentCount':getDocumentCount,'getChecklistCount': getChecklistCount,
                                                    'getCommunityCount':getCommunityCount, 'getTrainingCount':getTrainingCount, 'project_id': project_id,
                                                    'getChecklist': getChecklist, 'getDistributionCount': getDistributionCount})


class ProgramDash(ListView):
    """
    Dashboard links for and status for each program with number of projects
    :param request:
    :param pk: program_id
    :param status: approval status of project
    :return:
    """
    template_name = 'activitydb/programdashboard_list.html'

    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries).distinct()

        if int(self.kwargs['pk']) == 0:
            getDashboard = Program.objects.all().prefetch_related('agreement','agreement__projectcomplete','agreement__office').filter(funding_status="Funded", country__in=countries).order_by('name').annotate(has_agreement=Count('agreement'),has_complete=Count('complete'))
        else:
            getDashboard = Program.objects.all().prefetch_related('agreement','agreement__projectcomplete','agreement__office').filter(id=self.kwargs['pk'], funding_status="Funded", country__in=countries).order_by('name')

        if self.kwargs.get('status', None):
            status = self.kwargs['status']
            if status == "in progress":
                getDashboard.filter(Q(agreement__approval=self.kwargs['status']) | Q(agreement__approval=None))
            else:
                getDashboard.filter(agreement__approval=self.kwargs['status'])
        else:
            status = None

        return render(request, self.template_name, {'getDashboard': getDashboard, 'getPrograms': getPrograms, 'APPROVALS': APPROVALS, 'program_id':  self.kwargs['pk'], 'status': status})


class ProjectAgreementList(ListView):
    """
    Project Agreement
    :param request:
    """
    model = ProjectAgreement
    template_name = 'activitydb/projectagreement_list.html'

    def get(self, request, *args, **kwargs):
        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries).distinct()

        if int(self.kwargs['pk']) == 0:
            getDashboard = ProjectAgreement.objects.all().filter(program__country__in=countries)
            return render(request, self.template_name, {'form': form, 'getDashboard':getDashboard,'getPrograms':getPrograms})
        else:
            getDashboard = ProjectAgreement.objects.all().filter(program__id=self.kwargs['pk'])
            getProgram =Program.objects.get(id=self.kwargs['pk'])

            return render(request, self.template_name, {'form': form, 'getProgram': getProgram, 'getDashboard':getDashboard,'getPrograms':getPrograms})


class ProjectAgreementImport(ListView):
    """
    Import a project agreement from TolaData or other third party service
    """

    template_name = 'activitydb/projectagreement_import.html'

    def get(self, request, *args, **kwargs):
        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
        getServices = ExternalService.objects.all()
        getCountries = Country.objects.all().filter(country__in=countries)

        return render(request, self.template_name, {'getPrograms': getPrograms, 'getServices': getServices , 'getCountries': getCountries})


class ProjectAgreementCreate(CreateView):
    """
    Project Agreement Form
    :param request:
    :param id:
    This is only used in case of an error incomplete form submission from the simple form
    in the project dashboard
    """

    model = ProjectAgreement
    template_name = 'activitydb/projectagreement_form.html'

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Agreement")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(ProjectAgreementCreate, self).dispatch(request, *args, **kwargs)

     # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProjectAgreementCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    #get shared data from project agreement and pre-populate form with it
    def get_initial(self):

        initial = {
            'approved_by': self.request.user,
            'estimated_by': self.request.user,
            'checked_by': self.request.user,
            'reviewed_by': self.request.user,
            'approval_submitted_by': self.request.user,
            }

        return initial

    def get_context_data(self, **kwargs):
        context = super(ProjectAgreementCreate, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        #save formset from context
        context = self.get_context_data()

        latest = ProjectAgreement.objects.latest('id')
        getAgreement = ProjectAgreement.objects.get(id=latest.id)

        #create a new dashbaord entry for the project
        getProgram = Program.objects.get(id=latest.program_id)

        create_checklist = Checklist(agreement=getAgreement)
        create_checklist.save()

        get_checklist = Checklist.objects.get(id=create_checklist.id)
        get_globals = ChecklistItem.objects.all().filter(global_item=True)
        for item in get_globals:
            ChecklistItem.objects.create(checklist=get_checklist,item=item.item)


        messages.success(self.request, 'Success, Initiation Created!')

        redirect_url = '/activitydb/dashboard/project/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = ProjectAgreementCreateForm


class ProjectAgreementUpdate(UpdateView):
    """
    Project Initiation Form
    :param request:
    :param id: project_agreement_id
    """
    model = ProjectAgreement
    form_class = ProjectAgreementForm

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Agreement")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(ProjectAgreementUpdate, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        check_form_type = ProjectAgreement.objects.get(id=self.kwargs['pk'])

        if check_form_type.short == True:
            form = ProjectAgreementSimpleForm
        else:
            form = ProjectAgreementForm

        return form(**self.get_form_kwargs())


    def get_context_data(self, **kwargs):
        context = super(ProjectAgreementUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context.update({'pk': pk})
        context.update({'program': pk})

        try:
            getQuantitative = CollectedData.objects.all().filter(agreement__id=self.kwargs['pk']).order_by('indicator')
        except CollectedData.DoesNotExist:
            getQuantitative = None
        context.update({'getQuantitative': getQuantitative})

        try:
            getMonitor = Monitor.objects.all().filter(agreement__id=self.kwargs['pk']).order_by('type')
        except Monitor.DoesNotExist:
            getMonitor = None
        context.update({'getMonitor': getMonitor})

        try:
            getBenchmark = Benchmarks.objects.all().filter(agreement__id=self.kwargs['pk']).order_by('description')
        except Benchmarks.DoesNotExist:
            getBenchmark = None
        context.update({'getBenchmark': getBenchmark})

        try:
            getBudget = Budget.objects.all().filter(agreement__id=self.kwargs['pk']).order_by('description_of_contribution')
        except Budget.DoesNotExist:
            getBudget = None
        context.update({'getBudget': getBudget})

        try:
            getDocuments = Documentation.objects.all().filter(project__id=self.kwargs['pk']).order_by('name')
        except Documentation.DoesNotExist:
            getDocuments = None
        context.update({'getDocuments': getDocuments})

        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProjectAgreementUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        #get the approval status of the form before it was submitted and set vars for use in condtions
        check_agreement_status = ProjectAgreement.objects.get(id=str(self.kwargs['pk']))
        is_approved = str(form.instance.approval)
        getProgram = Program.objects.get(agreement__id=check_agreement_status.id)
        country = getProgram.country

        #convert form field unicode project name to ascii safe string for email content
        import unicodedata
        project_name = unicodedata.normalize('NFKD', form.instance.project_name).encode('ascii','ignore')
        #check to see if the approval status has changed
        if str(is_approved) == "approved" and check_agreement_status.approval != "approved":
            budget = form.instance.total_estimated_budget
            if getProgram.budget_check == True:
                try:
                    user_budget_approval = ApprovalAuthority.objects.get(approval_user__user=self.request.user)
                except ApprovalAuthority.DoesNotExist:
                    user_budget_approval = None
            #compare budget amount to users approval amounts

            if getProgram.budget_check:
                if not user_budget_approval or int(budget) > int(user_budget_approval.budget_limit):
                    messages.success(self.request, 'You do not appear to have permissions to approve this initiation')
                    form.instance.approval = 'awaiting approval'
                else:
                    messages.success(self.request, 'Success, Initiation and Budget Approved')
                    form.instance.approval = 'approved'
            else:
                messages.success(self.request, 'Success, Initiation Approved')
                form.instance.approval = 'approved'

            if form.instance.approval == 'approved':
                #email the approver group so they know this was approved
                link = "Link: " + "https://" + get_current_site(self.request).name + "/activitydb/projectagreement_update/" + str(self.kwargs['pk']) + "/"
                subject = "Project Initiation Approved: " + project_name
                message = "A new initiation was approved by " + str(self.request.user) + "\n" + "Budget Amount: " + str(form.instance.total_estimated_budget) + "\n"
                getSubmiter = User.objects.get(username=self.request.user)
                emailGroup(submiter=getSubmiter.email, country=country,group=form.instance.approved_by,link=link,subject=subject,message=message)
        elif str(is_approved) == "awaiting approval" and check_agreement_status.approval != "awaiting approval":
            messages.success(self.request, 'Success, Initiation has been saved and is now Awaiting Approval (Notifications have been Sent)')
            #email the approver group so they know this was approved
            link = "Link: " + "https://" + get_current_site(self.request).name + "/activitydb/projectagreement_update/" + str(self.kwargs['pk']) + "/"
            subject = "Project Initiation Waiting for Approval: " + project_name
            message = "A new initiation was submitted for approval by " + str(self.request.user) + "\n" + "Budget Amount: " + str(form.instance.total_estimated_budget) + "\n"
            emailGroup(country=country,group=form.instance.approved_by,link=link,subject=subject,message=message)
        else:
            messages.success(self.request, 'Success, form updated!')
        form.save()
        #save formset from context
        context = self.get_context_data()
        self.object = form.save()

        return self.render_to_response(self.get_context_data(form=form))


class ProjectAgreementDetail(DetailView):

    model = ProjectAgreement
    context_object_name = 'agreement'
    queryset = ProjectAgreement.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProjectAgreementDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        context.update({'id': self.kwargs['pk']})

        try:
            getMonitor = Monitor.objects.all().filter(agreement__id=self.kwargs['pk'])
        except Monitor.DoesNotExist:
            getMonitor = None
        context.update({'getMonitor': getMonitor})

        try:
            getBenchmark = Benchmarks.objects.all().filter(agreement__id=self.kwargs['pk'])
        except Benchmarks.DoesNotExist:
            getBenchmark = None
        context.update({'getBenchmark': getBenchmark})

        try:
            getBudget = Budget.objects.all().filter(agreement__id=self.kwargs['pk'])
        except Budget.DoesNotExist:
            getBudget = None
        context.update({'getBudget': getBudget})

        try:
            getDocuments = Documentation.objects.all().filter(project__id=self.kwargs['pk']).order_by('name')
        except Documentation.DoesNotExist:
            getDocuments = None
        context.update({'getDocuments': getDocuments})

        return context


class ProjectAgreementDelete(DeleteView):
    """
    Project Agreement Delete
    """
    model = ProjectAgreement
    success_url = 'activitydb/dashboard/0/'

    @method_decorator(group_required('Country',url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectAgreementDelete, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        return HttpResponseRedirect('/activitydb/success')

    form_class = ProjectAgreementForm


class ProjectCompleteList(ListView):
    """
    Project Complete
    :param request:
    :param pk: program_id
    """
    model = ProjectComplete
    template_name = 'activitydb/projectcomplete_list.html'

    def get(self, request, *args, **kwargs):
        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

        if int(self.kwargs['pk']) == 0:
            getDashboard = ProjectComplete.objects.all().filter(program__country__in=countries)
            return render(request, self.template_name, {'getDashboard':getDashboard,'getPrograms':getPrograms})
        else:
            getDashboard = ProjectComplete.objects.all().filter(program__id=self.kwargs['pk'])
            getProgram =Program.objects.get(id=self.kwargs['pk'])

            return render(request, self.template_name, {'getProgram': getProgram, 'getDashboard':getDashboard,'getPrograms':getPrograms})


class ProjectCompleteCreate(CreateView):
    """
    Project Complete Form
    """
    model = ProjectComplete
    template_name = 'activitydb/projectcomplete_form.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Complete")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(ProjectCompleteCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProjectCompleteCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    #get shared data from project agreement and pre-populate form with it
    def get_initial(self):
        getProjectAgreement = ProjectAgreement.objects.get(id=self.kwargs['pk'])
        pre_initial = {
            'approved_by': self.request.user,
            'approval_submitted_by': self.request.user,
            'program': getProjectAgreement.program,
            'office': getProjectAgreement.office,
            'sector': getProjectAgreement.sector,
            'project_agreement': getProjectAgreement.id,
            'project_name': getProjectAgreement.project_name,
            'activity_code': getProjectAgreement.activity_code,
            'expected_start_date': getProjectAgreement.expected_start_date,
            'expected_end_date': getProjectAgreement.expected_end_date,
            'expected_duration': getProjectAgreement.expected_duration,
            'estimated_budget': getProjectAgreement.total_estimated_budget,
        }

        try:
            getSites = SiteProfile.objects.filter(projectagreement__id=getProjectAgreement.id).values_list('id',flat=True)
            site = {'site': [o for o in getSites], }
            initial = pre_initial.copy()
            initial.update(site)
        except SiteProfile.DoesNotExist:
            getSites = None

        try:
            getStakeholder = Stakeholder.objects.filter(projectagreement__id=getProjectAgreement.id).values_list('id',flat=True)
            stakeholder = {'stakeholder': [o for o in getStakeholder], }
            initial = pre_initial.copy()
            initial.update(stakeholder)
        except Stakeholder.DoesNotExist:
            getStakeholder = None

        return initial

    def get_context_data(self, **kwargs):
        context = super(ProjectCompleteCreate, self).get_context_data(**kwargs)

        pk = self.kwargs['pk']
        context.update({'pk': pk})

        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        context = self.get_context_data()
        self.object = form.save()

        latest = ProjectComplete.objects.latest('id')
        getComplete = ProjectComplete.objects.get(id=latest.id)
        getAgreement = ProjectAgreement.objects.get(id=self.request.POST['project_agreement'])

        #update the quantitative data fields to include the newly created complete
        CollectedData.objects.filter(agreement__id=getComplete.project_agreement_id).update(complete=getComplete)

        #update the other budget items
        Budget.objects.filter(agreement__id=getComplete.project_agreement_id).update(complete=getComplete)

        #update the benchmarks
        Benchmarks.objects.filter(agreement__id=getComplete.project_agreement_id).update(complete=getComplete)

        #update main compelte fields
        ProjectComplete.objects.filter(id=getComplete.id).update(account_code=getAgreement.account_code, lin_code=getAgreement.lin_code)

        messages.success(self.request, 'Success, Tracking Form Created!')
        redirect_url = '/activitydb/projectcomplete_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = ProjectCompleteCreateForm


class ProjectCompleteUpdate(UpdateView):
    """
    Project Tracking Form
    """
    model = ProjectComplete
    template_name = 'activitydb/projectcomplete_form.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Complete")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(ProjectCompleteUpdate, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class):
        check_form_type = ProjectComplete.objects.get(id=self.kwargs['pk'])

        if check_form_type.project_agreement.short == True:
            form = ProjectCompleteSimpleForm
        else:
            form = ProjectCompleteForm

        return form(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(ProjectCompleteUpdate, self).get_context_data(**kwargs)
        getComplete = ProjectComplete.objects.get(id=self.kwargs['pk'])
        id = getComplete.project_agreement_id
        context.update({'id': id})
        pk = self.kwargs['pk']
        context.update({'pk': pk})

        # get budget data
        try:
            getBudget = Budget.objects.all().filter(agreement__id=getComplete.project_agreement_id)
        except Budget.DoesNotExist:
            getBudget = None
        context.update({'getBudget': getBudget})

        # get Quantitative data
        try:
            getQuantitative = CollectedData.objects.all().filter(agreement__id=getComplete.project_agreement_id).order_by('indicator')
        except CollectedData.DoesNotExist:
            getQuantitative = None
        context.update({'getQuantitative': getQuantitative})

        # get benchmark or project components
        try:
            getBenchmark = Benchmarks.objects.all().filter(agreement__id=getComplete.project_agreement_id).order_by('description')
        except Benchmarks.DoesNotExist:
            getBenchmark = None
        context.update({'getBenchmark': getBenchmark})

        # get documents from the original agreement (documents are not seperate in complete)
        try:
            getDocuments = Documentation.objects.all().filter(project__id=getComplete.project_agreement_id).order_by('name')
        except Documentation.DoesNotExist:
            getDocuments = None
        context.update({'getDocuments': getDocuments})


        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProjectCompleteUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    #get shared data from project agreement and pre-populate form with it
    def get_initial(self):
        initial = {
            'approved_by': self.request.user,
            'approval_submitted_by': self.request.user,
        }

        #update budget with new agreement
        try:
            getBudget = Budget.objects.all().filter(complete_id=self.kwargs['pk'])
            #if there aren't any budget try importing from the agreement
            if not getBudget:
                getComplete = ProjectComplete.objects.get(id=self.kwargs['pk'])
                Budget.objects.filter(agreement=getComplete.project_agreement_id).update(complete_id=self.kwargs['pk'])
        except Budget.DoesNotExist:
            getBudget = None

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        self.object = form.save()

        messages.success(self.request, 'Success, form updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProjectCompleteForm


class ProjectCompleteDetail(DetailView):

    model = ProjectComplete
    context_object_name = 'complete'

    def get_object(self, queryset=ProjectComplete.objects.all()):
        try:
            return queryset.get(project_agreement__id=self.kwargs['pk'])
        except ProjectComplete.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):

        context = super(ProjectCompleteDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        try:
            data = ProjectComplete.objects.all().filter(project_agreement__id=self.kwargs['pk'])
        except ProjectComplete.DoesNotExist:
            data = None
        """
        getData = serializers.serialize('python', data)
        #return just the fields and skip the object name
        justFields = [d['fields'] for d in getData]
        #temp name fiels
        jsonData =json.dumps(justFields, default=date_handler)
        context.update({'jsonData': jsonData})
        """
        context.update({'id':self.kwargs['pk']})

        return context


class ProjectCompleteDelete(DeleteView):
    """
    Project Complete Delete
    """
    model = ProjectComplete
    success_url = '/activitydb/projectcomplete_list/0/'

    @method_decorator(group_required('Country',url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(ProjectCompleteDelete, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        return HttpResponseRedirect('/activitydb/success')

    form_class = ProjectCompleteForm


class ProjectCompleteImport(ListView):

    def get_context_data(self, **kwargs):
        context = super(ProjectCompleteImport, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    template_name = 'activitydb/projectcomplete_import.html'


class DocumentationList(ListView):
    """
    Documentation
    """
    model = Documentation
    template_name = 'activitydb/documentation_list.html'

    def get(self, request, *args, **kwargs):

        project_agreement_id = self.kwargs['project']
        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

        if int(self.kwargs['program']) != 0 & int(self.kwargs['project']) == 0:
            getDocumentation = Documentation.objects.all().prefetch_related('program','project').filter(program__id=self.kwargs['program'])
        elif int(self.kwargs['project']) != 0:
            getDocumentation = Documentation.objects.all().prefetch_related('program','project').filter(project__id=self.kwargs['project'])
        else:
            countries = getCountry(request.user)
            getDocumentation = Documentation.objects.all().prefetch_related('program','project','project__office').filter(program__country__in=countries)

        return render(request, self.template_name, {'getPrograms': getPrograms, 'getDocumentation':getDocumentation, 'project_agreement_id': project_agreement_id})


class DocumentationAgreementList(AjaxableResponseMixin, CreateView):
    """
       Documentation Modal List
    """
    model = Documentation
    template_name = 'activitydb/documentation_popup_list.html'

    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

        getDocumentation = Documentation.objects.all().prefetch_related('program', 'project')


        return render(request, self.template_name, {'getPrograms': getPrograms, 'getDocumentation': getDocumentation})


class DocumentationAgreementCreate(AjaxableResponseMixin, CreateView):
    """
    Documentation Form
    """
    model = Documentation
    template_name = 'activitydb/documentation_popup_form.html'

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Documentation")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(DocumentationAgreementCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(DocumentationAgreementCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DocumentationAgreementCreate, self).get_context_data(**kwargs)
        getProject = ProjectAgreement.objects.get(id=self.kwargs['id'])
        context.update({'program': getProject.program})
        context.update({'project': getProject})
        context.update({'id': self.kwargs['id']})
        return context

    def get_initial(self):
        getProject = ProjectAgreement.objects.get(id=self.kwargs['id'])
        initial = {
            'project': self.kwargs['id'],
            'program': getProject.program,
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Documentation Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


class DocumentationAgreementUpdate(AjaxableResponseMixin, UpdateView):
    """
    Documentation Form
    """
    model = Documentation
    template_name = 'activitydb/documentation_popup_form.html'

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Documentation")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(DocumentationAgreementUpdate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(DocumentationAgreementUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DocumentationAgreementUpdate, self).get_context_data(**kwargs)
        getProject = ProjectAgreement.objects.get(id=self.kwargs['id'])
        context.update({'project': getProject})
        context.update({'id': self.kwargs['id']})
        context.update({'pk': self.kwargs['pk']})
        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Documentation Updated!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


class DocumentationAgreementDelete(AjaxableResponseMixin, DeleteView):
    """
    Documentation Delete popup window
    """
    model = Documentation
    template_name = 'activitydb/documentation_agreement_confirm_delete.html'
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(DocumentationAgreementDelete, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Documentation Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


class DocumentationCreate(CreateView):
    """
    Documentation Form
    """
    model = Documentation

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Documentation")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(DocumentationCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(DocumentationCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Documentation Created!')
        latest = Documentation.objects.latest('id')
        redirect_url = '/activitydb/documentation_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = DocumentationForm


class DocumentationUpdate(UpdateView):
    """
    Documentation Form
    """
    model = Documentation
    queryset = Documentation.objects.select_related()

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Documentation")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(DocumentationUpdate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(DocumentationUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()
        messages.success(self.request, 'Success, Documentation Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


class DocumentationDelete(DeleteView):
    """
    Documentation Form
    """
    model = Documentation
    success_url = '/activitydb/documentation_list/0/0/'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Documentation Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


class SiteProfileList(ListView):
    """
    SiteProfile list creates a map and list of sites by user country access and filters
    by either direct link from project or by program dropdown filter
    """
    model = SiteProfile
    template_name = 'activitydb/site_profile_list.html'

    def dispatch(self, request, *args, **kwargs):
        if request.GET.has_key('report'):
            template_name = 'activitydb/site_profile_report.html'
        else:
            template_name = 'activitydb/site_profile_list.html'
        return super(SiteProfileList, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        activity_id = int(self.kwargs['activity_id'])
        program_id = int(self.kwargs['program_id'])

        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

        #this date, 3 months ago, a site is considered inactive
        inactiveSite = pytz.UTC.localize(datetime.now()) - relativedelta(months=3)

        #Filter SiteProfile list and map by activity or program
        if activity_id != 0:
            getSiteProfile = SiteProfile.objects.all().prefetch_related('country','district','province').filter(projectagreement__id=activity_id).distinct()
        elif program_id != 0:
            getSiteProfile = SiteProfile.objects.all().prefetch_related('country','district','province').filter(Q(projectagreement__program__id=program_id) | Q(collecteddata__program__id=program_id)).distinct()
        else:
            getSiteProfile = SiteProfile.objects.all().prefetch_related('country','district','province').filter(country__in=countries).distinct()
        if request.method == "GET" and "search" in request.GET:
            """
             fields = ('name', 'office')
            """
            getSiteProfile = SiteProfile.objects.all().filter(Q(country__in=countries), Q(name__contains=request.GET["search"]) | Q(office__name__contains=request.GET["search"]) | Q(type__profile__contains=request.GET['search']) |
                                                            Q(province__name__contains=request.GET["search"]) | Q(district__name__contains=request.GET["search"]) | Q(village__contains=request.GET['search']) |
                                                             Q(projectagreement__project_name__contains=request.GET["search"]) | Q(projectcomplete__project_name__contains=request.GET['search'])).select_related().distinct()

        return render(request, self.template_name, {'inactiveSite':inactiveSite,'getSiteProfile':getSiteProfile,'project_agreement_id': activity_id,'country': countries,'getPrograms':getPrograms, 'form': FilterForm(), 'helper': FilterForm.helper})

class SiteProfileReport(ListView):
    """
    SiteProfile Report filtered by project
    """
    model = SiteProfile
    template_name = 'activitydb/site_profile_report.html'

    def get(self, request, *args, **kwargs):
        countries = getCountry(request.user)
        project_agreement_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getCommunity = SiteProfile.objects.all()
        else:
            getCommunity = SiteProfile.objects.all().filter(projectagreement__id=self.kwargs['pk'])

        id=self.kwargs['pk']

        return render(request, self.template_name, {'getCommunity':getCommunity,'project_agreement_id': project_agreement_id,'id':id,'country': countries})


class SiteProfileCreate(CreateView):
    """
    Using SiteProfile Form, create a new site profile
    """
    model = SiteProfile

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="SiteProfile")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(SiteProfileCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(SiteProfileCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        countries = getCountry(self.request.user)
        default_country = None
        if countries:
            default_country = countries[0]
        initial = {
            'approved_by': self.request.user,
            'filled_by': self.request.user,
            'country': default_country
        }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Site Profile Created!')
        latest = SiteProfile.objects.latest('id')
        redirect_url = '/activitydb/siteprofile_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = SiteProfileForm


class SiteProfileUpdate(UpdateView):
    """
    SiteProfile Form Update an existing site profile
    """
    model = SiteProfile

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="SiteProfile")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(SiteProfileUpdate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(SiteProfileUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SiteProfileUpdate, self).get_context_data(**kwargs)
        getProjects = ProjectAgreement.objects.all().filter(site__id=self.kwargs['pk'])
        context.update({'getProjects': getProjects})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, SiteProfile Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = SiteProfileForm


class SiteProfileDelete(DeleteView):
    """
    SiteProfile Form Delete an existing community
    """
    model = SiteProfile
    success_url = "/activitydb/siteprofile_list/0/0/"

    @method_decorator(group_required('Country',url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(SiteProfileDelete, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, SiteProfile Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = SiteProfileForm


class MonitorList(ListView):
    """
    Monitoring Data
    """
    model = Monitor
    template_name = 'activitydb/monitor_list.html'

    def get(self, request, *args, **kwargs):

        project_agreement_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getMonitorData = Monitor.objects.all()
        else:
            getMonitorData = Monitor.objects.all().filter(agreement__id=self.kwargs['pk'])

        if int(self.kwargs['pk']) == 0:
            getBenchmarkData = Benchmarks.objects.all()
        else:
            getBenchmarkData = Benchmarks.objects.all().filter(agreement__id=self.kwargs['pk'])

        return render(request, self.template_name, {'getMonitorData': getMonitorData, 'getBenchmarkData': getBenchmarkData,'project_agreement_id': project_agreement_id})


class MonitorCreate(AjaxableResponseMixin,CreateView):
    """
    Monitor Form
    """
    model = Monitor

    def dispatch(self, request, *args, **kwargs):
        return super(MonitorCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MonitorCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    def get_initial(self):
        initial = {
            'agreement': self.kwargs['id'],
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Monitor Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = MonitorForm


class MonitorUpdate(AjaxableResponseMixin, UpdateView):
    """
    Monitor Form
    """
    model = Monitor

    def get_context_data(self, **kwargs):
        context = super(MonitorUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Monitor Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = MonitorForm


class MonitorDelete(AjaxableResponseMixin, DeleteView):
    """
    Monitor Form
    """
    model = Monitor
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(MonitorDelete, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Monitor Deleted!')
        return self.render_to_response(self.get_context_data(form=form))


class BenchmarkCreate(AjaxableResponseMixin, CreateView):
    """
    Benchmark Form
    """
    model = Benchmarks

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(BenchmarkCreate, self).get_form_kwargs()
        try:
            getComplete = ProjectComplete.objects.get(project_agreement__id=self.kwargs['id'])
            kwargs['complete'] = getComplete.id
        except ProjectComplete.DoesNotExist:
            kwargs['complete'] = None

        kwargs['request'] = self.request
        kwargs['agreement'] = self.kwargs['id']
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        return super(BenchmarkCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BenchmarkCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    def get_initial(self):
        try:
            getComplete = ProjectComplete.objects.get(project_agreement__id=self.kwargs['id'])
            initial = {
                'agreement': self.kwargs['id'],
                'complete': getComplete.id,
                }
        except ProjectComplete.DoesNotExist:
            initial = {
                'agreement': self.kwargs['id'],
                }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Component Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = BenchmarkForm


class BenchmarkUpdate(AjaxableResponseMixin, UpdateView):
    """
    Benchmark Form
    """
    model = Benchmarks

    def get_context_data(self, **kwargs):
        context = super(BenchmarkUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(BenchmarkUpdate, self).get_form_kwargs()
        getBenchmark = Benchmarks.objects.all().get(id=self.kwargs['pk'])

        kwargs['request'] = self.request
        kwargs['agreement'] = getBenchmark.agreement.id
        if getBenchmark.complete:
            kwargs['complete'] = getBenchmark.complete.id
        else:
            kwargs['complete'] = None

        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Component Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = BenchmarkForm


class BenchmarkDelete(AjaxableResponseMixin, DeleteView):
    """
    Benchmark Form
    """
    model = Benchmarks
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(BenchmarkDelete, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Component Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = BenchmarkForm


class ContactList(ListView):
    """
    getStakeholders
    """
    model = Contact
    template_name = 'activitydb/contact_list.html'

    def get(self, request, *args, **kwargs):

        project_agreement_id = self.kwargs['pk']

        getProject = ProjectAgreement.objects.all().filter(id=project_agreement_id)

        if int(self.kwargs['pk']) == 0:
            countries=getCountry(request.user)
            getContacts = Contact.objects.all().filter(country__in=countries)
        else:
            getContacts = Contact.objects.all().filter(stakeholder__projectagreement=project_agreement_id)

        return render(request, self.template_name, {'getContacts': getContacts, 'getProject': getProject})


class ContactCreate(CreateView):
    """
    Contact Form
    """
    model = Contact

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Contact")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(ContactCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    def get_initial(self):
        country = getCountry(self.request.user)[0]
        initial = {
            'agreement': self.kwargs['id'],
            'country': country,
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Contact Created!')
        latest = Contact.objects.latest('id')
        redirect_url = '/activitydb/contact_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = ContactForm


class ContactUpdate(UpdateView):
    """
    Contact Form
    """
    model = Contact

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Contact")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(ContactUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Contact Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = ContactForm


class ContactDelete(DeleteView):
    """
    Benchmark Form
    """
    model = Contact
    success_url = '/'

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(ContactDelete, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactDelete, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Contact Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = ContactForm


class StakeholderList(ListView):
    """
    getStakeholders
    """
    model = Stakeholder
    template_name = 'activitydb/stakeholder_list.html'

    def get(self, request, *args, **kwargs):

        project_agreement_id = self.kwargs['pk']
        countries = getCountry(request.user)
        if int(self.kwargs['pk']) == 0:
            getStakeholders = Stakeholder.objects.all().filter(country__in=countries)
        else:
            getStakeholders = Stakeholder.objects.all().filter(projectagreement=self.kwargs['pk'])

        return render(request, self.template_name, {'getStakeholders': getStakeholders, 'project_agreement_id': project_agreement_id})


class StakeholderCreate(CreateView):
    """
    Stakeholder Form
    """
    model = Stakeholder

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Stakeholder")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(StakeholderCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(StakeholderCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(StakeholderCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    def get_initial(self):

        country = getCountry(self.request.user)[0]

        initial = {
            'agreement': self.kwargs['id'],
            'country': country,
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Stakeholder Created!')
        latest = Stakeholder.objects.latest('id')
        redirect_url = '/activitydb/stakeholder_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = StakeholderForm


class StakeholderUpdate(UpdateView):
    """
    Stakeholder Form
    """
    model = Stakeholder

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Stakeholder")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(StakeholderUpdate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(StakeholderUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(StakeholderUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Stakeholder Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = StakeholderForm


class StakeholderDelete(DeleteView):
    """
    Benchmark Form
    """
    model = Stakeholder
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(StakeholderDelete, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Stakeholder Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = StakeholderForm


class TrainingList(ListView):
    """
    Training Attendance
    """
    model = TrainingAttendance
    template_name = 'activitydb/training_list.html'

    def get(self, request, *args, **kwargs):

        project_agreement_id = self.kwargs['pk']
        countries = getCountry(request.user)
        if int(self.kwargs['pk']) == 0:
            getTraining = TrainingAttendance.objects.all().filter(program__country__in=countries)
        else:
            getTraining = TrainingAttendance.objects.all().filter(project_agreement_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getTraining': getTraining, 'project_agreement_id': project_agreement_id})


class TrainingCreate(CreateView):
    """
    Training Form
    """
    model = TrainingAttendance

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Training")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(TrainingCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(TrainingCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        initial = {
            'agreement': self.kwargs['id'],
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Training Created!')
        latest = TrainingAttendance.objects.latest('id')
        redirect_url = '/activitydb/training_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = TrainingAttendanceForm


class TrainingUpdate(UpdateView):
    """
    Training Form
    """
    model = TrainingAttendance

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Training")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(TrainingUpdate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(TrainingUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Training Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = TrainingAttendanceForm


class TrainingDelete(DeleteView):
    """
    Training Delete
    """
    model = TrainingAttendance
    success_url = '/activitydb/training_list/0/'
    template_name = 'activitydb/training_confirm_delete.html'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Training Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = TrainingAttendanceForm


class BeneficiaryList(ListView):
    """
    Beneficiary
    """
    model = Beneficiary
    template_name = 'activitydb/beneficiary_list.html'

    def get(self, request, *args, **kwargs):

        project_agreement_id = self.kwargs['pk']
        countries = getCountry(request.user)

        if int(self.kwargs['pk']) == 0:
            getBeneficiaries = Beneficiary.objects.all().filter(Q(training__program__country__in=countries) | Q(distribution__program__country__in=countries) )
        else:
            getBeneficiaries = Beneficiary.objects.all().filter(training_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getBeneficiaries': getBeneficiaries, 'project_agreement_id': project_agreement_id})


class BeneficiaryCreate(CreateView):
    """
    Beneficiary Form
    """
    model = Beneficiary

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Beneficiary")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(BeneficiaryCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = {
            'training': self.kwargs['id'],
            }

        return initial

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(BeneficiaryCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Beneficiary Created!')
        latest = Beneficiary.objects.latest('id')
        redirect_url = '/activitydb/beneficiary_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = BeneficiaryForm


class BeneficiaryUpdate(UpdateView):
    """
    Training Form
    """
    model = Beneficiary

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Beneficiary")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(BeneficiaryUpdate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(BeneficiaryUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Beneficiary Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = BeneficiaryForm


class BeneficiaryDelete(DeleteView):
    """
    Beneficiary Delete
    """
    model = Beneficiary
    success_url = reverse_lazy('beneficiary_list')

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(BeneficiaryDelete, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Beneficiary Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = BeneficiaryForm

class DistributionList(ListView):
    """
    Distribution
    """
    model = Distribution
    template_name = 'activitydb/distribution_list.html'

    def get(self, request, *args, **kwargs):

        program_id = self.kwargs['pk']
        countries = getCountry(request.user)
        if int(self.kwargs['pk']) == 0:
            getDistribution = Distribution.objects.all().filter(program__country__in=countries)
        else:
            getDistribution = Distribution.objects.all().filter(program_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getDistribution': getDistribution, 'program_id': program_id})


class DistributionCreate(CreateView):
    """
    Distribution Form
    """
    model = Distribution

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Distribution")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(DistributionCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(DistributionCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        initial = {
            'program': self.kwargs['id']
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Distribution Created!')
        latest = Distribution.objects.latest('id')
        redirect_url = '/activitydb/distribution_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = DistributionForm


class DistributionUpdate(UpdateView):
    """
    Distribution Form
    """
    model = Distribution

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Distribution")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(DistributionUpdate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(DistributionUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Distribution Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = DistributionForm


class DistributionDelete(DeleteView):
    """
    Distribution Delete
    """
    model = Distribution
    success_url = '/activitydb/distribution_list/0/'
    template_name = 'activitydb/distribution_confirm_delete.html'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Distribution Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DistributionForm


class QuantitativeOutputsCreate(AjaxableResponseMixin, CreateView):
    """
    QuantitativeOutput Form
    """
    model = CollectedData
    template_name = 'activitydb/quantitativeoutputs_form.html'

    def get_context_data(self, **kwargs):
        context = super(QuantitativeOutputsCreate, self).get_context_data(**kwargs)
        getProgram = Program.objects.get(agreement__id = self.kwargs['id'])
        context.update({'id': self.kwargs['id']})
        context.update({'program': getProgram})
        return context

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(QuantitativeOutputsCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        getProgram = Program.objects.get(agreement__id = self.kwargs['id'])
        initial = {
            'agreement': self.kwargs['id'],
            'program': getProgram.id,
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Quantitative Output Created!')
        form = ""
        return self.render_to_response(self.get_context_data(form=form))


    form_class = QuantitativeOutputsForm


class QuantitativeOutputsUpdate(AjaxableResponseMixin, UpdateView):
    """
    QuantitativeOutput Form
    """
    model = CollectedData
    template_name = 'activitydb/quantitativeoutputs_form.html'

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(QuantitativeOutputsUpdate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        """
        get the program to filter the list and indicators by.. the FK to colelcteddata is i_program
        we should change that name at somepoint as it is very confusing
        """
        getProgram = Program.objects.get(i_program__pk=self.kwargs['pk'])
        initial = {
            'program': getProgram.id,
            }

        return initial

    def get_context_data(self, **kwargs):
        context = super(QuantitativeOutputsUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Quantitative Output Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = QuantitativeOutputsForm


class QuantitativeOutputsDelete(AjaxableResponseMixin, DeleteView):
    """
    QuantitativeOutput Delete
    """
    model = CollectedData
    success_url = '/'

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(QuantitativeOutputsDelete, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Quantitative Output Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = QuantitativeOutputsForm


class BudgetList(ListView):
    """
    Budget List
    """
    model = Budget
    template_name = 'activitydb/budget_list.html'

    def get(self, request, *args, **kwargs):

        project_agreement_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getBudget = Budget.objects.all()
        else:
            getBudget = Budget.objects.all().filter(project_agreement_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getBudget': getBudget, 'project_agreement_id': project_agreement_id})


class BudgetCreate(AjaxableResponseMixin, CreateView):
    """
    Budget Form
    """
    model = Budget
    template_name = 'activitydb/budget_form.html'

    def get_context_data(self, **kwargs):
        context = super(BudgetCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(BudgetCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = {
            'agreement': self.kwargs['id'],
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Budget Created!')
        form = ""
        return self.render_to_response(self.get_context_data(form=form))


    form_class = BudgetForm


class BudgetUpdate(AjaxableResponseMixin, UpdateView):
    """
    Budget Form
    """
    model = Budget

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(BudgetUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BudgetUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Budget Output Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = BudgetForm


class BudgetDelete(AjaxableResponseMixin, DeleteView):
    """
    Budget Delete
    """
    model = Budget
    success_url = '/'

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(BudgetDelete, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BudgetDelete, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Budget Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = BudgetForm


class ChecklistItemList(ListView):
    """
    Checklist List
    """
    model = ChecklistItem
    template_name = 'activitydb/checklist_list.html'

    def get(self, request, *args, **kwargs):

        project_agreement_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getChecklist = ChecklistItem.objects.all()
        else:
            getChecklist = ChecklistItem.objects.all().filter(checklist__agreement_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getChecklist': getChecklist, 'project_agreement_id': self.kwargs['pk']})


class ChecklistItemCreate(CreateView):
    """
    Checklist Form
    """
    model = ChecklistItem

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="ChecklistItem")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(ChecklistItemCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChecklistItemCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ChecklistItemCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(ChecklistItemCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        checklist = Checklist.objects.get(agreement=self.kwargs['id'])
        initial = {
            'checklist': checklist,
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Checklist Item Created!')
        latest = ChecklistItem.objects.latest('id')
        redirect_url = '/activitydb/checklistitem_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)


    form_class = ChecklistItemForm


class ChecklistItemUpdate(UpdateView):
    """
    Checklist Form
    """
    model = ChecklistItem

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="ChecklistItem")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(ChecklistItemUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChecklistItemUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ChecklistItemUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Checklist Item Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = ChecklistItemForm


def checklist_update_link(AjaxableResponseMixin,pk,type,value):
    """
    Checklist Update from Link
    """
    value = int(value)

    if type == "in_file":
        update = ChecklistItem.objects.filter(id=pk).update(in_file=value)
    elif type == "not_applicable":
        update = ChecklistItem.objects.filter(id=pk).update(not_applicable=value)

    return HttpResponse(value)


class ChecklistItemDelete(DeleteView):
    """
    Checklist Delete
    """
    model = ChecklistItem
    success_url = '/'

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(ChecklistItemDelete, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChecklistItemDelete, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Checklist Item Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = ChecklistItemForm


def report(request):
    """
    project agreement list report
    """
    countries=getCountry(request.user)
    getAgreements = ProjectAgreement.objects.select_related().filter(program__country__in=countries)
    filtered = ProjectAgreementFilter(request.GET, queryset=getAgreements)
    table = ProjectAgreementTable(filtered.queryset)
    table.paginate(page=request.GET.get('page', 1), per_page=20)

    if request.method == "GET" and "search" in request.GET:
        #list1 = list()
        #for obj in filtered:
        #    list1.append(obj)
        """
         fields = 'program','community'
        """
        getAgreements = ProjectAgreement.objects.filter(
                                           Q(project_name__contains=request.GET["search"]) |
                                           Q(activity_code__contains=request.GET["search"]))
        table = ProjectAgreementTable(getAgreements)

    RequestConfig(request).configure(table)

    if request.GET.get('export'):
        dataset = ProjectAgreementResource().export(getAgreements)
        response = HttpResponse(dataset.csv, content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=activity_report.csv'
        return response

    # send the keys and vars
    return render(request, "activitydb/report.html", {'get_agreements': table, 'country': countries, 'form': FilterForm(), 'filter': filtered, 'helper': FilterForm.helper})


def country_json(request, country):
    """
    For populating the province dropdown based  country dropdown value
    """
    selected_country = Country.objects.get(id=country)
    province = Province.objects.all().filter(country=selected_country)
    provinces_json = serializers.serialize("json", province)
    return HttpResponse(provinces_json, content_type="application/json")


def province_json(request, province):
    """
    For populating the office district based  country province value
    """
    selected_province = Province.objects.get(id=province)
    district = District.objects.all().filter(province=selected_province)
    districts_json = serializers.serialize("json", district)
    return HttpResponse(districts_json, content_type="application/json")


def district_json(request, district):
    """
    For populating the office dropdown based  country dropdown value
    """
    selected_district = District.objects.get(id=district)
    adminthree = AdminLevelThree.objects.all().filter(district=selected_district)
    adminthree_json = serializers.serialize("json", adminthree)
    return HttpResponse(adminthree_json, content_type="application/json")


def import_service(service_id=1, deserialize=True):
    """
    Import a indicators from a web service (the dig only for now)
    """
    service = ExternalService.objects.all().filter(id=service_id)

    response = requests.get(service.feed_url)
    get_json = json.loads(response.content)

    if deserialize == True:
        data = json.load(get_json) # deserialises it
    else:
        #send json data back not deserialized data
        data = get_json
    #debug the json data string uncomment dump and print
    data2 = json.dumps(data) # json formatted string

    return data


def service_json(request, service):
    """
    For populating service indicators in dropdown
    """
    service_indicators = import_service(service,deserialize=False)
    return HttpResponse(service_indicators, content_type="application/json")

# This lists available custom dashboards to view
class CustomDashboardList(ListView):
    """
    CustomDashboard
    :param request:
    :param pk: program_id
    """
    model = CustomDashboard
    template_name = 'customdashboard/admin/dashboard_list.html'

    def get(self, request, *args, **kwargs):
    ## retrieve program
        model = Program
        program_id = int(self.kwargs['pk'])
        getProgram = Program.objects.all().filter(id=program_id)

        ## retrieve the coutries the user has data access for
        countries = getCountry(request.user)

        #retrieve projects for a program
        # getProjects = ProjectAgreement.objects.all().filter(program__id=program__id, program__country__in=countries)

        #retrieve projects for a program
        getCustomDashboards = CustomDashboard.objects.all().filter(program=program_id)
            
        return render(request, self.template_name, {'getCustomDashboards': getCustomDashboards, 'getProgram': getProgram})

class CustomDashboardCreate(CreateView):
    #   :param request:
    #   :param id:
    #   """
    model = CustomDashboard
    template_name = 'customdashboard/admin/customdashboard_form.html'

    try:
        guidance = FormGuidance.objects.get(form="CustomDashboard")
    except FormGuidance.DoesNotExist:
        guidance = None

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(CustomDashboardCreate, self).dispatch(request, *args, **kwargs)

     # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(CustomDashboardCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        initial = {}
        return initial

    def get_context_data(self, **kwargs):
        context = super(CustomDashboardCreate, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        print form
        form.save()

        #save formset from context
        context = self.get_context_data()

        messages.success(self.request, 'Success, Dashboard Created!')

        latest = CustomDashboard.objects.latest('id')
        getCustomDashboard = CustomDashboard.objects.get(id=latest.id)
        dashboard_id = getCustomDashboard.id
        redirect_url = '/activitydb/custom_dashboard_update/' + str(dashboard_id) 
        return HttpResponseRedirect(redirect_url)

    form_class = CustomDashboardCreateForm 

class CustomDashboardDetail(DetailView):

    model = CustomDashboard

    # def get_object(self, queryset=CustomDashboard.objects.all()):
    #     try:
    #         # return queryset.get(customdashboard__id = self.kwarg['id'])
    #     except CustomDashboard.DoesNotExist:
    #         return None

    def get_template_names(self):
        dashboard = CustomDashboard.objects.get(id = self.kwargs['pk'])
        getDashboardTheme = DashboardTheme.objects.all().filter(id = dashboard.theme.id)
        template_name = getDashboardTheme[0].theme_template
        return template_name

    def get_context_data(self, **kwargs):
        context = super(CustomDashboardDetail, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context.update({'pk': pk})

        try:
            getCustomDashboard =CustomDashboard.objects.get(id=self.kwargs['pk'])
        except CustomDashboard.DoesNotExist:
            getCustomDashboard = None
        context.update({'getCustomDashboard': getCustomDashboard})

        try:
            selected_theme = getCustomDashboard.theme.id
            getDashboardTheme = DashboardTheme.objects.all().filter(id=selected_theme)
        except DashboardTheme.DoesNotExist:
            getDashboardTheme = None
        context.update({'getDashboardTheme': getDashboardTheme})

        try:
            getDashboardComponents = getCustomDashboard.components.all()
        except DashboardComponent.DoesNotExist:
            getDashboardComponents = None
        context.update({'getDashboardComponents': getDashboardComponents})
        
        try:
            color_selection = getCustomDashboard.color_palette
            if color_selection == 'bright':
                getColorPalette = ['#82BC00','#C8C500','#10A400','#CF102E','#DB5E11','#A40D7A','#00AFA8','#1349BB','#FFD200','#FF7100','#FFFD00','#ABABAB','#7F7F7F','#7B5213','#C18A34'],
            else:
                getColorPalette = ['#BAEE46','#FDFB4A','#4BCF3D','#F2637A','#FFA268','#C451A4','#4BC3BE','#5B7FCC','#9F54CC','#FFE464','#FFA964','#FFFE64','#D7D7D7','#7F7F7F','#D2A868','#FFD592']
        except getCustomDashboard.DoesNotExist:
                getColorPalette = None
        context.update({'getColorPalette': getColorPalette})


    # Process for Matching Data and Subcomponent Template
    # Step 1: Retrieve JSON data for components
    # Step 2: colorize data with colorDictionary 
    # Step 3: Pass that component data to the template -- associate component # in getAllComponentData to template
    # Step 4: Include correct component template  "include component.component_template" for that component
        try:
            getAllComponentData = {}
            projectDictionary = {} 
            for component in getDashboardComponents:
              getSingleComponentData = {}
              for data in component.data_sources.all():
                filter_url = 'http://tables.toladata.io/api/silo/9/data/'
                #data.data_source + data.data_filter_key
                headers = {
                         'content-type': 'application/json',
                         'Authorization': 'Token bd43de0c16ac0400bc404c6598a6fe0e4ce73aa2'}
                response = requests.get(filter_url, headers=headers, verify=False)
                get_json = json.loads(response.content)
                getSingleComponentData["{{data.data_name}}"] = get_json
                # should this be getSingleComponentData[data.data_name.data] = get_json
                # and then taking that set of values and looking at the data dictionary for color matches
                # if data.data_name.data.labels:
                #     colorsQueue = getColorPalette
                #     colors = []
                #     for label in data.data_name.data.labels:
                #         if label in projectDictionary:
                #             colors.append(projectDictionary['{{label}}'])
                #             #remove projectDictionary['{{label}}'] from colorsQueue
                #         else:
                #             poppedColor = colorsQueue.pop()
                #             projectDictionary['{{label}}'] = poppedColor
                #             colors.append(productDictionary('{{label}}'))
                getSingleComponentData["{{data.data_name}}"] = {'data': get_json} #when ready, add colors: color_selection
              getAllComponentData["{{component.component_name}}"] = getSingleComponentData
        except DashboardComponent.DoesNotExist:
            getAllComponentData = None
        context.update({'getAllComponentData': getAllComponentData})

        return context

def custom_dashboard_update_components(AjaxableResponseMixin,pk,location,type): #component_map):
# (?P<pk>[0-9]+)/(?P<location>[0-9]+)/(?P<type>[-\w]+)/$
    # form_mapping = component_map
    mapped = false
    current_dashboard = CustomDashboard.objects.get(id=self.kwargs['pk'])
    current_map = current_dashboard.component_map#.split("]","],")
    # for mapped_object in current_map:
    #     if mapping.0 == form_mapping.0
    #         update = current_dashboard.update(component_map=form_mapping)
    #         mapped = true
    # if mapped == false:
    #     update = current_dashboard.component_map.append(form_mapping)
    #     current_dashboard.save()
    return HttpResponse(component_map)


class CustomDashboardUpdate(UpdateView):

    model = CustomDashboard
    form_class = CustomDashboardForm

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            guidance = FormGuidance.objects.get(form="CustomDashboard")
        except FormGuidance.DoesNotExist:
            guidance = None
        
        return super(CustomDashboardUpdate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        getCustomDashboard = CustomDashboard.objects.get(id=self.kwargs['pk'])
        getDashboardComponents = DashboardComponent.objects.all().filter(componentset=getCustomDashboard)
        getComponentDataSources = ComponentDataSource.objects.all()
        initial = {
            'getCustomDashboard': getCustomDashboard,
            'getDashboardComponents': getDashboardComponents,
            'getComponentDataSources': getComponentDataSources,
            }

        return initial

    def get_form(self, form_class):
        check_form_type = self.request.get_full_path()
        if check_form_type.startswith('/activitydb/custom_dashboard_edit'):
            form = CustomDashboardModalForm
        else:
            form = CustomDashboardForm

        return form(**self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(CustomDashboardUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context.update({'pk': pk})

        check_path = self.request.get_full_path()
        if check_path.startswith('/activitydb/custom_dashboard_map'):
            location = self.kwargs['location']
            component_type = self.kwargs['type']
        # else if check_form_type.startswith('/activitydb/custom_dashboard_remap'):
        #     location = self.kwargs['location']
        #     component_type = self.kwargs['type']
        else:
            location = None
            component_type = None
        context.update({'location': location})
        context.update({'component_type': component_type})

        try:
            getCustomDashboard =CustomDashboard.objects.get(id=self.kwargs['pk'])
        except CustomDashboard.DoesNotExist:
            getCustomDashboard = None
        context.update({'getCustomDashboard': getCustomDashboard})

        try:
            selected_theme = getCustomDashboard.theme.id
            getDashboardTheme = DashboardTheme.objects.all().filter(id=selected_theme)
        except DashboardTheme.DoesNotExist:
            getDashboardTheme = None
        context.update({'getDashboardTheme': getDashboardTheme})

        # This theme layout helps to map the components to their position on the page
        layout = getDashboardTheme[0].layout_dictionary
        layoutList = ast.literal_eval(layout)
        getDashboardLayoutList = list(layoutList.items())
        context.update({'getDashboardLayoutList': getDashboardLayoutList})
        # getLayoutDictionary = "{"template_position": {"component_type":"bar_chart","component_assigned": "component_id"}}"
        # for item in getDashboardLayoutList:
        #     if !getDashboardLayoutList[item.0]:
        #         getLayoutDictionary[item.0]={"component_type":item.1, "component_assigned":""}
        #     else if getLayoutDictionary[item.0].component_type != item.1
        #         getLayoutDictionary[item.0]={"component_type":item.1, "component_assigned":""}
        # context.update({'getLayoutDictionary': getLayoutDictionary})

        try:
            getDashboardComponents = DashboardComponent.objects.all().filter(componentset=getCustomDashboard)
        except DashboardComponent.DoesNotExist:
            getDashboardComponents = None
        context.update({'getDashboardComponents': getDashboardComponents})

        try:
            getComponentDataSources = ComponentDataSource.objects.all()
        except ComponentDataSource.DoesNotExist:
            getComponentDataSources = None
        context.update({'getComponentDataSources': getComponentDataSources})

        mapped_location = self.request.GET.get('location')
        component_type = self.request.GET.get('type')
        if mapped_location and component_type:
            context.update({'mapped_location': mapped_location})
            context.update({'component_type': component_type})

        return context
        
        # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(CustomDashboardUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, self, fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        check_form_type = self.request.get_full_path()
        # if check_form_type.startswith('/activitydb/custom_dashboard_map'):
        #     getCustomDashboard.component_map = form.cleaned_data['component_map']
        #     getCustomDashboard.save()
            # for position in getCustomDashboard.component_map:
            #     mapped_position = form.component_map.0
            #     if position.0 == mapped_position:
            #         position.1 == form.component_map.1
            #         mapped = true
            # if mapped != true:
            #     getCustomDashboard.component_map.append(form.component_map)
        # else:
        form.save()
        messages.success(self.request, 'Success, CustomDashboard Output Updated!')

        return self.render_to_response(self.get_context_data(form=form))

class CustomDashboardDelete(AjaxableResponseMixin, DeleteView):
    """
    CustomDashboard Delete
    """
    model = CustomDashboard
    template_name = 'customdashboard/admin/customdashboard_confirm_delete.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CustomDashboardDelete, self).get_context_data(**kwargs)
        getCustomDashboard = CustomDashboard.objects.all().get(id=self.kwargs['pk'])
        pk=self.kwargs['pk']
        context.update({'pk': self.kwargs['pk']})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Dashboard Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = CustomDashboardForm     


class DashboardThemeList(ListView):
    model = CustomDashboard
    template_name = 'customdashboard/admin/dashboard_theme_list.html'

    def get(self, request, *args, **kwargs):
        getDashboardThemes = DashboardTheme.objects.all() 
        return render(request, self.template_name, {'getDashboardThemes': getDashboardThemes})

class DashboardThemeCreate(CreateView):
    model = DashboardTheme
    template_name = 'customdashboard/admin/dashboard_theme_form.html'

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(DashboardThemeCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="DashboardTheme")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(DashboardThemeCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardThemeCreate, self).get_context_data(**kwargs)

        return context 

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Theme Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DashboardThemeCreateForm 

class DashboardThemeUpdate(UpdateView):
    model = DashboardTheme
    template_name = 'customdashboard/admin/dashboard_theme_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        return super(DashboardThemeUpdate, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(DashboardThemeUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context.update({'pk': pk})
        getComplete = DashboardTheme.objects.get(id=self.kwargs['pk'])
        context.update({'getComplete': getComplete})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(DashboardThemeUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        self.object = form.save()

        messages.success(self.request, 'Success, form updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = DashboardThemeForm

class DashboardThemeDelete(DeleteView):
    """
    DashboardTheme Delete
    """
    model = DashboardTheme
    template_name = 'customdashboard/admin/dashboard_theme_confirm_delete.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(DashboardThemeDelete, self).get_context_data(**kwargs)
        context.update({'pk': self.kwargs['pk']})
        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Dashboard Theme Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DashboardThemeForm 

class DashboardComponentList(ListView):
    model = DashboardComponent
    template_name = 'customdashboard/admin/dashboard_component_list.html'

    def get(self, request, *args, **kwargs):
        ## retrieve program
        model = Program
        ## retrieve the countries the user has data access for
        countries = getCountry(request.user)
        dashboard_id = int(self.kwargs['pk'])
        
        getDashboardListComponents = DashboardComponent.objects.all().filter(componentset=dashboard_id)
            
        return render(request, self.template_name, {'getDashboardListComponents': getDashboardListComponents})

class DashboardComponentCreate(CreateView):
    model = DashboardComponent
    template_name = 'customdashboard/admin/dashboard_component_form.html'

     # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(DashboardComponentCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        id = self.kwargs['id']
        return kwargs

    @method_decorator(group_excluded('ViewOnly', url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            guidance = FormGuidance.objects.get(form="DashboardComponent")
        except FormGuidance.DoesNotExist:
            guidance = None
        return super(DashboardComponentCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = {
            'getCustomDashboard': CustomDashboard.objects.get(id=self.kwargs['id']),
            'getComponentDataSources': ComponentDataSource.objects.all(),
            }

    def get_context_data(self, **kwargs):
        context = super(DashboardComponentCreate, self).get_context_data(**kwargs)
        try:
            getCustomDashboard =CustomDashboard.objects.get(id=self.kwargs['id'])
        except CustomDashboard.DoesNotExist:
            getCustomDashboard = None
        context.update({'getCustomDashboard': getCustomDashboard})

        return context 

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        context = self.get_context_data()
        messages.success(self.request, 'Success, Component Created!')
        latestComponent = DashboardComponent.objects.latest('id')
        getCustomDashboard.componentset.add(latestComponent)
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DashboardComponentCreateForm 

class DashboardComponentUpdate(UpdateView):
    model = DashboardComponent
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        # try:
        #     guidance = FormGuidance.objects.get(form="DashboardComponentUpdate")
        # except FormGuidance.DoesNotExist:
        #     guidance = None
        return super(DashboardComponentUpdate, self).dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super(DashboardComponentUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context.update({'pk': pk})

        getComponentDataSources = []
        getComponentDataSources = ComponentDataSource.objects.all()
        context.update({'getComponentDataSources': getComponentDataSources})

        getDashboardComponent = DashboardComponent.objects.all().get(id=self.kwargs['pk'])
        context.update({'getDashboardComponent': getDashboardComponent})

        #for each component define the properties the component needs to have data mapped for by type
        #ideally this dictionary would be saved externally as a constant
        getComponentProperties = {
            'bar_graph':{'labels':'', 'data': '', 'colors':''}, 
            'doughnut': {'labels':'', 'data': '', 'colors':''}, 
            'line':{'labels':'', 'data': '', 'colors':''}, 
            'pie':{'labels':'', 'data': '', 'colors':''}, 
            'polar':{'labels':'', 'data': '', 'colors':''}, 
            'radar':{'labels':'', 'data': '', 'colors':''}, 
            'sidebar_gallery':{'photo_url':'', 'photo_titles':'', 'photo_captions':'', 'photo_dates':''}, 
            'content_map':{'latitude':'', 'longitude':'', 'location_name':'', 'description': '', 'region_link': '','region_name':''}, 
            'region_map':{'latitude':'', 'longitude':'', 'site_contact':'', 'location_name':'','description': ''}, 
            'sidebar_map':{'latitude':'', 'longitude':'', 'site_contact':'', 'location_name':'','description': ''}, 
            'context_pane':{}, 
            'sidebar_events':{}, 
            'sidebar_news':{},
            'sidebar_objectives':{}
        }
        context.update({'getComponentProperties': getComponentProperties})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(DashboardComponentUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        self.object = form.save()

        messages.success(self.request, 'Success, form updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = DashboardComponentForm


class DashboardComponentDelete(AjaxableResponseMixin, DeleteView):
    model = DashboardComponent
    template_name = 'customdashboard/admin/dashboard_component_confirm_delete.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(DashboardComponentDelete, self).get_context_data(**kwargs)
        context.update({'pk': self.kwargs['pk']})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Component Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DashboardComponentForm  

class ComponentDataSourceList(ListView):
    model = ComponentDataSource
    template_name = 'customdashboard/admin/component_data_source_list.html'

    def get(self, request, *args, **kwargs):
        getComponentDataSources = ComponentDataSource.objects.all()
            
        return render(request, self.template_name, {'getComponentDataSources': getComponentDataSources})

class ComponentDataSourceCreate(CreateView):
    model = ComponentDataSource
    template_name = 'customdashboard/admin/component_data_source_form.html'

     # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ComponentDataSourceCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        return super(ComponentDataSourceCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ComponentDataSourceCreate, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        context = self.get_context_data()
        messages.success(self.request, 'Success, Data Source Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = ComponentDataSourceCreateForm 


class ComponentDataSourceUpdate(UpdateView):
    model = ComponentDataSource
    template_name = 'customdashboard/admin/component_data_source_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            guidance = FormGuidance.objects.get(form="ComponentDataSource")
        except FormGuidance.DoesNotExist:
            guidance = None
        return super(ComponentDataSourceUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ComponentDataSourceUpdate, self).get_context_data(**kwargs)
        getComponentDataSource = ComponentDataSource.objects.all().get(id=self.kwargs['pk'])
        pk = self.kwargs['pk']
        context.update({'pk': pk})

        # get stuff
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ComponentDataSourceUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    #get shared data from project agreement and pre-populate form with it
    def get_initial(self):
        initial = {}
        return initial

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        self.object = form.save()

        messages.success(self.request, 'Success, form updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = ComponentDataSourceForm


class ComponentDataSourceDelete(AjaxableResponseMixin, DeleteView):    
    model = ComponentDataSource
    template_name = 'customdashboard/admin/component_data_source_confirm_delete.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ComponentDataSourceDelete, self).get_context_data(**kwargs)
        getDataSource = ComponentDataSource.objects.all().get(id=self.kwargs['pk'])
        pk=self.kwargs['pk']
        context.update({'pk': self.kwargs['pk']})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Component Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = ComponentDataSourceForm  
