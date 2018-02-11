from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset, Field
from django.forms import HiddenInput
from functools import partial
from widgets import GoogleMapsWidget
from django import forms
from .models import WorkflowLevel1, WorkflowLevel2, SiteProfile, Documentation, Budget, ApprovalWorkflow, \
    Office, ChecklistItem, AdminLevelOne, Stakeholder, TolaUser, Contact, Sector
from indicators.models import CollectedData, Indicator
from crispy_forms.layout import LayoutObject, TEMPLATE_PACK
from tola.util import getCountry


#Global for approvals
APPROVALS=(
        ('in progress', 'in progress'),
        ('awaiting approval', 'awaiting approval'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
    )


#Global for Budget Variance
BUDGET_VARIANCE=(
        ("Over Budget", "Over Budget"),
        ("Under Budget", "Under Budget"),
        ("No Variance", "No Variance"),
    )


class Formset(LayoutObject):
    """
    Layout object. It renders an entire formset, as though it were a Field.

    Example::

    Formset("attached_files_formset")
    """

    def __init__(self, formset_name_in_context, *fields, **kwargs):
        self.fields = []
        self.formset_name_in_context = formset_name_in_context
        self.label_class = kwargs.pop('label_class', u'blockLabel')
        self.css_class = kwargs.pop('css_class', u'ctrlHolder')
        self.css_id = kwargs.pop('css_id', None)
        self.flat_attrs = flatatt(kwargs)
        self.template = "formset.html"
        self.helper = FormHelper()
        self.helper.form_tag = False

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):

        form_class = 'form-horizontal'

        return render_to_string(self.template, Context({'wrapper': self, 'formset': self.formset_name_in_context, 'form_class': form_class}))


class DatePicker(forms.DateInput):
    """
    Use in form to create a Jquery datepicker element
    """
    template_name = 'datepicker.html'

    DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class BudgetForm(forms.ModelForm):

    class Meta:
        model = Budget
        exclude = ['create_date', 'edit_date']

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request')
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('contributor', required=False), Field('description_of_contribution', required=False), PrependedAppendedText('proposed_value','$', '.00'), 'workflowlevel2',
        )


        super(BudgetForm, self).__init__(*args, **kwargs)
        self.fields['workflowlevel2'].widget = forms.HiddenInput()#TextInput()

        #countries = getCountry(self.request.user)

        #self.fields['agreement'].queryset = ProjectAgreement.objects.filter(program__country__in = countries)

    def save(self, *args, **kwargs):
        # Commit is already set to false
        obj = super(BudgetForm, self).save(*args, **kwargs)
        return obj


class ApprovalForm(forms.ModelForm):

    class Meta:
        model = ApprovalWorkflow
        exclude = ['create_date', 'edit_date']

    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request')
        self.section = kwargs.pop('section', None)
        self.id = kwargs.pop('id')
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_tag = False

        super(ApprovalForm, self).__init__(*args, **kwargs)

        self.fields['status'].widget = forms.HiddenInput()
        self.fields['date_assigned'].widget = forms.HiddenInput()
        self.fields['date_approved'].widget = forms.HiddenInput()
        # hide the section field and set value from originating form
        self.fields["section"].widget = forms.HiddenInput()
        self.fields["section"].initial = self.section
        if self.section == "workflow2":
            workflow2 = forms.HiddenInput().initial = self.id
            self.fields += workflow2


    def save(self, *args, **kwargs):
        # Commit is already set to false
        obj = super(ApprovalForm, self).save(*args, **kwargs)
        return obj


class WorkflowLevel1Form(forms.ModelForm):
    class Meta:
        model = WorkflowLevel1
        exclude = ['create_date','edit_date','unique_id','level1_uuid']

    start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_tag = False

        super(WorkflowLevel1Form, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Commit is already set to false
        obj = super(WorkflowLevel1Form, self).save(*args, **kwargs)
        return obj


class WorkflowLevel2CreateForm(forms.ModelForm):

    class Meta:
        model = WorkflowLevel2
        fields = ("workflowlevel1","sector","name")

    def __init__(self, *args, **kwargs):

        #get the user object from request to check permissions
        self.request = kwargs.pop('request')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_tag = True
        super(WorkflowLevel2CreateForm, self).__init__(*args, **kwargs)


class WorkflowLevel2Form(forms.ModelForm):

    class Meta:
        model = WorkflowLevel2
        fields = '__all__'

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    expected_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    expected_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_cost_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    exchange_rate_date = forms.DateField(widget=DatePicker.DateInput(), required=False)


    approval = forms.ChoiceField(
        choices=APPROVALS,
        initial='in progress',
        required=False,
    )

    budget_variance = forms.ChoiceField(
        choices=BUDGET_VARIANCE,
        initial='Over Budget',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        #get the user object from request to check permissions
        self.request = kwargs.pop('request')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Executive Summary',
                    Fieldset('', 'workflowlevel1',\
                             'office', 'sector','name', 'site', 'stakeholder',
                        ),
                    Fieldset(
                        'Dates',
                        'expected_start_date','expected_end_date', 'actual_start_date', 'actual_end_date',
                        'no_explanation',

                        ),

                    Fieldset("Codes",
                         HTML("""
                                <fieldset>
                                  {% if getCodedField %}
                                        {% for item in getCodedField %}
                                        <div id='div_id_name' class="form-group">
                                            <label for="{{ item.label }}" class="control-label col-sm-2">{{ item.label }}</label>
                                            <input type="text" value="{{ item.default_value }}" name="{{ item.name }}">
                                        {% endfor %}
                                      </table>
                                  {% endif %}
                                </fieldset>
                        """),
                    ),
                ),

                Tab('Budget',
                    Fieldset(
                        '',
                        PrependedAppendedText('estimated_budget','$', '.00'), PrependedAppendedText('actual_cost','$', '.00'),'actual_cost_date', 'budget_variance', 'explanation_of_variance',
                        PrependedAppendedText('total_cost','$', '.00'), PrependedAppendedText('agency_cost','$', '.00'),
                        AppendedText('local_total_cost', '.00'), AppendedText('local_agency_cost', '.00'),'exchange_rate','exchange_rate_date',
                    ),

                ),
                Tab('Budget Other',
                    Fieldset("Other Budget Contributions:",
                        Div(
                                "",
                                HTML("""

                                    <div class='panel panel-default'>
                                      <!-- Default panel contents -->
                                      <div class='panel-heading'>Budget Contributions</div>
                                      <!-- Table -->
                                      <table class="table" id="budget_contributions_table">
                                      <tbody>
                                      {% if getBudget %}
                                            <tr>
                                            <th>Contributor</th>
                                            <th>Description</th>
                                            <th>Value</th>
                                            <th>View</th>
                                            </tr>
                                            {% for item in getBudget %}
                                            <tr>
                                                <td>{{ item.contributor}}</td>
                                                <td>{{ item.contributor_description}}</td>
                                                <td>{{ item.proposed_value}}</td>
                                                <td><a class="output" data-toggle="modal" data-target="#myModal" href='/workflow/budget_update/{{ item.id }}/'>View</a> | <a class="output" href='/workflow/budget_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal" >Delete</a>
                                            </tr>
                                            {% endfor %}
                                      {% endif %}
                                      </tbody>
                                      </table>
                                      <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/workflow/budget_add/{{ pk }}/?is_it_project_complete_form=true">Add Budget Contribution</a>
                                      </div>
                                    </div>
                                """),
                        ),
                    ),

                ),
                Tab('Impact',
                    Fieldset('',
                        'indicators', AppendedText('progress_against_targets','%'),'beneficiary_type', 'direct_beneficiaries', 'average_household_size', 'indirect_beneficiaries', 'capacity_built','quality_assured','issues_and_challenges', 'lessons_learned',
                    ),
                ),

                Tab('Approval',
                    Fieldset(
                        '','status',
                        Div(
                            '',
                             HTML("""
                                    <div class='panel panel-default'>
                                      <!-- Default panel contents -->
                                      <div class='panel-heading'>Approvals</div>
                                      {% if getApproval %}
                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Approval Type</th>
                                            <th>Note</th>
                                            <th>Approval Status</th>
                                            <th>Approved By</th>
                                            <th>Requested From</th>
                                            <th>Date Requested</th>
                                            <th>Date Approved</th>
                                            </tr>
                                            {% for item in getApproval %}
                                            <tr>
                                                <td>{{ item.approval_type}}</td>
                                                <td>{{ item.note}}</td>
                                                <td>{{ item.status}}</td>
                                                <td>{{ item.approval_by}}</td>
                                                <td>{{ item.requested_from}}</td>
                                                <td>{{ item.date_assigned}}</td>
                                                <td>{{ item.date_approved}}</td>
                                                <td><a class="output" data-toggle="modal" data-target="#myModal" href='/workflow/approval_update/{{ item.id }}/'>Edit</a> | <a class="output" href='/workflow/approval_delete/{{ item.id }}/' data-target="#myModal">Delete</a>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/workflow/approval_add/{{ pk }}/workflowlevel2/?is_it_project_complete_form=true">Request Approval</a>
                                      </div>
                                    </div>
                             """),
                        ),
                    ),
                ),
            ),

            FormActions(
                Submit('submit', 'Save', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            ),

            HTML("""<br/>"""),

            Fieldset(
                'Project Files',
                Div(
                    '',
                    HTML("""

                        <div class='panel panel-default'>
                          <!-- Default panel contents -->
                          <div class='panel-heading'>Documentation</div>
                          {% if getDocuments %}
                              <!-- Table -->
                              <table class="table">
                                <tr>
                                <th>Name</th>
                                <th>Link(URL)</th>
                                <th>Description</th>
                                <th>&nbsp;</th>
                                </tr>
                                {% for item in getDocuments %}
                                <tr>
                                    <td>{{ item.name}}</td>
                                    <td><a href="{{ item.url}}" target="_new">{{ item.url}}</a></td>
                                    <td>{{ item.description}}</td>
                                    <td><a class="monitoring" data-toggle="modal" data-target="#myModal" href='/workflow/documentation_agreement_update/{{ item.id }}/{{ pk }}/'>Edit</a> | <a class="monitoring" href='/workflow/documentation_agreement_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal">Delete</a>
                                </tr>
                                {% endfor %}
                              </table>
                          {% endif %}
                          <div class="panel-footer">
                            <a onclick="newPopup('/workflow/documentation_list/0/{{ pk }}','Add New Documentation'); return false;" href="#" class="btn btn-sm btn-info">Add New Documentation</a>
                          </div>
                        </div>
                         """),
                ),
            ),
        )
        super(WorkflowLevel2Form, self).__init__(*args, **kwargs)

        # override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['workflowlevel1'].widget = forms.HiddenInput()
        self.fields['short'].widget = forms.HiddenInput()

        # override the office queryset to use request.user for country
        self.fields['office'].queryset = Office.objects.filter(country__in=countries)

        # override the community queryset to use request.user for country
        self.fields['site'].queryset = SiteProfile.objects.filter(country__in=countries)

        # override the stakeholder queryset to use request.user for country
        self.fields['stakeholder'].queryset = Stakeholder.objects.filter(country__in=countries)
        self.fields['indicators'].queryset = Indicator.objects.filter(workflowlevel1__country__in=countries)


class WorkflowLevel2SimpleForm(forms.ModelForm):

    class Meta:
        model = WorkflowLevel2
        fields = '__all__'

        exclude = ['create_date', 'edit_date',]

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    expected_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    expected_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)


    approval = forms.ChoiceField(
        choices=APPROVALS,
        initial='in progress',
        required=False,
    )

    budget_variance = forms.ChoiceField(
        choices=BUDGET_VARIANCE,
        initial='Over Budget',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        #get the user object from request to check permissions
        self.request = kwargs.pop('request')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(
            HTML("""<br/>"""),
            TabHolder(
                Tab('Executive Summary',
                    Fieldset('Details',
                        'workflowlevel1', 'activity_code', 'office', 'sector','name','site','stakeholder'
                    ),
                    Fieldset('Dates',
                        'expected_start_date','expected_end_date', 'actual_start_date', 'actual_end_date',
                        'no_explanation',
                    ),
                ),
                Tab('Budget',
                    Fieldset('',
                        PrependedAppendedText('estimated_budget','$', '.00'), PrependedAppendedText('actual_cost','$', '.00')
                    ),
                    Fieldset("Other Budget Contributions:",
                         Div(
                            HTML("""
                                <div class='panel panel-default'>
                                    <div class='panel-heading'>Budget Contributions</div>
                                    <table class="table" id="budget_contributions_table">
                                        <tbody>
                                            {% if getBudget %}
                                                <tr>
                                                    <th>Contributor</th>
                                                    <th>Description</th>
                                                    <th>Value</th>
                                                    <th>View</th>
                                                </tr>
                                                {% for item in getBudget %}
                                                    <tr>
                                                        <td>{{ item.contributor}}</td>
                                                        <td>{{ item.contributor_description}}</td>
                                                        <td>{{ item.proposed_value}}</td>
                                                        <td><a class="output" data-toggle="modal" data-target="#myModal" href='/workflow/budget_update/{{ item.id }}/'>View</a> | <a class="output" href='/workflow/budget_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal" >Delete</a>
                                                    </tr>
                                                {% endfor %}
                                            {% endif %}
                                        </tbody>
                                    </table>
                                    <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/workflow/budget_add/{{ pk }}/?is_it_project_complete_form=true">Add Budget Contribution</a>
                                    </div>
                                </div>
                            """),
                        ),
                    ),
                ),
                Tab('Impact',
                    Fieldset('',
                        'indicators',AppendedText('progress_against_targets','%'), 'beneficiary_type', 'capacity_built', 'quality_assured','issues_and_challenges', 'lessons_learned'
                    ),
                ),
                Tab('Approval',
                    Fieldset(
                        '','status',
                        Div(
                            '',
                            HTML("""
                                    <div class='panel panel-default'>
                                      <!-- Default panel contents -->
                                      <div class='panel-heading'>Approvals</div>
                                      {% if getApproval %}
                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Approval Type</th>
                                            <th>Note</th>
                                            <th>Approval Status</th>
                                            <th>Approved By</th>
                                            <th>Requested From</th>
                                            <th>Date Requested</th>
                                            <th>Date Approved</th>
                                            </tr>
                                            {% for item in getApproval %}
                                            <tr>
                                                <td>{{ item.approval_type}}</td>
                                                <td>{{ item.note}}</td>
                                                <td>{{ item.status}}</td>
                                                <td>{{ item.approval_by}}</td>
                                                <td>{{ item.requested_from}}</td>
                                                <td>{{ item.date_assigned}}</td>
                                                <td>{{ item.date_approved}}</td>
                                                <td><a class="output" data-toggle="modal" data-target="#myModal" href='/workflow/approval_update/{{ item.id }}/'>Edit</a> | <a class="output" href='/workflow/approval_delete/{{ item.id }}/' data-target="#myModal">Delete</a>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/workflow/approval_add/{{ pk }}/workflowlevel2/">Request Approval</a>
                                      </div>
                                    </div>
                                 """),
                        ),
                    ),
                ),
            ),
            FormActions(
                Submit('submit', 'Save', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            ),
            HTML("""<br/>"""),
            Fieldset('Project Files',
                Div(
                    HTML("""
                        <div class='panel panel-default'>
                            <div class='panel-heading'>Documentation</div>
                            {% if getDocuments %}
                                <table class="table">
                                    <tr>
                                        <th>Name</th>
                                        <th>Link(URL)</th>
                                        <th>Description</th>
                                        <th>&nbsp;</th>
                                    </tr>
                                    {% for item in getDocuments %}
                                        <tr>
                                            <td>{{ item.name}}</td>
                                            <td><a href="{{ item.url}}" target="_new">{{ item.url}}</a></td>
                                            <td>{{ item.description}}</td>
                                            <td><a class="monitoring" data-toggle="modal" data-target="#myModal" href='/workflow/documentation_agreement_update/{{ item.id }}/{{ pk }}/'>Edit</a> | <a class="monitoring" href='/workflow/documentation_agreement_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal">Delete</a>
                                        </tr>
                                    {% endfor %}
                                </table>
                            {% endif %}
                            <div class="panel-footer">
                                <a onclick="newPopup('/workflow/documentation_list/0/{{ pk }}','Add New Documentation'); return false;" href="#" class="btn btn-sm btn-info">Add New Documentation</a>
                            </div>
                        </div>
                    """),
                ),
            ),
        )
        super(WorkflowLevel2SimpleForm, self).__init__(*args, **kwargs)

        countries = getCountry(self.request.user)

        #self.fields['program'].queryset = Program.objects.filter(funding_status="Funded", country__in=countries)
        self.fields['workflowlevel1'].widget = forms.HiddenInput()
        self.fields['short'].widget = forms.HiddenInput()

        # override the office queryset to use request.user for country
        self.fields['office'].queryset = Office.objects.filter(country__in=countries)

        # override the community queryset to use request.user for country
        self.fields['site'].queryset = SiteProfile.objects.filter(country__in=countries)

        # override the stakeholder queryset to use request.user for country
        self.fields['stakeholder'].queryset = Stakeholder.objects.filter(country__in=countries)
        self.fields['indicators'].queryset = Indicator.objects.filter(workflowlevel1__country__in=countries)


class SiteProfileForm(forms.ModelForm):

    class Meta:
        model = SiteProfile
        exclude = ['create_date', 'edit_date']

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude','country':'Find a city or village'}), required=False)

    date_of_firstcontact = forms.DateField(widget=DatePicker.DateInput(), required=False)

    approval = forms.ChoiceField(
        choices=APPROVALS,
        initial='in progress',
        required=False,
    )

    def __init__(self, *args, **kwargs):

        # get the user object from request to check user permissions
        self.request = kwargs.pop('request')

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True

        # Organize the fields in the site profile form using a layout class
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Profile',
                    Fieldset('Description',
                        'site_uuid', 'name', 'type', 'office','status',
                    ),
                    Fieldset('Contact Info',
                        'contact_leader', 'date_of_firstcontact', 'contact_number', 'num_members',
                    ),
                ),
                Tab('Location',
                    Fieldset('Places',
                        'country','province','district','admin_level_three','village', Field('latitude', step="any"), Field('longitude', step="any"),
                    ),
                    Fieldset('Map',
                        'map',
                    ),
                ),
                Tab('Demographic Information',
                    Fieldset('Land',
                        'classify_land','total_land','total_agricultural_land','total_rainfed_land','total_horticultural_land',
                        'populations_owning_land', 'avg_landholding_size', 'households_owning_livestock','animal_type'
                    ),
                    Fieldset('Literacy',
                        'literate_males','literate_females','literacy_rate',
                    ),
                    Fieldset('Demographic Info Data Source',
                             'info_source'
                    ),
                ),

            ),
            FormActions(
                Submit('submit', 'Save', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            ),

             HTML("""
                  <br/>
                  <div class='panel panel-default'>

                  <!-- Default panel contents -->
                  <div class='panel-heading'>Projects in this Site</div>
                    {% if getProjects %}
                      <!-- Table -->
                      <table class="table">
                       <tr>
                         <th>Project Name</th>
                         <th>Program</th>
                         <th>Activity Code</th>
                         <th>View</th>
                       </tr>

                    {% for item in getProjects %}
                       <tr>
                        <td>{{ item.name }}</td>
                        <td>{{ item.workflowlevel1.name }}</td>
                        <td>{{ item.activity_code }}</td>
                        <td><a target="_new" href='/workflow/projectagreement_detail/{{ item.id }}/'>View</a>
                       </tr>
                    {% endfor %}
                     </table>
                    {% endif %}
                  </div>
             """),
        )

        super(SiteProfileForm, self).__init__(*args, **kwargs)

        #override the office queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['date_of_firstcontact'].label = "Date of First Contact"
        self.fields['office'].queryset = Office.objects.filter(country__in=countries)
        self.fields['province'].queryset = AdminLevelOne.objects.filter(country__in=countries)
        self.fields['site_uuid'].widget = forms.HiddenInput()


class DocumentationForm(forms.ModelForm):

    class Meta:
        model = Documentation
        exclude = ['create_date', 'edit_date']


    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.request = kwargs.pop('request')
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.layout = Layout(

            HTML("""<br/>"""),

                'name',FieldWithButtons('url', StrictButton("gdrive", onclick="onApiLoad();")), Field('description', rows="3", css_class='input-xlarge'),
                'workflowlevel2','workflowlevel1',

            FormActions(
                Submit('submit', 'Save', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )

        super(DocumentationForm, self).__init__(*args, **kwargs)

        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['workflowlevel2'].queryset = WorkflowLevel2.objects.filter(workflowlevel1__country__in=countries)
        self.fields['workflowlevel1'].queryset = WorkflowLevel1.objects.filter(country__in=countries)


class QuantitativeOutputsForm(forms.ModelForm):

    class Meta:
        model = CollectedData
        exclude = ['create_date', 'edit_date']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.request = kwargs.pop('request')
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_tag = False
        self.helper.layout = Layout(

                'targeted','achieved','indicator','workflowlevel2','workflowlevel1'

        )

        super(QuantitativeOutputsForm, self).__init__(*args, **kwargs)

        countries = getCountry(self.request.user)

        self.fields['indicator'].queryset = Indicator.objects.filter(workflowlevel1__id=kwargs['initial']['program'])
        self.fields['workflowlevel2'].queryset = WorkflowLevel2.objects.filter(id=kwargs['initial']['agreement'])
        #self.fields['program'].widget.attrs['disabled'] = "disabled"
        self.fields['workflowlevel1'].widget = HiddenInput()
        self.fields['workflowlevel2'].widget = HiddenInput()


class ChecklistItemForm(forms.ModelForm):

    class Meta:
        model = ChecklistItem
        exclude = ['create_date', 'edit_date','global_item']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.add_input(Submit('submit', 'Save'))

        super(ChecklistItemForm, self).__init__(*args, **kwargs)

        #countries = getCountry(self.request.user)
        #override the community queryset to use request.user for country
        #self.fields['item'].queryset = ChecklistItem.objects.filter(checklist__country__in=countries)


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        exclude = ['create_date', 'edit_date']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.add_input(Submit('submit', 'Save'))

        super(ContactForm, self).__init__(*args, **kwargs)


class StakeholderForm(forms.ModelForm):

    class Meta:
        model = Stakeholder
        #fields = ['contact', 'country', 'approved_by', 'filled_by', 'sectors', 'formal_relationship_document', 'vetting_document', ]
        exclude = ['create_date', 'edit_date']

    approval = forms.ChoiceField(
        choices=APPROVALS,
        initial='in progress',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.request = kwargs.pop('request')
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.add_input(Submit('submit', 'Save'))
        pkval = kwargs['instance'].pk if kwargs['instance'] else 0
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Details',
                    Fieldset('Details',
                        'organization', 'stakeholder_uuid','name', 'type', 'contact', HTML("""<a onclick="window.open('/workflow/contact_add/%s/0/').focus();">Add New Contact</a>""" % pkval ), 'country', 'sectors', PrependedText('stakeholder_register',''), 'formal_relationship_document', 'vetting_document', 'notes',
                    ),
                ),

                Tab('Approval',
                    Fieldset(
                        '',
                        Div(
                            '',
                            HTML("""
                                    <div class='panel panel-default'>
                                      <!-- Default panel contents -->
                                      <div class='panel-heading'>Approvals</div>
                                      {% if getApproval %}
                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Approval Type</th>
                                            <th>Note</th>
                                            <th>Approval Status</th>
                                            <th>Approved By</th>
                                            <th>Requested From</th>
                                            <th>Date Requested</th>
                                            <th>Date Approved</th>
                                            </tr>
                                            {% for item in getApproval %}
                                            <tr>
                                                <td>{{ item.approval_type}}</td>
                                                <td>{{ item.note}}</td>
                                                <td>{{ item.status}}</td>
                                                <td>{{ item.approval_by}}</td>
                                                <td>{{ item.requested_from}}</td>
                                                <td>{{ item.date_assigned}}</td>
                                                <td>{{ item.date_approved}}</td>
                                                <td><a class="output" data-toggle="modal" data-target="#myModal" href='/workflow/approval_update/{{ item.id }}/'>Edit</a> | <a class="output" href='/workflow/approval_delete/{{ item.id }}/' data-target="#myModal">Delete</a>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/workflow/approval_add/{{ pk }}/stakeholder/">Request Approval</a>
                                      </div>
                                    </div>
                                 """),
                        ),
                    ),
                ),
            ),
        )
        super(StakeholderForm, self).__init__(*args, **kwargs)

        countries = getCountry(self.request.user)
        users = TolaUser.objects.filter(country__in=countries)
        self.fields['contact'].queryset = Contact.objects.filter(country__in=countries)
        self.fields['sectors'].queryset = Sector.objects.all()
        self.fields['country'].queryset = countries
        self.fields['formal_relationship_document'].queryset = Documentation.objects.filter(workflowlevel1__country__in=countries)
        self.fields['vetting_document'].queryset = Documentation.objects.filter(workflowlevel1__country__in=countries)
        self.fields['stakeholder_uuid'].widget = forms.HiddenInput()
        self.fields['organization'].widget = forms.HiddenInput()


class FilterForm(forms.Form):
    fields = "search"
    search = forms.CharField(required=False)
    helper = FormHelper()
    helper.form_method = 'get'
    helper.form_class = 'form-inline'
    helper.layout = Layout(FieldWithButtons('search', StrictButton('Submit', type='submit', css_class='btn-primary')))


class ProjectCompleteTable(forms.ModelForm):

    class Meta:
        model = WorkflowLevel2
        fields = '__all__'
