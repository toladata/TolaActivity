from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import View, DetailView
from django.views.generic import TemplateView
from .models import ProgramDashboard, Program, Country, Province, Village, District, ProjectAgreement, ProjectComplete, SiteProfile, Documentation, Monitor, Benchmarks, TrainingAttendance, Beneficiary, Budget, ApprovalAuthority, Checklist, ChecklistItem, Stakeholder, Contact, FormLibrary, FormEnabled
from indicators.models import CollectedData, ExternalService
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
from .forms import ProgramDashboardForm, ProjectAgreementForm, ProjectAgreementCreateForm, ProjectCompleteForm, ProjectCompleteCreateForm, DocumentationForm, SiteProfileForm, MonitorForm, BenchmarkForm, TrainingAttendanceForm, BeneficiaryForm, BudgetForm, FilterForm, QuantitativeOutputsForm, ChecklistItemForm, StakeholderForm, ContactForm
import logging
from django.shortcuts import render
from django.contrib import messages
from django.db import connections
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.decorators import permission_required
from tables import ProjectAgreementTable
from django_tables2 import RequestConfig
from filters import ProjectAgreementFilter
from datetime import datetime
import json
import urllib2
import requests
from django.shortcuts import get_object_or_404

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect

# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from tola.util import getCountry, emailGroup
from mixins import AjaxableResponseMixin


def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def group_required(*group_names, **url):
    #Requires user membership in at least one of the groups passed in.
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)


class ProjectDash(ListView):

    template_name = 'activitydb/projectdashboard_list.html'

    def get(self, request, *args, **kwargs):
        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
        form = ProgramDashboardForm
        project_id = int(self.kwargs['pk'])

        if project_id == 0:
            getAgreement = None
            getComplete = None
            getChecklist = None
            getDocumentCount = 0
            getCommunityCount = 0
            getTrainingCount = 0
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
            getChecklistCount = ChecklistItem.objects.all().filter(checklist__agreement_id=self.kwargs['pk']).count()
            getChecklist = ChecklistItem.objects.all().filter(checklist__agreement_id=self.kwargs['pk'])


        if int(self.kwargs['pk']) == 0:
            getProgram =Program.objects.all().filter(funding_status="Funded", country__in=countries).distinct()
        else:
            getProgram =Program.objects.get(agreement__id=self.kwargs['pk'])

        return render(request, self.template_name, {'form': form, 'getProgram': getProgram, 'getAgreement': getAgreement,'getComplete': getComplete,
                                                    'getPrograms':getPrograms, 'getDocumentCount':getDocumentCount,'getChecklistCount': getChecklistCount,
                                                    'getCommunityCount':getCommunityCount, 'getTrainingCount':getTrainingCount, 'project_id': project_id, 'getChecklist': getChecklist})


class ProgramDash(ListView):
    """
    Dashboard links for and status for each program with number of projects
    :param request:
    :param pk: program_id
    :return:
    """
    template_name = 'activitydb/programdashboard_list.html'

    def get(self, request, *args, **kwargs):
        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries).distinct()

        if int(self.kwargs['pk']) == 0:
            getDashboard = Program.objects.all().select_related().filter(funding_status="Funded", country__in=countries).order_by('name').annotate(has_agreement=Count('agreement'),has_complete=Count('complete'))
        else:
            getDashboard = Program.objects.all().filter(id=self.kwargs['pk'], funding_status="Funded", country__in=countries).order_by('name')

        return render(request, self.template_name, {'getDashboard': getDashboard, 'getPrograms': getPrograms})


class ProjectAgreementList(ListView):
    """
    Project Agreement
    :param request:
    """
    model = ProjectAgreement
    template_name = 'activitydb/projectagreement_list.html'

    def get(self, request, *args, **kwargs):
        form = ProgramDashboardForm
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
    """
    model = ProjectAgreement
    template_name = 'activitydb/projectagreement_form.html'

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

        create_dashboard_entry = ProgramDashboard(program=getProgram, project_agreement=getAgreement)
        create_dashboard_entry.save()

        create_checklist = Checklist(agreement=getAgreement)
        create_checklist.save()

        get_checklist = Checklist.objects.get(id=create_checklist.id)
        get_globals = ChecklistItem.objects.all().filter(global_item=True)
        for item in get_globals:
            ChecklistItem.objects.create(checklist=get_checklist,item=item.item)

        messages.success(self.request, 'Success, Agreement Created!')
        redirect_url = '/activitydb/dashboard/project/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = ProjectAgreementCreateForm


class ProjectAgreementUpdate(UpdateView):
    """
    Project Agreement Form
    :param request:
    :param id: project_agreement_id
    """
    model = ProjectAgreement

    def get_context_data(self, **kwargs):
        context = super(ProjectAgreementUpdate, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context.update({'pk': pk})

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
            getBenchmark = Benchmarks.objects.all().filter(agreement__id=self.kwargs['pk']).order_by('percent_cumulative')
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

        #get the approval status of the form before it was submitted
        check_agreement_status = ProjectAgreement.objects.get(id=str(self.kwargs['pk']))
        is_approved = str(form.instance.approval)

        #check to see if the approval status has changed
        if str(is_approved) == "approved" and check_agreement_status.approval != "approved":
            getProgram = Program.objects.get(agreement__id=check_agreement_status.id)
            country = getProgram.country
            budget = form.instance.total_estimated_budget
            if getProgram.budget_check == True:
                try:
                    user_budget_approval = ApprovalAuthority.objects.get(approval_user=self.request.user)
                except ApprovalAuthority.DoesNotExist:
                    user_budget_approval = None
            #compare budget amount to users approval amounts

            if getProgram.budget_check:
                if not user_budget_approval or int(budget) > int(user_budget_approval.budget_limit):
                    messages.success(self.request, 'You do not appear to have permissions to approve this agreement')
                    form.instance.approval = 'awaiting approval'
                else:
                    messages.success(self.request, 'Success, Agreement and Budget Approved')
                    form.instance.approval = 'approved'
            else:
                messages.success(self.request, 'Success, Agreement Approved')
                form.instance.approval = 'approved'

            if form.instance.approval == 'approved':
                #email the approver group so they know this was approved
                link = "Link: " + "https://tola-activity.mercycorps.org/activitydb/projectagreement_update/" + str(self.kwargs['pk']) + "/"
                subject = "Project Agreement Approved: " + str(form.instance.project_name)
                message = "A new agreement was approved by " + str(self.request.user) + "\n" + "Budget Amount: " + str(form.instance.total_estimated_budget) + "\n"
                getSubmiter = User.objects.get(username=self.request.user)
                emailGroup(submiter=getSubmiter.email, country=country,group="Approver",link=link,subject=subject,message=message)
        elif str(is_approved) == "awaiting approval" and check_agreement_status.approval != "awaiting approval":
            messages.success(self.request, 'Success, Agreement has been saved and is now Awaiting Approval (Notifications have been Sent)')
            #email the approver group so they know this was approved
            link = "Link: " + "https://tola-activity.mercycorps.org/activitydb/projectagreement_update/" + str(self.kwargs['pk']) + "/"
            subject = "Project Agreement Waiting for Approval: " + str(form.instance.project_name)
            message = "A new agreement was submitted for approval by " + str(self.request.user) + "\n" + "Budget Amount: " + str(form.instance.total_estimated_budget) + "\n"
            emailGroup(country=country,group="Approver",link=link,subject=subject,message=message)
        else:
            messages.success(self.request, 'Success, form updated!')
        form.save()
        #save formset from context
        context = self.get_context_data()
        self.object = form.save()

        return self.render_to_response(self.get_context_data(form=form))

    form_class = ProjectAgreementForm


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

        return context


class ProjectAgreementDelete(DeleteView):
    """
    Project Agreement Delete
    """
    model = ProjectAgreement
    success_url = '/activitydb/projectagreement_list/0/'

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
        form = ProgramDashboardForm
        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

        if int(self.kwargs['pk']) == 0:
            getDashboard = ProjectComplete.objects.all().filter(program__country__in=countries)
            return render(request, self.template_name, {'form': form, 'getDashboard':getDashboard,'getPrograms':getPrograms})
        else:
            getDashboard = ProjectComplete.objects.all().filter(program__id=self.kwargs['pk'])
            getProgram =Program.objects.get(id=self.kwargs['pk'])

            return render(request, self.template_name, {'form': form, 'getProgram': getProgram, 'getDashboard':getDashboard,'getPrograms':getPrograms})


class ProjectCompleteCreate(CreateView):
    """
    Project Complete Form
    """
    model = ProjectComplete
    template_name = 'activitydb/projectcomplete_form.html'

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
            site = {'site': [o for o in getSites],}
            initial = pre_initial.copy()
            initial.update(site)
        except SiteProfile.DoesNotExist:
            getSites = None

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

        ProgramDashboard.objects.filter(project_agreement__id=self.request.POST['project_agreement']).update(project_completion=getComplete)

        #update the quantitative data fields to include the newly created complete
        CollectedData.objects.filter(agreement__id=getComplete.project_agreement_id).update(complete=getComplete)

        #update the other budget items
        Budget.objects.filter(agreement__id=getComplete.project_agreement_id).update(complete=getComplete)

        #update main compelte fields
        ProjectComplete.objects.filter(id=getComplete.id).update(account_code=getAgreement.account_code, lin_code=getAgreement.lin_code)


        messages.success(self.request, 'Success, Completion Form Created!')
        redirect_url = '/activitydb/projectcomplete_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = ProjectCompleteCreateForm


class ProjectCompleteUpdate(UpdateView):
    """
    Project Complete Form
    """
    model = ProjectComplete
    template_name = 'activitydb/projectcomplete_form.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectCompleteUpdate, self).get_context_data(**kwargs)
        getComplete = ProjectComplete.objects.get(id=self.kwargs['pk'])
        id = getComplete.project_agreement_id
        context.update({'id': id})
        pk = self.kwargs['pk']
        context.update({'pk': pk})

        #get budget data
        try:
            getBudget = Budget.objects.all().filter(complete__id=self.kwargs['pk'])
        except Budget.DoesNotExist:
            getBudget = None
        context.update({'getBudget': getBudget})

        #get Quantitative data
        try:
            getQuantitative = CollectedData.objects.all().filter(complete__id=self.kwargs['pk']).order_by('indicator')
        except CollectedData.DoesNotExist:
            getQuantitative = None
        context.update({'getQuantitative': getQuantitative})

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
        context = self.get_context_data()
        self.object = form.save()

        is_approved = self.request.GET.get('approved')

        if is_approved:
            update_dashboard = ProgramDashboard.objects.filter(project_completion__id=self.request.GET.get('id')).update(project_completion_approved=True)


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
        getData = serializers.serialize('python', data)
        #return just the fields and skip the object name
        justFields = [d['fields'] for d in getData]
        #temp name fiels
        jsonData =json.dumps(justFields, default=date_handler)
        context.update({'jsonData': jsonData})
        context.update({'id':self.kwargs['pk']})

        return context


class ProjectCompleteDelete(DeleteView):
    """
    Project Complete Delete
    """
    model = ProjectComplete
    success_url = '/activitydb/projectcomplete_list/0/'

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

        project_agreement_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            countries = getCountry(request.user)
            getDocumentation = Documentation.objects.all().filter(program__country__in=countries)
        else:
            getDocumentation = Documentation.objects.all().filter(project__id=self.kwargs['pk'])

        return render(request, self.template_name, {'getDocumentation':getDocumentation, 'project_agreement_id': project_agreement_id})


class DocumentationAgreementCreate(AjaxableResponseMixin, CreateView):
    """
    Documentation Form
    """
    model = Documentation
    template_name = 'activitydb/documentation_popup_form.html'

    def dispatch(self, request, *args, **kwargs):
        return super(DocumentationAgreementCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(DocumentationAgreementCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(DocumentationAgreementCreate, self).get_context_data(**kwargs)
        getProject = ProjectAgreement.objects.get(id=self.kwargs['id'])
        context.update({'project': getProject})
        context.update({'id': self.kwargs['id']})
        return context

    def get_initial(self):
        initial = {
            'project': self.kwargs['id'],
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

    def dispatch(self, request, *args, **kwargs):
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
    success_url = '/activitydb/documentation_list/0/'

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
        #Filter SiteProfile list and map by activity or program
        if activity_id != 0:
            getCommunity = SiteProfile.objects.all().filter(projectagreement__id=activity_id).distinct()
        elif program_id != 0:
            print "program"
            getCommunity = SiteProfile.objects.all().filter(Q(projectagreement__program__id=program_id)).distinct()
        else:
            getCommunity = SiteProfile.objects.all().filter(country__in=countries).distinct()

        if request.method == "GET" and "search" in request.GET:
            """
             fields = ('name', 'office')
            """
            getCommunity = SiteProfile.objects.all().filter(Q(country__in=countries), Q(name__contains=request.GET["search"]) | Q(office__name__contains=request.GET["search"]) | Q(type__profile__contains=request.GET['search']) |
                                                            Q(province__name__contains=request.GET["search"]) | Q(district__name__contains=request.GET["search"]) | Q(village__contains=request.GET['search']) |
                                                             Q(projectagreement__project_name__contains=request.GET["search"]) | Q(projectcomplete__project_name__contains=request.GET['search'])).select_related().distinct()

        return render(request, self.template_name, {'getCommunity':getCommunity,'project_agreement_id': activity_id,'country': countries,'getPrograms':getPrograms, 'form': FilterForm(), 'helper': FilterForm.helper})


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

    @method_decorator(group_required('Editor',url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
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

    def dispatch(self, request, *args, **kwargs):
        return super(BenchmarkCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BenchmarkCreate, self).get_context_data(**kwargs)
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
        messages.success(self.request, 'Success, Benchmark Created!')
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

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Benchmark Updated!')

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

        messages.success(self.request, 'Success, Benchmark Deleted!')
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

        if int(self.kwargs['pk']) == 0:
            countries=getCountry(request.user)
            getContacts = Contact.objects.all().filter(country__in=countries)
        else:
            getContacts = Contact.objects.all().filter(projectagreement=self.kwargs['pk'])

        return render(request, self.template_name, {'getContacts': getContacts})


class ContactCreate(CreateView):
    """
    Contact Form
    """
    model = Contact

    def dispatch(self, request, *args, **kwargs):
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

    def dispatch(self, request, *args, **kwargs):
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

        if int(self.kwargs['pk']) == 0:
            getTraining = TrainingAttendance.objects.all()
        else:
            getTraining = TrainingAttendance.objects.all().filter(project_agreement_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getTraining': getTraining, 'project_agreement_id': project_agreement_id})


class TrainingCreate(CreateView):
    """
    Training Form
    """
    model = TrainingAttendance

    def dispatch(self, request, *args, **kwargs):
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
    success_url = reverse_lazy('training_list')

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

        if int(self.kwargs['pk']) == 0:
            getBeneficiaries = Beneficiary.objects.all()
        else:
            getBeneficiaries = Beneficiary.objects.all().filter(training_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getBeneficiaries': getBeneficiaries, 'project_agreement_id': project_agreement_id})


class BeneficiaryCreate(CreateView):
    """
    Beneficiary Form
    """
    model = Beneficiary

    def dispatch(self, request, *args, **kwargs):
        return super(BeneficiaryCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = {
            'training': self.kwargs['id'],
            }

        return initial

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
    success_url = reverse_lazy('training_list')

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Beneficiary Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = BeneficiaryForm


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

    def get_context_data(self, **kwargs):
        context = super(ChecklistItemCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ChecklistItemCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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


def checklist_update_link(request,pk,type,value):
    """
    Checklist Update from Link To Update if a Task is Done
    """
    value = int(value)

    if type == "in_file":
        update = ChecklistItem.objects.filter(id=pk).update(in_file=value)
    elif type == "not_applicable":
        update = ChecklistItem.objects.filter(id=pk).update(not_applicable=value)


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ChecklistItemDelete(DeleteView):
    """
    Checklist Delete
    """
    model = ChecklistItem
    success_url = '/'


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


class FormLibraryList(ListView):
    """
    List of all available forms and what forms are enabled for a project
    """
    model = FormLibrary
    template_name = 'activitydb/formlibrary_list.html'

    def get(self, request, *args, **kwargs):

        project_agreement_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getForms = FormLibrary.objects.all()
            getAgreementForms = None
        else:
            getForms = FormLibrary.objects.all()
            getAgreementForms = FormEnabled.objects.all().filter(agreement_id=self.kwargs['pk'])


        return render(request, self.template_name, {'getForms': getForms,'getAgreementForms': getAgreementForms,'project_agreement_id': project_agreement_id})


def report(request):
    """
    Show LIST of submitted incidents with a filtered search view using django-tables2
    and django-filter
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
        queryset = ProjectAgreement.objects.filter(
                                           Q(project_name__contains=request.GET["search"]) |
                                           Q(activity_code__contains=request.GET["search"]))
        table = ProjectAgreementTable(queryset)

    RequestConfig(request).configure(table)

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
    village = Village.objects.all().filter(district=selected_district)
    villages_json = serializers.serialize("json", village)
    return HttpResponse(villages_json, content_type="application/json")


def import_service(service_id=1, deserialize=True):
    """
    Import a indicators from a web service (the dig only for now)
    """
    service = ExternalService.objects.all().filter(id=service_id)

    response = requests.get(services.feed_url)
    get_json = json.loads(response.content)

    if deserialize == True:
        data = json.load(get_json) # deserialises it
    else:
        #send json data back not deserialized data
        data = get_json
    #debug the json data string uncomment dump and print
    data2 = json.dumps(data) # json formatted string
    print data2
    print "HELP!"

    return data


def service_json(request, service):
    """
    For populating service indicators in dropdown
    """
    service_indicators = import_service(service,deserialize=False)
    return HttpResponse(service_indicators, content_type="application/json")