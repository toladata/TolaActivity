from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset, Field
from functools import partial
from widgets import GoogleMapsWidget
from django import forms
from .models import WorkflowLevel2, WorkflowLevel1, SiteProfile, Documentation, WorkflowLevel3, Budget, Capacity,\
    Evaluate, Office, Checklist, ChecklistItem, Province, Stakeholder, TolaUser, Contact
from indicators.models import CollectedData, Indicator
from crispy_forms.layout import LayoutObject, TEMPLATE_PACK
from tola.util import getCountry
import ast
import collections


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
            Field('contributor', required=False), Field('description_of_contribution', required=False), PrependedAppendedText('proposed_value','$', '.00'), 'agreement',
        )


        super(BudgetForm, self).__init__(*args, **kwargs)
        
        countries = getCountry(self.request.user)

        self.fields['agreement'].queryset = WorkflowLevel2.objects.filter(program__country__in = countries)

    def save(self, *args, **kwargs):
        # Commit is already set to false
        obj = super(BudgetForm, self).save(*args, **kwargs)
        return obj


class ProjectAgreementCreateForm(forms.ModelForm):

    class Meta:
        model = WorkflowLevel2
        fields = '__all__'

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
        super(ProjectAgreementCreateForm, self).__init__(*args, **kwargs)

class ProjectAgreementForm(forms.ModelForm):

    class Meta:
        model = WorkflowLevel2
        fields = '__all__'
        exclude = ['create_date', 'edit_date', 'short']

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    expected_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    expected_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    estimation_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    reviewed_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    approved_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    me_reviewed_by_date = forms.DateField(label="M&E Reviewed by Date", widget=DatePicker.DateInput(), required=False)
    checked_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    estimated_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    finance_reviewed_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    exchange_rate_date = forms.DateField(widget=DatePicker.DateInput(), required=False)

    documentation_government_approval = forms.FileField(required=False)
    documentation_community_approval = forms.FileField(required=False)

    effect_or_impact = forms.CharField(help_text="Please do not include outputs and keep less than 120 words. Describe the logic that will link this project/activity to the proposed desired outcome/goal. Note any assumptions that are critical in this logic chain.", widget=forms.Textarea, required=False)
    justification_background = forms.CharField(help_text="As someone would write a background and problem statement in a proposal, this should be described here. What is the situation in this community where the project is proposed and what is the problem facing them that this project will help solve", widget=forms.Textarea, required=False)
    justification_description_community_selection = forms.CharField(help_text="How was this community selected for this project. It may be it was already selected as part of the project (like CDP-2, KIWI-2), but others may need to describe, out of an entire cluster, why this community? This can't be just 'because they wanted it', or 'because they are poor.' It must refer to a needs assessment, some kind of selection criteria, maybe identification by the government, or some formal process.", widget=forms.Textarea, required=False)
    description_of_project_activities = forms.CharField(help_text="Briefly describe the day to day work you plan to complete in order to accomplish this project. Include rationale for budget, scope, timeframe as well as staff and stakeholders that will be necessary to seeing this project is effectively implemented. Site any documentation/monitoring efforts that you'll need to do before completion.", widget=forms.Textarea, required=False)
    description_of_government_involvement = forms.CharField(help_text="This is an open-text field for describing the project. It does not need to be too long, but this is where you will be the main description and the main description that will be in the database.  Please make this a description from which someone can understand what this project is doing. You do not need to list all activities, such as those that will appear on your benchmark list. Just describe what you are doing. You should attach technical drawings, technical appraisals, bill of quantity or any other appropriate documentation", widget=forms.Textarea, required=False)
    documentation_government_approval = forms.CharField(help_text="Check the box if there IS documentation to show government request for or approval of the project. This should be attached to the proposal, and also kept in the program file.", widget=forms.Textarea, required=False)
    description_of_community_involvement = forms.CharField(help_text="How the community is involved in the planning, approval, or implementation of this project should be described. Indicate their approval (copy of a signed MOU, or their signed Project Prioritization request, etc.). But also describe how they will be involved in the implementation - supplying laborers, getting training, etc.", widget=forms.Textarea, required=False)

    approval = forms.ChoiceField(
        choices=APPROVALS,
        initial='in progress',
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
        self.helper.form_tag = True
        self.helper.form_id = "agreement"
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Executive Summary',
                    Fieldset('Project Details', 'activity_code','account_code','lin_code','office', 'sector','program', 'project_name', 'project_activity',
                             'project_type', 'site','stakeholder','mc_staff_responsible','expected_start_date','expected_end_date',
                        ),
                    ),
                Tab('Components',
                    Fieldset("Project Components",
                        HTML("""

                            <div class='panel panel-default'>
                              <!-- Default panel contents -->
                              <div class='panel-heading'>Components</div>
                              {% if getBenchmark %}
                                  <!-- Table -->
                                  <table class="table">
                                    <tr>
                                    <th>Description</th>
                                    <th>Site</th>
                                    <th>Est. Start Date</th>
                                    <th>Est. End Date</th>
                                    <th>Budget</th>
                                    <th>View</th>
                                    </tr>
                                    {% for item in getBenchmark %}
                                    <tr>
                                        <td>{{ item.description}}</td>
                                        <td>{{ item.site }}</td>
                                        <td>{{ item.est_start_date|date:"m-d-Y" }}</td>
                                        <td>{{ item.est_end_date|date:"m-d-Y" }}</td>
                                        <td>{{ item.budget }}</td>
                                        <td><a class="benchmarks" data-toggle="modal" data-target="#myModal" href='/workflow/benchmark_update/{{ item.id }}/'>Edit</a> | <a class="benchmarks" href='/workflow/benchmark_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal">Delete</a></td>
                                    </tr>
                                    {% endfor %}
                                  </table>
                              {% endif %}
                              <div class="panel-footer">
                                <a class="benchmarks" data-toggle="modal" data-target="#myModal" href="/workflow/benchmark_add/{{ pk }}">Add Component</a>
                              </div>
                            </div>

                            """),
                        ),
                    ),
                Tab('Budget',
                    Fieldset(
                        'Budget',
                        PrependedAppendedText('total_estimated_budget','$', '.00'), PrependedAppendedText('mc_estimated_budget','$', '.00'),
                        AppendedText('local_total_estimated_budget', '.00'), AppendedText('local_mc_estimated_budget', '.00'),
                        'exchange_rate','exchange_rate_date','estimation_date','other_budget',
                    ),
                    Fieldset("Other Budget Contributions:",
                        Div(
                            "",
                            HTML("""
                                <div class='panel panel-default'>
                                  <!-- Default panel contents -->
                                  <div class='panel-heading'>Budget Contributions</div>
                                  {% if getBudget %}
                                      <!-- Table -->
                                      <table class="table">
                                        <tr>
                                        <th>Contributor</th>
                                        <th>Description</th>
                                        <th>Value</th>
                                        <th>View</th>
                                        </tr>
                                        {% for item in getBudget %}
                                        <tr>
                                            <td>{{ item.contributor}}</td>
                                            <td>{{ item.description_of_contribution}}</td>
                                            <td>{{ item.proposed_value}}</td>
                                            <td><a class="output" data-toggle="modal" data-target="#myModal" href='/workflow/budget_update/{{ item.id }}/'>Edit</a> | <a class="output" href='/workflow/budget_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal" >Delete</a>
                                        </tr>
                                        {% endfor %}
                                      </table>
                                  {% endif %}
                                  <div class="panel-footer">
                                    <a class="output" data-toggle="modal" data-target="#myModal" href="/workflow/budget_add/{{ pk }}">Add Budget Contribution</a>
                                  </div>
                                </div>
                                 """),
                            ),
                        ),
                    ),
                Tab('Justification and Description',
                     Fieldset(
                        'Description',
                        Field('description_of_project_activities', rows="4", css_class='input-xlarge'),

                        ),
                    Fieldset(
                        'Justification',
                        Field('effect_or_impact',rows="4", css_class='input-xlarge', label="Anticipated Outcome and Goal"),
                        Field('risks_assumptions',rows="4", css_class='input-xlarge', label="Risks and Assumptions"),
                        ),
                    ),
                Tab('M&E',
                    Fieldset(
                        '',
                        Div(
                            '',
                             HTML("""
                                    <div class='panel panel-default'>
                                      <!-- Default panel contents -->
                                      <div class='panel-heading'>Indicator</div>
                                      {% if getQuantitative %}
                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Targeted</th>
                                            <th>Indicator</th>
                                            <th>View</th>
                                            </tr>
                                            {% for item in getQuantitative %}
                                            <tr>
                                                <td>{{ item.targeted}}</td>
                                                <td><a href="/indicators/indicator_update/{{ item.indicator_id }}">{{ item.indicator}}<a/></td>
                                                <td><a class="output" data-toggle="modal" data-target="#myModal" href='/workflow/quantitative_update/{{ item.id }}/'>Edit</a> | <a class="output" href='/workflow/quantitative_delete/{{ item.id }}/' data-target="#myModal">Delete</a>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/workflow/quantitative_add/{{ pk }}">Add Quantitative Outputs</a>
                                      </div>
                                    </div>
                                     """),

                            'capacity',
                        ),
                    ),
                    Fieldset(
                        '',
                        Div(
                            '',
                            HTML("""
                                    <br/>
                                    <div class='panel panel-default'>
                                      <!-- Default panel contents -->
                                      <div class='panel-heading'>Monitoring</div>
                                      {% if getMonitor %}
                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Person Responsible</th>
                                            <th>Frequency</th>
                                            <th>Type</th>
                                            <th>View</th>
                                            </tr>
                                            {% for item in getMonitor %}
                                            <tr>
                                                <td>{{ item.responsible_person}}</td>
                                                <td>{{ item.frequency}}</td>
                                                <td>{{ item.type}}</td>
                                                <td><a class="monitoring" data-toggle="modal" data-target="#myModal" href='/workflow/monitor_update/{{ item.id }}/'>Edit</a> | <a class="monitoring" href='/workflow/monitor_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal">Delete</a>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="monitoring" data-toggle="modal" data-target="#myModal" href="/workflow/monitor_add/{{ pk }}">Add Monitoring Data</a>
                                      </div>
                                    </div>
                                     """),

                            'evaluate',
                            ),
                        ),
                    ),

                Tab('Approval',
                    Fieldset('Approval',
                             'approval', 'estimated_by', 'reviewed_by',
                             'finance_reviewed_by','finance_reviewed_by_date','me_reviewed_by','me_reviewed_by_date','approved_by', 'approved_by_date',
                             Field('approval_remarks', rows="3", css_class='input-xlarge')
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
        super(ProjectAgreementForm, self).__init__(*args, **kwargs)

        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['program'].queryset = WorkflowLevel1.objects.filter(funding_status="Funded", country__in=countries).distinct()
        self.fields['approved_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()
        self.fields['estimated_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()
        self.fields['reviewed_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()
        self.fields['finance_reviewed_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()
        self.fields['me_reviewed_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()
        self.fields['approval_submitted_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()

        #override the office queryset to use request.user for country
        self.fields['office'].queryset = Office.objects.filter(province__country__in=countries)

        #override the site queryset to use request.user for country
        self.fields['site'].queryset = SiteProfile.objects.filter(country__in=countries)

        #override the stakeholder queryset to use request.user for country
        self.fields['stakeholder'].queryset = Stakeholder.objects.filter(country__in=countries)

        if not 'Approver' in self.request.user.groups.values_list('name', flat=True):
            APPROVALS = (
                ('in progress', 'in progress'),
                ('awaiting approval', 'awaiting approval'),
                ('rejected', 'rejected'),
            )
            self.fields['approval'].choices = APPROVALS
            #self.fields['approved_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_remarks'].widget.attrs['disabled'] = "disabled"
            self.fields['approval'].help_text = "Approval level permissions required"


class ProjectAgreementSimpleForm(forms.ModelForm):

    class Meta:
        model = WorkflowLevel2
        fields = '__all__'
        exclude = ['create_date', 'edit_date','account_code','lin_code','mc_estimated_budget','local_total_estimated_budget','local_estimated_budget'
                   ,'approval_submitted_by','finance_reviewed_by','me_reviewed_by','exchange_rate','exchange_rate_date','estimation_date','other_budget','short']

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    expected_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    expected_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    estimation_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    reviewed_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    approved_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    me_reviewed_by_date = forms.DateField(label="M&E Reviewed by Date", widget=DatePicker.DateInput(), required=False)
    checked_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    estimated_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    finance_reviewed_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    exchange_rate_date = forms.DateField(widget=DatePicker.DateInput(), required=False)

    documentation_government_approval = forms.FileField(required=False)
    documentation_community_approval = forms.FileField(required=False)

    effect_or_impact = forms.CharField(help_text="Please do not include outputs and keep less than 120 words. Describe the logic that will link this project/activity to the proposed desired outcome/goal. Note any assumptions that are critical in this logic chain.", widget=forms.Textarea, required=False)
    justification_background = forms.CharField(help_text="As someone would write a background and problem statement in a proposal, this should be described here. What is the situation in this community where the project is proposed and what is the problem facing them that this project will help solve", widget=forms.Textarea, required=False)
    justification_description_community_selection = forms.CharField(help_text="How was this community selected for this project. It may be it was already selected as part of the project (like CDP-2, KIWI-2), but others may need to describe, out of an entire cluster, why this community? This can't be just 'because they wanted it', or 'because they are poor.' It must refer to a needs assessment, some kind of selection criteria, maybe identification by the government, or some formal process.", widget=forms.Textarea, required=False)
    description_of_project_activities = forms.CharField(help_text="Briefly describe the day to day work you plan to complete in order to accomplish this project. Include rationale for budget, scope, timeframe as well as staff and stakeholders that will be necessary to seeing this project is effectively implemented. Site any documentation/monitoring efforts that you'll need to do before completion.", widget=forms.Textarea, required=False)
    description_of_government_involvement = forms.CharField(help_text="This is an open-text field for describing the project. It does not need to be too long, but this is where you will be the main description and the main description that will be in the database.  Please make this a description from which someone can understand what this project is doing. You do not need to list all activities, such as those that will appear on your benchmark list. Just describe what you are doing. You should attach technical drawings, technical appraisals, bill of quantity or any other appropriate documentation", widget=forms.Textarea, required=False)
    documentation_government_approval = forms.CharField(help_text="Check the box if there IS documentation to show government request for or approval of the project. This should be attached to the proposal, and also kept in the program file.", widget=forms.Textarea, required=False)
    description_of_community_involvement = forms.CharField(help_text="How the community is involved in the planning, approval, or implementation of this project should be described. Indicate their approval (copy of a signed MOU, or their signed Project Prioritization request, etc.). But also describe how they will be involved in the implementation - supplying laborers, getting training, etc.", widget=forms.Textarea, required=False)

    approval = forms.ChoiceField(
        choices=APPROVALS,
        initial='in progress',
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
        self.helper.form_tag = True
        self.helper.form_id = "agreement"
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Executive Summary',
                    Fieldset('Project Details', 'activity_code','office', 'sector','program', 'project_name',
                             'site','stakeholder','expected_start_date','expected_end_date',
                        ),

                    ),
                Tab('Components',
                    Fieldset("Project Components",
                        HTML("""

                            <div class='panel panel-default'>
                              <!-- Default panel contents -->
                              <div class='panel-heading'>Components</div>
                              {% if getBenchmark %}
                                  <!-- Table -->
                                  <table class="table">
                                    <tr>
                                    <th>Description</th>
                                    <th>Site</th>
                                    <th>Est. Start Date</th>
                                    <th>Est. End Date</th>
                                    <th>Budget</th>
                                    <th>View</th>
                                    </tr>
                                    {% for item in getBenchmark %}
                                    <tr>
                                        <td>{{ item.description}}</td>
                                        <td>{{ item.site }}</td>
                                        <td>{{ item.est_start_date|date:"m-d-Y" }}</td>
                                        <td>{{ item.est_end_date|date:"m-d-Y" }}</td>
                                        <td>{{ item.budget }}</td>
                                        <td><a class="benchmarks" data-toggle="modal" data-target="#myModal" href='/workflow/benchmark_update/{{ item.id }}/'>Edit</a> | <a class="benchmarks" href='/workflow/benchmark_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal">Delete</a></td>
                                    </tr>
                                    {% endfor %}
                                  </table>
                              {% endif %}
                              <div class="panel-footer">
                                <a class="benchmarks" data-toggle="modal" data-target="#myModal" href="/workflow/benchmark_add/{{ pk }}">Add Component</a>
                              </div>
                            </div>

                            """),
                        ),
                    ),
                Tab('Budget',
                    Fieldset(
                        'Budget',
                        PrependedAppendedText('total_estimated_budget','$', '.00'),
                        'estimation_date',
                    ),
                    Fieldset("Other Budget Contributions:",
                        Div(
                            "",
                            HTML("""

                                <div class='panel panel-default'>
                                  <!-- Default panel contents -->
                                  <div class='panel-heading'>Budget Contributions</div>
                                  {% if getBudget %}
                                      <!-- Table -->
                                      <table class="table">
                                        <tr>
                                        <th>Contributor</th>
                                        <th>Description</th>
                                        <th>Value</th>
                                        <th>View</th>
                                        </tr>
                                        {% for item in getBudget %}
                                        <tr>
                                            <td>{{ item.contributor}}</td>
                                            <td>{{ item.description_of_contribution}}</td>
                                            <td>{{ item.proposed_value}}</td>
                                            <td><a class="output" data-toggle="modal" data-target="#myModal" href='/workflow/budget_update/{{ item.id }}/'>Edit</a> | <a class="output" href='/workflow/budget_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal" >Delete</a>
                                        </tr>
                                        {% endfor %}
                                      </table>
                                  {% endif %}
                                  <div class="panel-footer">
                                    <a class="output" data-toggle="modal" data-target="#myModal" href="/workflow/budget_add/{{ pk }}">Add Budget Contribution</a>
                                  </div>
                                </div>
                                 """),
                            ),
                        ),

                    ),

                Tab('Justification and Description',
                    Fieldset(
                        'Description',
                        Field('description_of_project_activities', rows="4", css_class='input-xlarge'),

                        ),
                    Fieldset(
                        'Justification',
                        Field('effect_or_impact',rows="4", css_class='input-xlarge', label="Anticipated Outcome and Goal"),
                        Field('risks_assumptions',rows="4", css_class='input-xlarge', label="Risks and Assumptions"),
                        ),
                    ),

                Tab('Approval',
                    Fieldset('Approval',
                             'approval', 'estimated_by',
                             'approved_by', 'approved_by_date',
                             Field('approval_remarks', rows="3", css_class='input-xlarge')
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
        super(ProjectAgreementSimpleForm, self).__init__(*args, **kwargs)

        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['program'].queryset = WorkflowLevel1.objects.filter(funding_status="Funded", country__in=countries).distinct()
        self.fields['approved_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()
        self.fields['reviewed_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()
        self.fields['estimated_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()

        #override the office queryset to use request.user for country
        self.fields['office'].queryset = Office.objects.filter(province__country__in=countries)

        #override the site queryset to use request.user for country
        self.fields['site'].queryset = SiteProfile.objects.filter(country__in=countries)

        #override the stakeholder queryset to use request.user for country
        self.fields['stakeholder'].queryset = Stakeholder.objects.filter(country__in=countries)

        if not 'Approver' in self.request.user.groups.values_list('name', flat=True):
            APPROVALS = (
                ('in progress', 'in progress'),
                ('awaiting approval', 'awaiting approval'),
                ('rejected', 'rejected'),
            )
            self.fields['approval'].choices = APPROVALS
            #self.fields['approved_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_remarks'].widget.attrs['disabled'] = "disabled"
            self.fields['approval'].help_text = "Approval level permissions required"


class ProjectCompleteCreateForm(forms.ModelForm):

    class Meta:
        model = WorkflowLevel2
        fields = '__all__'

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    expected_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    expected_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)

    workflowlevel1 = forms.ModelChoiceField(queryset=WorkflowLevel1.objects.filter(funding_status="Funded"))

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
                    Fieldset('Program', 'program', 'project_proposal', 'project_agreement', 'activity_code', 'office', 'sector', 'project_name','site','stakeholder',
                    ),
                    Fieldset(
                        'Dates',
                        'expected_start_date','expected_end_date', 'actual_start_date', 'actual_end_date',
                        PrependedText('on_time', ''), 'no_explanation',

                    ),
                ),
            ),
            FormActions(
                Submit('submit', 'Save', css_class='btn-default')
            ),
        )
        super(ProjectCompleteCreateForm, self).__init__(*args, **kwargs)

        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['program'].queryset = WorkflowLevel1.objects.filter(funding_status="Funded", country__in=countries)

        #override the office queryset to use request.user for country
        self.fields['office'].queryset = Office.objects.filter(province__country__in=countries)


class ProjectCompleteForm(forms.ModelForm):

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

    workflowlevel1 = forms.ModelChoiceField(queryset=WorkflowLevel1.objects.filter(funding_status="Funded"))

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
                    Fieldset('', 'program', 'project_proposal', 'project_agreement', 'activity_code','account_code','lin_code',\
                             'office', 'sector','project_name', 'project_activity', 'site', 'stakeholder',
                        ),
                    Fieldset(
                        'Dates',
                        'expected_start_date','expected_end_date', 'actual_start_date', 'actual_end_date',
                        PrependedText('on_time', ''), 'no_explanation',

                        ),
                    ),
                Tab('Components',
                    Fieldset("Project Components",
                        HTML("""

                            <div class='panel panel-default'>
                              <!-- Default panel contents -->
                              <div class='panel-heading'>Components</div>
                              {% if getBenchmark %}
                                  <!-- Table -->
                                  <table class="table">
                                    <tr>
                                    <th>Description</th>
                                    <th>Site</th>
                                    <th>Est. Start Date</th>
                                    <th>Est. End Date</th>
                                    <th>Actual Start Date</th>
                                    <th>Actual End Date</th>
                                    <th>Budget</th>
                                    <th>Actual Cost</th>
                                    <th>View</th>
                                    </tr>
                                    {% for item in getBenchmark %}
                                    <tr>
                                        <td>{{ item.description}}</td>
                                        <td>{{ item.site }}</td>
                                        <td>{{ item.est_start_date|date:"m-d-Y"}}</td>
                                        <td>{{ item.est_end_date|date:"m-d-Y"}}</td>
                                        <td>{{ item.actual_start_date|date:"m-d-Y"}}</td>
                                        <td>{{ item.actual_end_date|date:"m-d-Y"}}</td>
                                        <td>{{ item.budget}}</td>
                                        <td>{{ item.cost}}</td>
                                        <td><a class="benchmarks" data-toggle="modal" data-target="#myModal" href='/workflow/benchmark_complete_update/{{ item.id }}/'>Edit</a> | <a class="benchmarks" href='/workflow/benchmark_complete_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal">Delete</a></td>
                                    </tr>
                                    {% endfor %}
                                  </table>
                              {% endif %}
                              <div class="panel-footer">
                                <a class="benchmarks" data-toggle="modal" data-target="#myModal" href="/workflow/benchmark_complete_add/{{ id }}/">Add Component</a>
                              </div>
                            </div>

                            """),
                        ),
                    ),
                Tab('Budget',
                    Fieldset(
                        '',
                        PrependedAppendedText('estimated_budget','$', '.00'), PrependedAppendedText('actual_budget','$', '.00'),'actual_cost_date', 'budget_variance', 'explanation_of_variance',
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
                                      {% if getBudget %}
                                          <!-- Table -->
                                          <table class="table">
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
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/workflow/budget_add/{{ id }}">Add Budget Contribution</a>
                                      </div>
                                    </div>
                                """),
                        ),
                    ),

                ),
                Tab('Impact',
                    Fieldset(
                        '',
                        Div(
                            '',
                             HTML("""
                                    <div class='panel panel-default'>
                                      <!-- Default panel contents -->
                                      <div class='panel-heading'>Indicator</div>
                                      {% if getQuantitative %}
                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Targeted</th>
                                            <th>Achieved</th>
                                            <th>Indicator</th>
                                            <th>View</th>
                                            </tr>
                                            {% for item in getQuantitative %}
                                            <tr>
                                                <td>{{ item.targeted}}</td>
                                                <td>{{ item.achieved}}</td>
                                                <td><a href="/indicators/indicator_update/{{ item.indicator_id }}">{{ item.indicator}}<a/></td>
                                                <td><a class="output" data-toggle="modal" data-target="#myModal" href='/workflow/quantitative_update/{{ item.id }}/'>Edit</a> | <a class="output" href='/workflow/quantitative_delete/{{ item.id }}/' data-target="#myModal">Delete</a>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/workflow/quantitative_add/{{ id }}">Add Quantitative Outputs</a>
                                      </div>
                                    </div>
                             """),
                        ),
                    ),
                    Fieldset(
                        '',AppendedText('progress_against_targets','%'),'actual_contribution','beneficiary_type', 'direct_beneficiaries', 'average_household_size', 'indirect_beneficiaries', 'capacity_built','quality_assured','issues_and_challenges', 'lessons_learned',
                    ),
                ),

                Tab('Approval',
                    Fieldset('Approval',
                             'approval', 'approved_by',
                             Field('approval_remarks', rows="3", css_class='input-xlarge')
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
                            <a onclick="newPopup('/workflow/documentation_list/0/{{ id }}','Add New Documentation'); return false;" href="#" class="btn btn-sm btn-info">Add New Documentation</a>
                          </div>
                        </div>
                         """),
                ),
            ),

        )
        super(ProjectCompleteForm, self).__init__(*args, **kwargs)

        # override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['program'].queryset = WorkflowLevel1.objects.filter(funding_status="Funded", country__in=countries)
        self.fields['approved_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()

        # override the office queryset to use request.user for country
        self.fields['office'].queryset = Office.objects.filter(province__country__in=countries)

        # override the community queryset to use request.user for country
        self.fields['site'].queryset = SiteProfile.objects.filter(country__in=countries)

        # override the stakeholder queryset to use request.user for country
        self.fields['stakeholder'].queryset = Stakeholder.objects.filter(country__in=countries)

        if not 'Approver' in self.request.user.groups.values_list('name', flat=True):
            APPROVALS = (
                ('in progress', 'in progress'),
                ('awaiting approval', 'awaiting approval'),
                ('rejected', 'rejected'),
            )
            self.fields['approval'].choices = APPROVALS
            self.fields['approved_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_submitted_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_remarks'].widget.attrs['disabled'] = "disabled"
            self.fields['approval'].help_text = "Approval level permissions required"


class ProjectCompleteSimpleForm(forms.ModelForm):

    class Meta:
        model = WorkflowLevel2
        fields = '__all__'

        exclude = ['create_date', 'edit_date','project_activity', 'account_code', 'lin_code', 'mc_estimated_budget',
               'local_total_estimated_budget', 'local_estimated_budget', 'approval_submitted_by', 'finance_reviewed_by',
               'me_reviewed_by', 'exchange_rate', 'exchange_rate_date',
               'estimation_date', 'other_budget']

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    expected_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    expected_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)

    workflowlevel1 = forms.ModelChoiceField(queryset=WorkflowLevel1.objects.filter(funding_status="Funded"))

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
                    Fieldset('', 'program', 'project_agreement', 'activity_code',
                             'office', 'sector','project_name','site','stakeholder',
                        ),
                    Fieldset(
                        'Dates',
                        'expected_start_date','expected_end_date', 'actual_start_date', 'actual_end_date',
                        PrependedText('on_time', ''), 'no_explanation',

                        ),
                    ),
                Tab('Components',
                    Fieldset("Project Components",
                        HTML("""
                            <div class='panel panel-default'>
                              <!-- Default panel contents -->
                              <div class='panel-heading'>Components</div>
                              {% if getBenchmark %}
                                  <!-- Table -->
                                  <table class="table">
                                    <tr>
                                    <th>Description</th>
                                    <th>Site</th>
                                    <th>Est. Start Date</th>
                                    <th>Est. End Date</th>
                                    <th>Actual Start Date</th>
                                    <th>Actual End Date</th>
                                    <th>Budget</th>
                                    <th>Actual Cost</th>
                                    <th>View</th>
                                    </tr>
                                    {% for item in getBenchmark %}
                                    <tr>
                                        <td>{{ item.description}}</td>
                                        <td>{{ item.site }}</td>
                                        <td>{{ item.est_start_date|date:"m-d-Y"}}</td>
                                        <td>{{ item.est_end_date|date:"m-d-Y"}}</td>
                                        <td>{{ item.actual_start_date|date:"m-d-Y"}}</td>
                                        <td>{{ item.actual_end_date|date:"m-d-Y"}}</td>
                                        <td>{{ item.budget}}</td>
                                        <td>{{ item.cost}}</td>
                                        <td><a class="benchmarks" data-toggle="modal" data-target="#myModal" href='/workflow/benchmark_complete_update/{{ item.id }}/'>Edit</a> | <a class="benchmarks" href='/workflow/benchmark_complete_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal">Delete</a></td>
                                    </tr>
                                    {% endfor %}
                                  </table>
                              {% endif %}
                              <div class="panel-footer">
                                <a class="benchmarks" data-toggle="modal" data-target="#myModal" href="/workflow/benchmark_complete_add/{{ id }}/" id="btn_bench">Add Component</a>
                              </div>
                            </div>

                            """),
                        ),
                    ),
                Tab('Budget',
                    Fieldset(
                        '',
                        PrependedAppendedText('estimated_budget','$', '.00'), PrependedAppendedText('actual_budget','$', '.00')
                    ),
                    Fieldset("Other Budget Contributions:",
                         Div(
                             "",
                             HTML("""

                                    <div class='panel panel-default'>
                                      <!-- Default panel contents -->
                                      <div class='panel-heading'>Budget Contributions</div>
                                      {% if getBudget %}
                                          <!-- Table -->
                                          <table class="table">
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
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/workflow/budget_add/{{ id }}">Add Budget Contribution</a>
                                      </div>
                                    </div>
                            """),
                            ),
                        ),
                    ),

                Tab('Impact',
                    Fieldset(
                        '',
                        Div(
                            '',
                             HTML("""
                                    <div class='panel panel-default'>
                                      <!-- Default panel contents -->
                                      <div class='panel-heading'>Indicator</div>
                                      {% if getQuantitative %}
                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Targeted</th>
                                            <th>Achieved</th>
                                            <th>Indicator</th>
                                            <th>View</th>
                                            </tr>
                                            {% for item in getQuantitative %}
                                            <tr>
                                                <td>{{ item.targeted}}</td>
                                                <td>{{ item.achieved}}</td>
                                                <td>{{ item.description}}</td>
                                                <td><a href="/indicators/indicator_update/{{ item.indicator_id }}">{{ item.indicator}}<a/></td>
                                                <td><a class="output" data-toggle="modal" data-target="#myModal" href='/workflow/quantitative_update/{{ item.id }}/'>Edit</a> | <a class="output" href='/workflow/quantitative_delete/{{ item.id }}/' data-target="#myModal">Delete</a>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/workflow/quantitative_add/{{ id }}">Add Indicators</a>
                                      </div>
                                    </div>
                             """),
                        ),
                    ),
                    Fieldset(
                        '',AppendedText('progress_against_targets','%'),'actual_contribution','beneficiary_type', 'capacity_built', 'quality_assured','issues_and_challenges', 'lessons_learned',
                    ),
                ),

                Tab('Approval',
                    Fieldset('Approval',
                             'approval', 'approved_by',
                             Field('approval_remarks', rows="3", css_class='input-xlarge')
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
                            <a onclick="newPopup('/workflow/documentation_list/0/{{ id }}','Add New Documentation'); return false;" href="#" class="btn btn-sm btn-info">Add New Documentation</a>
                          </div>
                        </div>
                         """),
                ),
            ),

        )
        super(ProjectCompleteSimpleForm, self).__init__(*args, **kwargs)

        # override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['program'].queryset = WorkflowLevel1.objects.filter(funding_status="Funded", country__in=countries)
        #self.fields['project_agreement'].queryset = ProjectAgreement.objects.filter(program__country__in = countries)
        self.fields['approved_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()

        # override the office queryset to use request.user for country
        self.fields['office'].queryset = Office.objects.filter(province__country__in=countries)

        # override the community queryset to use request.user for country
        self.fields['site'].queryset = SiteProfile.objects.filter(country__in=countries)

        # override the stakeholder queryset to use request.user for country
        self.fields['stakeholder'].queryset = Stakeholder.objects.filter(country__in=countries)

        if not 'Approver' in self.request.user.groups.values_list('name', flat=True):
            APPROVALS = (
                ('in progress', 'in progress'),
                ('awaiting approval', 'awaiting approval'),
                ('rejected', 'rejected'),
            )
            self.fields['approval'].choices = APPROVALS
            self.fields['approved_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_remarks'].widget.attrs['disabled'] = "disabled"
            self.fields['approval'].help_text = "Approval level permissions required"
            self.fields['project_agreement'].widget.attrs['disabled'] = "disabled"


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
                        'name', 'type', 'office','status',
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
                    Fieldset('Households',
                        'total_num_households','avg_household_size', 'male_0_5', 'female_0_5', 'male_6_9', 'female_6_9',
                        'male_10_14', 'female_10_14','male_15_19', 'female_15_19', 'male_20_24', 'female_20_24', 'male_25_34', 'female_25_34', 'male_35_49', 'female_35_49', 'male_over_50', 'female_over_50', 'total_population',
                    ),
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
                        <td>{{ item.project_name }}</td>
                        <td>{{ item.program.name }}</td>
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
        self.fields['office'].queryset = Office.objects.filter(province__country__in=countries)
        self.fields['province'].queryset = Province.objects.filter(country__in=countries)
        self.fields['approved_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()
        self.fields['filled_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()


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
                'project','program',

            FormActions(
                Submit('submit', 'Save', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )

        super(DocumentationForm, self).__init__(*args, **kwargs)

        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['project'].queryset = WorkflowLevel2.objects.filter(program__country__in=countries)
        self.fields['program'].queryset = WorkflowLevel1.objects.filter(country__in=countries)


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

                'targeted','achieved','indicator','agreement','program'

        )

        super(QuantitativeOutputsForm, self).__init__(*args, **kwargs)

        countries = getCountry(self.request.user)

        self.fields['indicator'].queryset = Indicator.objects.filter(program__id=kwargs['initial']['program'])
        self.fields['agreement'].queryset = WorkflowLevel2.objects.filter(program__country__in=countries)


class BenchmarkForm(forms.ModelForm):

    class Meta:
        model = WorkflowLevel3
        exclude = ['create_date', 'edit_date']

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.request = kwargs.pop('request')
        self.agreement = kwargs.pop('agreement')
        self.complete = kwargs.pop('complete')
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_tag = False

        if "benchmark_complete" in self.request.path:
            self.helper.layout = Layout(
                Field('description', rows="3", css_class='input-xlarge'),'site','est_start_date','est_end_date',
                Field('actual_start_date', css_class="act_datepicker", id="actual_start_date_id"),
                 Field('actual_end_date', css_class="act_datepicker", id="actual_end_date_id"),'budget','cost','agreement','complete',
            )
        else:
            self.helper.layout = Layout(
                Field('description', rows="3", css_class='input-xlarge'),'site','est_start_date','est_end_date','budget','agreement',
            )
        super(BenchmarkForm, self).__init__(*args, **kwargs)

        # override the site queryset to use request.user for country
        self.fields['site'].queryset = SiteProfile.objects.all().filter(projectagreement__id=self.agreement)


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
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Details',
                    Fieldset('Details',
                        'name', 'type', 'contact', HTML("""<a onclick="window.open('/workflow/contact_add/0/').focus();">Add New Contact</a>"""), 'country', 'sector', PrependedText('stakeholder_register',''), 'formal_relationship_document', 'vetting_document',
                    ),
                ),

                Tab('Approvals',
                    Fieldset('Approval',
                        'approval','approved_by','filled_by',
                    ),
                ),
            ),
        )

        super(StakeholderForm, self).__init__(*args, **kwargs)

        countries = getCountry(self.request.user)
        users = TolaUser.objects.filter(country__in=countries)
        self.fields['contact'].queryset = Contact.objects.filter(country__in=countries)
        self.fields['country'].queryset = countries
        self.fields['approved_by'].queryset = users
        self.fields['filled_by'].queryset = users
        self.fields['formal_relationship_document'].queryset = Documentation.objects.filter(program__country__in=countries)
        self.fields['vetting_document'].queryset = Documentation.objects.filter(program__country__in=countries)


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
