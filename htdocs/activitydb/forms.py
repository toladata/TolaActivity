from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset, Field
from functools import partial
from widgets import GoogleMapsWidget
import floppyforms.__future__ as forms
from django.contrib.auth.models import Permission, User, Group
from .models import ProgramDashboard, ProjectAgreement, ProjectComplete, Sector, Program, Community, Documentation, Benchmarks, Monitor, TrainingAttendance, Beneficiary, Budget, Capacity, Evaluate, Office, Checklist, ChecklistItem
from indicators.models import CollectedData
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
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


class ProgramDashboardForm(forms.ModelForm):

    class Meta:
        model = ProgramDashboard
        fields = '__all__'


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

    def save(self, *args, **kwargs):
        # Commit is already set to false
        obj = super(BudgetForm, self).save(*args, **kwargs)
        return obj


class ProjectAgreementCreateForm(forms.ModelForm):

    class Meta:
        model = ProjectAgreement
        fields = '__all__'

    program = forms.ModelChoiceField(queryset=Program.objects.filter(country='1'), required=False)

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
        self.helper.layout = Layout(

            HTML("""<p>Create a Summary first then add additional fields after saving</p><br/>"""),
            TabHolder(
                   Tab('Executive Summary',
                        Fieldset('Program', 'activity_code', 'office', 'sector','program', 'project_name', 'project_activity',
                                 'project_type','mc_staff_responsible','expected_start_date','expected_end_date','expected_duration',
                        ),

                    ),
                    Tab('Community Proposal',
                        Fieldset(
                            'Community',
                            'community_rep','community_rep_contact', 'community_mobilizer','community_mobilizer_contact'
                            'community_proposal','community',PrependedText('has_rej_letter', ''), 'rejection_letter',
                        ),
                        Fieldset(
                            'Partners',
                            PrependedText('partners',''), 'name_of_partners', 'external_stakeholder_list',
                        ),
                    ),
            ),

            HTML("""<br/>"""),

        )
        super(ProjectAgreementCreateForm, self).__init__(*args, **kwargs)

        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['program'].queryset = Program.objects.filter(funding_status="Funded", country__in=countries)

        #override the office queryset to use request.user for country
        self.fields['office'].queryset = Office.objects.filter(province__country__in=countries)

        #override the community queryset to use request.user for country
        self.fields['community'].queryset = Community.objects.filter(country__in=countries)


class ProjectAgreementForm(forms.ModelForm):

    class Meta:
        model = ProjectAgreement
        fields = '__all__'

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    expected_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    expected_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    estimation_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    reviewed_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    approved_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    me_reviewed_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    checked_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    estimated_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    finance_reviewed_by_date = forms.DateField(widget=DatePicker.DateInput(), required=False)

    program = forms.ModelChoiceField(queryset=Program.objects.filter(country='1'), required=False)

    documentation_government_approval = forms.FileField(required=False)
    documentation_community_approval = forms.FileField(required=False)

    program_objectives = forms.CharField(label="What program objectives does this help?",help_text="This comes from your Logframe", widget=forms.Textarea, required=False)
    mc_objectives = forms.CharField(label="What MC strategic Objectives does this help fulfill?",help_text="This comes from MC Strategic Objectives", widget=forms.Textarea, required=False)
    effect_or_impact = forms.CharField(help_text="Please do not include outputs and keep less than 120 words", widget=forms.Textarea, required=False)
    justification_background = forms.CharField(help_text="As someone would write a background and problem statement in a proposal, this should be described here. What is the situation in this community where the project is proposed and what is the problem facing them that this project will help solve", widget=forms.Textarea, required=False)
    justification_description_community_selection = forms.CharField(help_text="How was this community selected for this project. It may be it was already selected as part of the project (like CDP-2, KIWI-2), but others may need to describe, out of an entire cluster, why this community? This can't be just 'because they wanted it', or 'because they are poor.' It must refer to a needs assessment, some kind of selection criteria, maybe identification by the government, or some formal process.", widget=forms.Textarea, required=False)
    description_of_project_activities = forms.CharField(help_text="How was this community selected for this project. It may be it was already selected as part of the project (like CDP-2, KIWI-2), but others may need to describe, out of an entire cluster, why this community? This can't be just 'because they wanted it', or 'because they are poor.' It must refer to a needs assessment, some kind of selection criteria, maybe identification by the government, or some formal process.", widget=forms.Textarea, required=False)
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
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Executive Summary',
                    Fieldset('Program', 'activity_code', 'office', 'sector','program', 'project_name', 'project_activity',
                             'project_type','mc_staff_responsible','expected_start_date','expected_end_date','expected_duration',
                    ),

                ),
                Tab('Community Proposal',
                    Fieldset(
                        'Community',
                        'community_rep','community_rep_contact', 'community_mobilizer','community_mobilizer_contact'
                        'community_proposal','community',PrependedText('has_rej_letter', ''), 'rejection_letter',
                    ),
                    Fieldset(
                        'Partners',
                        PrependedText('partners',''), 'name_of_partners', 'external_stakeholder_list',
                    ),
                ),
                Tab('Budget',
                     Fieldset(
                        'Budget',
                        PrependedAppendedText('total_estimated_budget','$', '.00'), PrependedAppendedText('mc_estimated_budget','$', '.00'),
                        'estimation_date','other_budget','project_type_other',
                    ),
                    Fieldset("Other Budget Contributions:",
                        MultiField(
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
                                            <th>Proposed Value</th>
                                            <th>View</th>
                                            </tr>
                                            {% for item in getBudget %}
                                            <tr>
                                                <td>{{ item.contributor}}</td>
                                                <td>{{ item.description_of_contribution}}</td>
                                                <td>{{ item.proposed_value}}</td>
                                                <td><a class="output" data-toggle="modal" data-target="#myModal" href='/activitydb/budget_update/{{ item.id }}/'>Edit</a> | <a class="output" href='/activitydb/budget_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal" >Delete</a>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/activitydb/budget_add/{{ pk }}">Add Budget Contribution</a>
                                      </div>
                                    </div>
                                     """),
                        ),
                    ),

                ),

                Tab('Justification and Description',
                    Fieldset(
                        'Justification',
                        Field('program_objectives'),Field('mc_objectives'),Field('effect_or_impact'),
                        Field('justification_background', rows="3", css_class='input-xlarge'),
                        Field('justification_description_community_selection', rows="3", css_class='input-xlarge'),
                    ),
                     Fieldset(
                        'Description',
                        Field('description_of_project_activities', rows="3", css_class='input-xlarge'),
                        Field('description_of_government_involvement', rows="3", css_class='input-xlarge'),
                        'documentation_government_approval',
                        Field('description_of_community_involvement', rows="3", css_class='input-xlarge'),
                        'documentation_community_approval',

                    ),
                ),
                Tab('Planning',
                    Fieldset(
                        '',
                        MultiField(
                            '',
                             HTML("""
                                    <div class='panel panel-default'>
                                      <!-- Default panel contents -->
                                      <div class='panel-heading'>Indicator Evidence</div>
                                      {% if getQuantitative %}
                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Targeted</th>
                                            <th>Description</th>
                                            <th>Indicator</th>
                                            <th>View</th>
                                            </tr>
                                            {% for item in getQuantitative %}
                                            <tr>
                                                <td>{{ item.targeted}}</td>
                                                <td>{{ item.description}}</td>
                                                <td>{{ item.indicator}}</td>
                                                <td><a class="output" data-toggle="modal" data-target="#myModal" href='/activitydb/quantitative_update/{{ item.id }}/'>Edit</a> | <a class="output" href='/activitydb/quantitative_delete/{{ item.id }}/' data-target="#myModal">Delete</a>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/activitydb/quantitative_add/{{ pk }}">Add Quantitative Outputs</a>
                                      </div>
                                    </div>
                                     """),

                             HTML("""

                                    <div class='panel panel-default'>
                                      <!-- Default panel contents -->
                                      <div class='panel-heading'>Benchmarks</div>
                                      {% if getBenchmark %}
                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Percent Complete</th>
                                            <th>Percent Cumlative Completion</th>
                                            <th>Description</th>
                                            <th>View</th>
                                            </tr>
                                            {% for item in getBenchmark %}
                                            <tr>
                                                <td>{{ item.percent_complete}}</td>
                                                <td>{{ item.percent_cumulative}}</td>
                                                <td>{{ item.description}}</td>
                                                <td><a class="benchmarks" data-toggle="modal" data-target="#myModal" href='/activitydb/benchmark_update/{{ item.id }}/'>Edit</a> | <a class="benchmarks" href='/activitydb/benchmark_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal">Delete</a></td>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="benchmarks" data-toggle="modal" data-target="#myModal" href="/activitydb/benchmark_add/{{ pk }}">Add Benchmarks</a>
                                      </div>
                                    </div>
                                     """),

                            'capacity',
                        ),
                    ),
                ),
                 Tab('M&E',
                    Fieldset(
                        '',
                        MultiField(
                            '',
                            HTML("""

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
                                                <td><a class="monitoring" data-toggle="modal" data-target="#myModal" href='/activitydb/monitor_update/{{ item.id }}/'>Edit</a> | <a class="monitoring" href='/activitydb/monitor_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal">Delete</a>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="monitoring" data-toggle="modal" data-target="#myModal" href="/activitydb/monitor_add/{{ pk }}">Add Monitoring Data</a>
                                      </div>
                                    </div>
                                     """),

                            'evaluate',
                        ),
                    ),
                ),


                Tab('Project Impact',
                     Fieldset(
                        'Beneficiaries',
                        'beneficiary_type','estimated_num_direct_beneficiaries', 'average_household_size', 'estimated_num_indirect_beneficiaries',
                     ),
                     Fieldset(
                         'Training',
                         'estimate_male_trained','estimate_female_trained','estimate_total_trained','estimate_trainings',
                     ),
                     Fieldset(
                         'Distribution',
                         'distribution_type','distribution_uom','distribution_estimate',
                     ),
                     Fieldset(
                         'Cash For Work',
                         'cfw_estimate_male','cfw_estimate_female','cfw_estimate_total','cfw_estimate_project_days','cfw_estimate_person_days',
                         'cfw_estimate_cost_materials','cfw_estimate_wages_budgeted',
                     ),
                ),
                Tab('Approval',
                    Fieldset('Approval',
                             'approval', 'estimated_by','estimated_by_date', 'checked_by','checked_by_date','reviewed_by','reviewed_by_date',
                             'finance_reviewed_by','finance_reviewed_by_date','me_reviewed_by','me_reviewed_by_date','approved_by', 'approved_by_date', 'approval_submitted_by',
                             Field('approval_remarks', rows="3", css_class='input-xlarge')
                    ),
                ),
            ),

            HTML("""<br/>"""),

        )
        super(ProjectAgreementForm, self).__init__(*args, **kwargs)

        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['program'].queryset = Program.objects.filter(funding_status="Funded", country__in=countries)

        #override the office queryset to use request.user for country
        self.fields['office'].queryset = Office.objects.filter(province__country__in=countries)

        #override the community queryset to use request.user for country
        self.fields['community'].queryset = Community.objects.filter(country__in=countries)

        if not 'Approver' in self.request.user.groups.values_list('name', flat=True):
            self.fields['approval'].widget.attrs['disabled'] = "disabled"
            self.fields['approved_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_submitted_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_remarks'].widget.attrs['disabled'] = "disabled"
            self.fields['approval'].help_text = "Approval level permissions required"


class ProjectCompleteCreateForm(forms.ModelForm):

    class Meta:
        model = ProjectComplete
        fields = '__all__'

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    expected_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    expected_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)

    program = forms.ModelChoiceField(queryset=Program.objects.filter(funding_status="Funded"))

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
                    Fieldset('Program', 'program', 'project_proposal', 'project_agreement', 'activity_code', 'office', 'sector', 'project_name'
                    ),
                    Fieldset(
                        'Dates',
                        'expected_start_date','expected_end_date', 'expected_duration', 'actual_start_date', 'actual_end_date', 'actual_duration',
                        PrependedText('on_time', ''), 'no_explanation',

                    ),
                ),
            ),

        )
        super(ProjectCompleteCreateForm, self).__init__(*args, **kwargs)

        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['program'].queryset = Program.objects.filter(funding_status="Funded", country__in=countries)

        #override the office queryset to use request.user for country
        self.fields['office'].queryset = Office.objects.filter(province__country__in=countries)


class ProjectCompleteForm(forms.ModelForm):

    class Meta:
        model = ProjectComplete
        fields = '__all__'

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    expected_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    expected_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_start_date = forms.DateField(widget=DatePicker.DateInput(), required=False)
    actual_end_date = forms.DateField(widget=DatePicker.DateInput(), required=False)

    program = forms.ModelChoiceField(queryset=Program.objects.filter(funding_status="Funded"))

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
                    Fieldset('Program', 'program', 'project_proposal', 'project_agreement', 'activity_code', 'office', 'sector', 'project_name'
                    ),
                    Fieldset(
                        'Dates',
                        'expected_start_date','expected_end_date', 'expected_duration', 'actual_start_date', 'actual_end_date', 'actual_duration',
                        PrependedText('on_time', ''), 'no_explanation',

                    ),
                ),
                Tab('Budget and Issues',
                    Fieldset(
                        'Budget',
                        'estimated_budget','actual_budget', 'budget_variance', 'explanation_of_variance', 'actual_contribution', 'direct_beneficiaries',
                    ),
                     Fieldset(
                        'Jobs',
                        'jobs_created','jobs_part_time','jobs_full_time','government_involvement','capacity_built',

                    ),
                     Fieldset(
                        'Issues',
                        'issues_and_challenges','lessons_learned','quantitative_outputs'

                    ),
                ),
                Tab('Budget Other',
                    Fieldset("Other Budget Contributions:",
                        MultiField(
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
                                            <th>Proposed Value</th>
                                            <th>View</th>
                                            </tr>
                                            {% for item in getBudget %}
                                            <tr>
                                                <td>{{ item.contributor}}</td>
                                                <td>{{ item.contributor_description}}</td>
                                                <td>{{ item.proposed_value}}</td>
                                                <td><a class="output" data-toggle="modal" data-target="#myModal" href='/activitydb/budget_update/{{ item.id }}/'>View</a> | <a class="output" href='/activitydb/budget_delete/{{ item.id }}/' data-toggle="modal" data-target="#myModal" >Delete</a>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                      {% endif %}
                                      <div class="panel-footer">
                                        <a class="output" data-toggle="modal" data-target="#myModal" href="/activitydb/budget_add/{{ pk }}">Add Budget Contribution</a>
                                      </div>
                                    </div>
                                     """),
                        ),
                    ),

                ),

                Tab('Approval',
                    Fieldset('Approval',
                             'approval', 'approved_by', 'approval_submitted_by',
                             Field('approval_remarks', rows="3", css_class='input-xlarge')
                    ),
                ),
            ),

        )
        super(ProjectCompleteForm, self).__init__(*args, **kwargs)

        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['program'].queryset = Program.objects.filter(funding_status="Funded", country__in=countries)

        #override the office queryset to use request.user for country
        self.fields['office'].queryset = Office.objects.filter(province__country__in=countries)

        #override the community queryset to use request.user for country
        self.fields['community'].queryset = Community.objects.filter(country__in=countries)

        if not 'Approver' in self.request.user.groups.values_list('name', flat=True):
            self.fields['approval'].widget.attrs['disabled'] = "disabled"
            self.fields['approved_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_submitted_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval_remarks'].widget.attrs['disabled'] = "disabled"
            self.fields['approval'].help_text = "Approval level permissions required"


class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        exclude = ['create_date', 'edit_date']

    map = forms.CharField(widget=GoogleMapsWidget(
        attrs={'width': 700, 'height': 400, 'longitude': 'longitude', 'latitude': 'latitude'}), required=False)

    date_of_firstcontact = forms.DateField(widget=DatePicker.DateInput(), required=False)

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
        self.helper.layout = Layout(

            HTML("""<br/>"""),
            TabHolder(
                Tab('Profile',
                    Fieldset('Description',
                        'code', 'name', 'type', 'office', PrependedText('existing_village',''), 'existing_village_descr',
                    ),
                    Fieldset('Community',
                        'community_leader', 'head_of_institution', 'date_of_firstcontact', 'contact_number', 'num_members',
                    ),
                ),
                Tab('Location',
                    Fieldset('Places',
                        'country','province','district','village','latitude','longitude','altitude', 'precision',
                    ),
                    Fieldset('Map',
                        'map',
                    ),
                    Fieldset('Distances',
                        'distance_district_capital','distance_site_camp','distance_field_office',
                    ),
                ),
                Tab('For Geographic Communities',
                    Fieldset('Households',
                        'total_num_households','avg_household_size', 'male_0_14', 'female_0_14', 'male_15_24', 'female_15_24',
                        'male_25_59', 'female_25_59', 'male_over_60', 'female_over_60', 'total_population',
                    ),
                    Fieldset('Land',
                        'total_land','total_agricultural_land','total_rainfed_land','total_horticultural_land',
                        'population_owning_land', 'avg_landholding_size', 'population_owning_livestock','animal_type'
                    ),
                    Fieldset('Literacy',
                        'total_num_literate','literate_males','literate_females','literacy_rate',
                    ),
                ),
                Tab('Approval',
                    Fieldset('Approval',
                        'approval', 'filled_by', 'location_verified_by', 'approved_by',
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
              <div class='panel-heading'>Projects in this Community</div>
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
                        <td><a target="_new" href='/activitydb/projectagreement_detail/{{ item.id }}/'>View</a>
                    </tr>
                    {% endfor %}
                  </table>
              {% endif %}
            </div>
             """),
        )

        super(CommunityForm, self).__init__(*args, **kwargs)

        #override the office queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['office'].queryset = Office.objects.filter(province__country__in=countries)


        if not 'Approver' in self.request.user.groups.values_list('name', flat=True):
            self.fields['approval'].widget.attrs['disabled'] = "disabled"
            self.fields['approved_by'].widget.attrs['disabled'] = "disabled"
            self.fields['approval'].help_text = "Approval level permissions required"


class DocumentationForm(forms.ModelForm):

    class Meta:
        model = Documentation
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
        self.helper.layout = Layout(

            HTML("""<br/>"""),

                'name', 'url', Field('description', rows="3", css_class='input-xlarge'),'silo',
                'project',

            FormActions(
                Submit('submit', 'Save', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )

        super(DocumentationForm, self).__init__(*args, **kwargs)


class QuantitativeOutputsForm(forms.ModelForm):

    class Meta:
        model = CollectedData
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
        self.helper.form_tag = False
        self.helper.layout = Layout(

                'targeted', 'indicator', Field('description', rows="3", css_class='input-xlarge'),'date_collected', 'agreement',

        )

        super(QuantitativeOutputsForm, self).__init__(*args, **kwargs)


class BenchmarkForm(forms.ModelForm):

    class Meta:
        model = Benchmarks
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
        self.helper.form_tag = False
        self.helper.layout = Layout(

                'percent_complete', 'percent_cumulative', Field('description', rows="3", css_class='input-xlarge'), 'agreement',
                'file_field'

        )

        super(BenchmarkForm, self).__init__(*args, **kwargs)


class MonitorForm(forms.ModelForm):

    class Meta:
        model = Monitor
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
        self.helper.form_tag = False
        self.helper.layout = Layout(

            HTML("""<br/>"""),

                'responsible_person', 'frequency', Field('type', rows="3", css_class='input-xlarge'), 'agreement',

        )

        super(MonitorForm, self).__init__(*args, **kwargs)


class ChecklistForm(forms.ModelForm):

    class Meta:
        model = Checklist
        exclude = ['create_date', 'edit_date']

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

        super(ChecklistForm, self).__init__(*args, **kwargs)

        countries = getCountry(self.request.user)
        #override the community queryset to use request.user for country
        self.fields['item'].queryset = ChecklistItem.objects.filter(country__in=countries)


class TrainingAttendanceForm(forms.ModelForm):

    class Meta:
        model = TrainingAttendance
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

        super(TrainingAttendanceForm, self).__init__(*args, **kwargs)


class BeneficiaryForm(forms.ModelForm):

    class Meta:
        model = Beneficiary
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

        super(BeneficiaryForm, self).__init__(*args, **kwargs)


class FilterForm(forms.Form):
    fields = "search"
    search = forms.CharField(required=False)
    helper = FormHelper()
    helper.form_method = 'get'
    helper.form_class = 'form-inline'
    helper.layout = Layout(FieldWithButtons('search', StrictButton('Submit', type='submit', css_class='btn-primary')))


class ProjectCompleteTable(forms.ModelForm):

    class Meta:
        model = ProjectComplete
        fields = '__all__'