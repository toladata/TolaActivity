from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import TrainingAttendance, Beneficiary, Distribution
from django.core.urlresolvers import reverse_lazy

from .forms import TrainingAttendanceForm, BeneficiaryForm, DistributionForm
from workflow.models import FormGuidance, WorkflowLevel1, WorkflowLevel2
from django.utils.decorators import method_decorator
from tola.util import getCountry, group_excluded

from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q

from django.http import  HttpResponseRedirect, JsonResponse
from django.views.generic.detail import View
from mixins import AjaxableResponseMixin
import json
from django.core.serializers.json import DjangoJSONEncoder


class TrainingList(ListView):
    """
    Training Attendance
    """
    model = TrainingAttendance
    template_name = 'formlibrary/training_list.html'

    def get(self, request, *args, **kwargs):

        project_agreement_id = self.kwargs['pk']
        countries = getCountry(request.user)
        getworkflowlevel1s = WorkflowLevel1.objects.all().filter(country__in=countries).distinct()
        if int(self.kwargs['pk']) == 0:
            getTraining = TrainingAttendance.objects.all().filter(workflowlevel1__country__in=countries)
        else:
            getTraining = TrainingAttendance.objects.all().filter(project_agreement_id=self.kwargs['pk'])

        return render(request, self.template_name, \
                      {'getTraining': getTraining, \
                      'project_agreement_id': project_agreement_id, \
                      'getworkflowlevel1s': getworkflowlevel1s})


class TrainingCreate(CreateView):
    """
    Training Form
    """
    model = TrainingAttendance

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
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
        redirect_url = '/formlibrary/training_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = TrainingAttendanceForm


class TrainingUpdate(UpdateView):
    """
    Training Form
    """
    model = TrainingAttendance

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
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
    success_url = '/formlibrary/training_list/0/'
    template_name = 'formlibrary/training_confirm_delete.html'

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
    template_name = 'formlibrary/beneficiary_list.html'

    def get(self, request, *args, **kwargs):

        project_agreement_id = self.kwargs['pk']
        countries = getCountry(request.user)
        getworkflowlevel1s = WorkflowLevel1.objects.all().filter(country__in=countries).distinct()


        if int(self.kwargs['pk']) == 0:
            getBeneficiaries = Beneficiary.objects.all().filter(\
                Q(training__workflowlevel1__country__in=countries) | \
                Q(distribution__workflowlevel1__country__in=countries) )
        else:
            getBeneficiaries = Beneficiary.objects.all().filter(training__id=self.kwargs['pk'])

        return render(request, self.template_name, \
                {'getBeneficiaries': getBeneficiaries, 'project_agreement_id': project_agreement_id, \
                'getworkflowlevel1s': getworkflowlevel1s})


class BeneficiaryCreate(CreateView):
    """
    Beneficiary Form
    """
    model = Beneficiary

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
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
        redirect_url = '/formlibrary/beneficiary_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = BeneficiaryForm


class BeneficiaryUpdate(UpdateView):
    """
    Training Form
    """
    model = Beneficiary

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
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

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
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
    template_name = 'formlibrary/distribution_list.html'

    def get(self, request, *args, **kwargs):

        workflowlevel1_id = self.kwargs['pk']
        countries = getCountry(request.user)
        getworkflowlevel1s = WorkflowLevel1.objects.all().filter(country__in=countries).distinct()

        if int(self.kwargs['pk']) == 0:
            getDistribution = Distribution.objects.all().filter(workflowlevel1__country__in=countries)
        else:
            getDistribution = Distribution.objects.all().filter(workflowlevel1_id=self.kwargs['pk'])

        return render(request, self.template_name, \
                    {'getDistribution': getDistribution, \
                    'workflowlevel1_id': workflowlevel1_id, \
                    'getworkflowlevel1s': getworkflowlevel1s})


class DistributionCreate(CreateView):
    """
    Distribution Form
    """
    model = Distribution

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
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
            'workflowlevel1': self.kwargs['id']
            }

        return initial

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Distribution Created!')
        latest = Distribution.objects.latest('id')
        redirect_url = '/formlibrary/distribution_update/' + str(latest.id)
        return HttpResponseRedirect(redirect_url)

    form_class = DistributionForm


class DistributionUpdate(UpdateView):
    """
    Distribution Form
    """
    model = Distribution

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
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
    success_url = '/formlibrary/distribution_list/0/'
    template_name = 'formlibrary/distribution_confirm_delete.html'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Distribution Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = DistributionForm

#Ajax views for ajax filters and paginators
class TrainingListObjects(View, AjaxableResponseMixin):

    def get(self, request, *args, **kwargs):

        workflowlevel1_id = int(self.kwargs['workflowlevel1'])
        project_id = int(self.kwargs['workflowlevel2'])
        print project_id
        countries = getCountry(request.user)
        if int(self.kwargs['workflowlevel1']) == 0:
            getTraining = TrainingAttendance.objects.all()\
                .filter(workflowlevel1__country__in=countries)\
                .values('id', 'create_date', 'training_name', 'workflowlevel2__name')
        elif workflowlevel1_id != 0 and project_id == 0:
            getTraining = TrainingAttendance.objects.all()\
                .filter(workflowlevel1=workflowlevel1_id)\
                .values('id','create_date', 'training_name', 'workflowlevel2__name')
        else:
            getTraining = TrainingAttendance.objects.all()\
                .filter(workflowlevel1_id=workflowlevel1_id, project_agreement_id=project_id)\
                .values('id','create_date', 'training_name', 'workflowlevel2__name')

        getTraining = json.dumps(list(getTraining), cls=DjangoJSONEncoder)

        final_dict = {'getTraining': getTraining}

        return JsonResponse(final_dict, safe=False)


class BeneficiaryListObjects(View, AjaxableResponseMixin):

    def get(self, request, *args, **kwargs):

        workflowlevel1_id = int(self.kwargs['workflowlevel1'])
        project_id = int(self.kwargs['workflowlevel2'])
        countries = getCountry(request.user)

        if workflowlevel1_id == 0:
            getBeneficiaries = Beneficiary.objects.all().filter(
                    Q(training__workflowlevel1__country__in=countries) | \
                    Q(distribution__workflowlevel1__country__in=countries) )\
                .values('id', 'beneficiary_name', 'create_date')
        elif workflowlevel1_id !=0 and project_id == 0:
            getBeneficiaries = Beneficiary.objects.all()\
                .filter(workflowlevel1__id=workflowlevel1_id)\
                .values('id', 'beneficiary_name', 'create_date')
        else:
            getBeneficiaries = Beneficiary.objects.all()\
                .filter(workflowlevel1__id=workflowlevel1_id, training__project_agreement=project_id)\
                .values('id', 'beneficiary_name', 'create_date')

        getBeneficiaries = json.dumps(list(getBeneficiaries), cls=DjangoJSONEncoder)

        final_dict = {'getBeneficiaries': getBeneficiaries}

        return JsonResponse(final_dict, safe=False)

class DistributionListObjects(View, AjaxableResponseMixin):

    def get(self, request, *args, **kwargs):

        workflowlevel1_id = int(self.kwargs['workflowlevel1'])
        project_id = int(self.kwargs['workflowlevel2'])
        countries = getCountry(request.user)
        if workflowlevel1_id == 0:
            getDistribution = Distribution.objects.all()\
                .filter(workflowlevel1__country__in=countries)\
                .values('id', 'distribution_name', 'create_date', 'workflowlevel1')
        elif workflowlevel1_id !=0 and project_id == 0:
            getDistribution = Distribution.objects.all()\
                .filter(workflowlevel1_id=workflowlevel1_id)\
                .values('id', 'distribution_name', 'create_date', 'workflowlevel1')
        else:
            getDistribution = Distribution.objects.all()\
                .filter(workflowlevel1_id=workflowlevel1_id, initiation_id=project_id)\
                .values('id', 'distribution_name', 'create_date', 'workflowlevel1')


        getDistribution = json.dumps(list(getDistribution), cls=DjangoJSONEncoder)

        final_dict = {'getDistribution': getDistribution}

        return JsonResponse(final_dict, safe=False)


#workflowlevel1 and project & training filters
class GetAgreements(View, AjaxableResponseMixin):

    def get(self, request, *args, **kwargs):

        workflowlevel1_id = self.kwargs['workflowlevel1']
        countries = getCountry(request.user)
        if workflowlevel1_id != 0:
            getAgreements = WorkflowLevel2.objects.all().filter(workflowlevel1=workflowlevel1_id).values('id', 'name')
        else:
            pass

        final_dict = {}
        if getAgreements:

            getAgreements = json.dumps(list(getAgreements), cls=DjangoJSONEncoder)

            final_dict = {'getAgreements': getAgreements}

        return JsonResponse(final_dict, safe=False)


from models import BinaryField
from serializers import BinaryFieldSerializer, BinaryFieldImageSerializer
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import base64


class BinaryFieldViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing or retrieving users.
    """
    queryset = BinaryField.objects.all()
    serializer_class = BinaryFieldSerializer

    def retrieve(self, request, pk=None):
        queryset = BinaryField.objects.all()
        field = get_object_or_404(queryset, pk=pk)
        serializer = BinaryFieldImageSerializer(instance=field, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """
        Override create method for POST requests to save binary files to database
        :param request:
        :return:
        """
        d = base64.b64decode(request.data["data"])
        b = BinaryField(name=request.data["name"], data=d)
        b.save()
        #headers = self.get_success_headers(serializer.data)
        b.data = None
        return Response(self.get_serializer(b).data, status=status.HTTP_201_CREATED) #, headers=headers


from django.http import HttpResponse
@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def binary_test(request, id):

    if request.method == 'GET':
        bfield = BinaryField.objects.get(id=id)
        return HttpResponse(bfield.data, content_type="image/png")
