from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import View, DetailView
from django.views.generic import TemplateView
from .models import ProgramDashboard, Program, Country, Province, Village, District, ProjectAgreement, ProjectComplete, Community, Documentation, Monitor, Benchmarks, TrainingAttendance, Beneficiary, Budget, ApprovalAuthority, Checklist, ChecklistItem
from indicators.models import CollectedData
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
from .forms import ProgramDashboardForm, ProjectAgreementForm, ProjectAgreementCreateForm, ProjectCompleteForm, ProjectCompleteCreateForm, DocumentationForm, CommunityForm, MonitorForm, BenchmarkForm, TrainingAttendanceForm, BeneficiaryForm, BudgetForm, FilterForm, QuantitativeOutputsForm, ChecklistForm
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
from tola.util import getCountry, getTolaDataSilos, emailGroup
from mixins import AjaxableResponseMixin
"""
project_agreement_id is the key to link each related form
 ProjectAgreement, ProjectComplete, Community (Main Forms and Workflow)
Monitor, Benchmark, TrainingAttendance and Beneficiary are related to Project Agreement via
the project_agreement_id

"""


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

        if int(self.kwargs['pk']) == 0:
            getAgreement = ProjectAgreement.objects.all()
            getComplete = ProjectComplete.objects.all()
            getDocumentCount = 0
            getCommunityCount = 0
            getTrainingCount = 0
        else:
            getAgreement = ProjectAgreement.objects.get(id=self.kwargs['pk'])
            try:
                getComplete = ProjectComplete.objects.get(project_agreement__id=self.kwargs['pk'])
            except ProjectComplete.DoesNotExist:
                getComplete = None
            getDocumentCount = Documentation.objects.all().filter(project_id=self.kwargs['pk']).count()
            getCommunityCount = Community.objects.all().filter(projectagreement__id=self.kwargs['pk']).count()
            getTrainingCount = TrainingAttendance.objects.all().filter(project_agreement_id=self.kwargs['pk']).count()
            getChecklistCount = Checklist.objects.all().filter(agreement_id=self.kwargs['pk']).count()


        if int(self.kwargs['pk']) == 0:
            getProgram =Program.objects.all().filter(funding_status="Funded", country__in=countries)
        else:
            getProgram =Program.objects.get(agreement__id=self.kwargs['pk'])

        return render(request, self.template_name, {'form': form, 'getProgram': getProgram, 'getAgreement': getAgreement,'getComplete': getComplete,
                                                    'getPrograms':getPrograms, 'getDocumentCount':getDocumentCount,'getChecklistCount': getChecklistCount,
                                                    'getCommunityCount':getCommunityCount, 'getTrainingCount':getTrainingCount})


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
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

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
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

        if int(self.kwargs['pk']) == 0:
            getDashboard = ProjectAgreement.objects.all()
            return render(request, self.template_name, {'form': form, 'getDashboard':getDashboard,'getPrograms':getPrograms})
        else:
            getDashboard = ProjectAgreement.objects.all().filter(program__id=self.kwargs['pk'])
            getProgram =Program.objects.get(id=self.kwargs['pk'])

            return render(request, self.template_name, {'form': form, 'getProgram': getProgram, 'getDashboard':getDashboard,'getPrograms':getPrograms})


class ProjectAgreementImport(ListView):
    """
    Import a project agreement from TolaData
    """

    template_name = 'activitydb/projectagreement_import.html'

    def get(self, request, *args, **kwargs):

        # set url for json feed here
        response = requests.get("https://tola-data-dev.mercycorps.org/api/read/?format=json")
        jsondata = json.loads(response.content)

        data = jsondata['results']


        return render(request, self.template_name, {'getAgreements': data})


class ProjectAgreementCreate(CreateView):
    """
    Project Agreement Form
    :param request:
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

        messages.success(self.request, 'Success, Agreement Created!')
        redirect_url = '/activitydb/projectagreement_update/' + str(latest.id)
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

        check_agreement_status = ProjectAgreement.objects.get(id=str(self.kwargs['pk']))
        is_approved = str(form.instance.approval)
        print check_agreement_status.approval
        print is_approved
        #check to see if the approval status has changed
        if str(is_approved) is "approved" and check_agreement_status.approval is not "approved":
            budget = form.instance.total_estimated_budget
            try:
                user_budget_approval = ApprovalAuthority.objects.get(approval_user=self.request.user)
            except ApprovalAuthority.DoesNotExist:
                user_budget_approval = None
            #compare budget amount to users approval amounts
            print "has approval="
            print user_budget_approval
            print " approval amount = "
            print budget
            print "budget limit = "
            print user_budget_approval.budget_limit
            if not user_budget_approval or int(budget) > int(user_budget_approval.budget_limit):
                messages.success(self.request, 'You do not appear to have permissions to approve this agreement')
                form.instance.approval = 'awaiting approval'
            else:
                messages.success(self.request, 'Success, Agreement and Budget Approved')
                #email the approver group so they know this was approved
                link = "Link: " + "https://tola-activity.mercycorps.org/activitydb/projectagreement_update/" + str(self.kwargs['pk']) + "/"
                subject = "Project Agreement Approved: " + str(form.instance.project_name)
                message = "A new agreement was approved by " + str(self.request.user) + "\n" + "Budget Amount: " + str(form.instance.total_estimated_budget) + "\n"
                emailGroup(group="Approver",link=link,subject=subject,message=message)
                form.instance.approval = 'approved'
        elif str(is_approved) is "awaiting approval" and check_agreement_status.approval is not "awaiting approval":
                messages.success(self.request, 'Success, Agreement has been saved and is now Awaiting Approval (Notifications have been Sent)')
                #email the approver group so they know this was approved
                link = "Link: " + "https://tola-activity.mercycorps.org/activitydb/projectagreement_update/" + str(self.kwargs['pk']) + "/"
                subject = "Project Agreement Waiting for Approval: " + str(form.instance.project_name)
                message = "A new agreement was submitted for approval by " + str(self.request.user) + "\n" + "Budget Amount: " + str(form.instance.total_estimated_budget) + "\n"
                emailGroup(group="Approver",link=link,subject=subject,message=message)
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
            getDashboard = ProjectComplete.objects.all()
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
            'project_agreement': getProjectAgreement.id,
            'project_name': getProjectAgreement.project_name,
            'activity_code': getProjectAgreement.activity_code,
            'expected_start_date': getProjectAgreement.expected_start_date,
            'expected_end_date': getProjectAgreement.expected_end_date,
            'expected_duration': getProjectAgreement.expected_duration,
            'estimated_budget': getProjectAgreement.total_estimated_budget,
        }

        try:
            getCommunites = Community.objects.filter(projectagreement__id=getProjectAgreement.id).values_list('id',flat=True)
            communites = {'community': [o for o in getCommunites],}
            initial = pre_initial.copy()
            initial.update(communites)
        except Community.DoesNotExist:
            getCommunites = None

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

        ProgramDashboard.objects.filter(project_agreement__id=self.request.POST['project_agreement']).update(project_completion=getComplete)

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
            getBudget = Budget.objects.all().filter(agreement__id=self.kwargs['pk'])
        except Budget.DoesNotExist:
            getBudget = None
        context.update({'getBudget': getBudget})

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
            getDocumentation = Documentation.objects.all()
        else:
            getDocumentation = Documentation.objects.all().filter(project__id=self.kwargs['pk'])

        return render(request, self.template_name, {'getDocumentation':getDocumentation, 'project_agreement_id': project_agreement_id})


class DocumentationCreate(CreateView):
    """
    Documentation Form
    """
    model = Documentation

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Documentation Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


class DocumentationUpdate(UpdateView):
    """
    Documentation Form
    """
    model = Documentation

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
    success_url = reverse_lazy('documentation_list')

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Documentation Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DocumentationForm


class CommunityList(ListView):
    """
    Community list creates a map and list of communites by user country access and filters
    by either direct link from project or by program dropdown filter
    """
    model = Community
    template_name = 'activitydb/community_list.html'

    def dispatch(self, request, *args, **kwargs):
        if request.GET.has_key('report'):
            template_name = 'activitydb/community_report.html'
        else:
            template_name = 'activitydb/community_list.html'
        return super(CommunityList, self).dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        countries = getCountry(request.user)
        activity_id = int(self.kwargs['activity_id'])
        program_id = int(self.kwargs['program_id'])

        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
        #Filter Community list and map by activity or program
        if activity_id != 0:
            getCommunity = Community.objects.all().filter(projectagreement__id=activity_id).distinct()
        elif program_id != 0:
            print "program"
            getCommunity = Community.objects.all().filter(Q(projectagreement__program__id=program_id)).distinct()
        else:
            getCommunity = Community.objects.all().distinct()

        if request.method == "GET" and "search" in request.GET:
            """
             fields = ('name', 'office')
            """
            getCommunity = Community.objects.all().filter(Q(name__contains=request.GET["search"]) | Q(office__name__contains=request.GET["search"]) | Q(type__profile__contains=request.GET['search']) |
                                                            Q(province__name__contains=request.GET["search"]) | Q(district__name__contains=request.GET["search"]) | Q(village__contains=request.GET['search']) |
                                                             Q(projectagreement__project_name__contains=request.GET["search"]) | Q(projectcomplete__project_name__contains=request.GET['search'])).select_related().distinct()

        return render(request, self.template_name, {'getCommunity':getCommunity,'project_agreement_id': activity_id,'country': countries,'getPrograms':getPrograms, 'form': FilterForm(), 'helper': FilterForm.helper})


class CommunityReport(ListView):
    """
    Community Report filtered by project
    """
    model = Community
    template_name = 'activitydb/community_report.html'


    def get(self, request, *args, **kwargs):
        countries = getCountry(request.user)
        project_agreement_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getCommunity = Community.objects.all()
        else:
            getCommunity = Community.objects.all().filter(projectagreement__id=self.kwargs['pk'])

        id=self.kwargs['pk']

        return render(request, self.template_name, {'getCommunity':getCommunity,'project_agreement_id': project_agreement_id,'id':id,'country': countries})


class CommunityCreate(CreateView):
    """
    Community Form create a new community
    """
    model = Community

    @method_decorator(group_required('Editor',url='activitydb/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(CommunityCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(CommunityCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_initial(self):
        initial = {
            'approved_by': self.request.user,
            'filled_by': self.request.user,
        }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Community Created!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = CommunityForm


class CommunityUpdate(UpdateView):
    """
    Community Form Update an existing community
    """
    model = Community

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(CommunityUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CommunityUpdate, self).get_context_data(**kwargs)
        getProjects = ProjectAgreement.objects.all().filter(community__id=self.kwargs['pk'])
        context.update({'getProjects': getProjects})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Community Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = CommunityForm


class CommunityDelete(DeleteView):
    """
    Community Form Delete an existing community
    """
    model = Community
    success_url = reverse_lazy('community_list',args='0')

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Community Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = CommunityForm


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
        return self.render_to_response(self.get_context_data(form=form))

    form_class = TrainingAttendanceForm


class TrainingUpdate(UpdateView):
    """
    Training Form
    """
    model = TrainingAttendance

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
        return self.render_to_response(self.get_context_data(form=form))

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


class QuantitativeOutputsList(ListView):
    """
    QuantitativeOutput List
    """
    model = CollectedData
    template_name = 'activitydb/quantitative_list.html'

    def get(self, request, *args, **kwargs):

        project_proposal_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getQuantitativeOutputs = QuantitativeOutputs.objects.all()
        else:
            getQuantitativeOutputs = QuantitativeOutputs.objects.all().filter(project_proposal_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getQuantitativeOutputs': getQuantitativeOutputs, 'project_proposal_id': project_proposal_id})


class QuantitativeOutputsCreate(AjaxableResponseMixin, CreateView):
    """
    QuantitativeOutput Form
    """
    model = CollectedData
    template_name = 'activitydb/quantitativeoutputs_form.html'
    def get_context_data(self, **kwargs):
        context = super(QuantitativeOutputsCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(QuantitativeOutputsCreate, self).dispatch(request, *args, **kwargs)

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


class ChecklistList(ListView):
    """
    Checklist List
    """
    model = Checklist
    template_name = 'activitydb/checklist_list.html'

    def get(self, request, *args, **kwargs):

        project_agreement_id = self.kwargs['pk']

        if int(self.kwargs['pk']) == 0:
            getChecklist = Checklist.objects.all()
        else:
            getChecklist = Checklist.objects.all().filter(agreement_id=self.kwargs['pk'])

        return render(request, self.template_name, {'getChecklist': getChecklist, 'project_agreement_id': self.kwargs['pk']})


class ChecklistCreate(CreateView):
    """
    Checklist Form
    """
    model = Checklist

    def get_context_data(self, **kwargs):
        context = super(ChecklistCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ChecklistCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        return super(ChecklistCreate, self).dispatch(request, *args, **kwargs)

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
        messages.success(self.request, 'Success, Checklist Created!')
        form = ""
        return self.render_to_response(self.get_context_data(form=form))


    form_class = ChecklistForm


class ChecklistUpdate(UpdateView):
    """
    Checklist Form
    """
    model = Checklist

    def get_context_data(self, **kwargs):
        context = super(ChecklistUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ChecklistCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Checklist Output Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = ChecklistForm


class ChecklistDelete(DeleteView):
    """
    Checklist Delete
    """
    model = Checklist
    success_url = '/'


    def get_context_data(self, **kwargs):
        context = super(ChecklistDelete, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Checklist Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = ChecklistForm


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

def ProgramDashboardCounts(request):
    """
    Loop over each program and increment that count for completes and
    regular program, agreements and completes
    :param request:
    :return:
    """
    getDashboard = ProgramDashboard.objects.all()

    for program in getDashboard:
        getAgreementOpen = ProjectAgreement.objects.all().filter(id=program.id).count()
        getAgreementApproved = ProjectAgreement.objects.all().filter(id=program.id,approval='approved').count()
        getCompleteOpen = ProjectComplete.objects.all().filter(id=program.id).count()
        getCompleteApproved = ProjectComplete.objects.all().filter(id=program.id,approval='approved').count()

        ProgramDashboard.objects.filter(id=program.id).update(
                                                              project_agreement_count=getAgreementOpen,
                                                              project_agreement_count_approved=getAgreementApproved,
                                                              project_completion_count=getCompleteOpen,
                                                              project_completion_count_approved=getCompleteApproved,
                                                              )
    return HttpResponseRedirect('/')
