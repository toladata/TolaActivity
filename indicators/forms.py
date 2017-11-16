from django.core.urlresolvers import reverse_lazy
from indicators.models import Indicator, PeriodicTarget, CollectedData, Objective, StrategicObjective, TolaTable, DisaggregationType
from workflow.models import WorkflowLevel1, SiteProfile, Documentation, WorkflowLevel2, TolaUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset
from functools import partial
from django import forms
from tola.util import getCountry
from django.db.models import Q


class DatePicker(forms.DateInput):
    """
    Use in form to create a Jquery datepicker element
    """
    template_name = 'datepicker.html'

    DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class IndicatorForm(forms.ModelForm):

    class Meta:
        model = Indicator
        exclude = ['create_date','edit_date']
        widgets = {
            'definition': forms.Textarea(attrs={'rows':4}),
            'justification': forms.Textarea(attrs={'rows':4}),
            'quality_assurance': forms.Textarea(attrs={'rows':4}),
            'data_issues': forms.Textarea(attrs={'rows':4}),
            'indicator_changes': forms.Textarea(attrs={'rows':4}),
            'comments': forms.Textarea(attrs={'rows':4}),
            'notes': forms.Textarea(attrs={'rows':4}),
            'rationale_for_target': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        #get the user object to check permissions with
        indicator = kwargs.get('instance', None)
        self.request = kwargs.pop('request')
        self.workflowlevel1 = kwargs.pop('workflowlevel1')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('indicator_update', kwargs={'pk': indicator.id})
        self.helper.form_id = 'indicator_update_form'
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
                Tab('Summary',
                     Fieldset('',
                        'workflowlevel1','sector','objectives','strategic_objectives', 'country',
                        ),
                ),
                Tab('Performance',
                     Fieldset('Performance',
                        'name', 'type', 'level', 'number', 'source', 'definition', 'unit_of_measure', 'justification', 'disaggregation','indicator_type',PrependedText('key_performance_indicator','')
                        ),
                ),
                Tab('Targets',
                    Fieldset('Targets',
                             'baseline','lop_target', 'rationale_for_target',
                             ),
                    Div("",
                        HTML("""<br/>
                            <div class='panel panel-default'>
                                <div class='panel-heading'>
                                    Periodic Targets
                                    <a class="pull-right" href="#" onclick="addPeriodicTarget()";>Add new Periodic Target</a>
                                </div>
                                <table class="table" id="periodic_targets_table">
                                    <thead>
                                        <tr>
                                            <th>Period</th>
                                            <th>Target</th>
                                            <th></th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in periodic_targets %}
                                            <tr id="{{item.id}}">
                                                <td><input type="text" name="period-{{ item.id }}" value="{{ item.period }}" class="textinput textInput form-control"></td>
                                                <td><input type="text" name="target-{{ item.id }}" value="{{ item.target }}" class="textinput textInput form-control"></td>
                                                <td style="vertical-align:middle">
                                                <a href="{% url 'pt_delete' item.id %}" class="detelebtn" style="color:red;"><span class="glyphicon glyphicon-trash"></span></a>
                                                </td>
                                            </tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                        """),
                    ),
                ),
                Tab('Data Acquisition',
                    Fieldset('Data Acquisition',
                        'means_of_verification','data_collection_method', 'data_collection_frequency', 'data_points', 'responsible_person',
                        ),
                ),
                Tab('Analysis and Reporting',
                    Fieldset('Analysis and Reporting',
                        'method_of_analysis','information_use', 'reporting_frequency', 'quality_assurance', 'data_issues', 'indicator_changes', 'comments','notes'
                    ),
                ),
                Tab('Approval',
                    Fieldset('Approval',
                        'approval', 'approval_submitted_by', 'approved_by',
                    ),
                ),
            ),
            HTML("""
                  {% if getExternalServiceRecord %}
                      <br/>
                      <div class='panel panel-default'>
                      <!-- Default panel contents -->
                      <div class='panel-heading'>External Indicator Service</div>
                          <!-- Table -->
                          <table class="table">
                           <tr>
                             <th>Service Name</th>
                             <th>View Guidance</th>
                           </tr>
                        {% for item in getExternalServiceRecord %}
                           <tr>
                            <td>{{ item.external_service.name }}</td>
                            <td><a target="_new" href='{{ item.full_url }}'>View</a>
                           </tr>
                        {% endfor %}
                         </table>
                      </div>
                  {% endif %}
             """),

            HTML("""<br/>"""),
            FormActions(
                Submit('submit', 'Save', css_class='btn-default'),
                Submit('_addanother', 'Save & Add Another >>', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )

        super(IndicatorForm, self).__init__(*args, **kwargs)

        #override the country queryset to use request.user for country
        countries = getCountry(self.request.user)
        organization_id = TolaUser.objects.values_list(
            'organization_id', flat=True).get(user=self.request.user)
        self.fields['workflowlevel1'].queryset = WorkflowLevel1.objects.filter(country__in=countries)
        self.fields['disaggregation'].queryset = \
            DisaggregationType.objects.filter(
                organization_id=organization_id, standard=False)
        self.fields['objectives'].queryset = Objective.objects.all().filter(workflowlevel1__id__in=self.workflowlevel1)
        self.fields['strategic_objectives'].queryset = StrategicObjective.objects.filter(country__in=countries)
        self.fields['approved_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()
        self.fields['approval_submitted_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()
        self.fields['workflowlevel1'].widget.attrs['readonly'] = "readonly"

class CollectedDataForm(forms.ModelForm):

    class Meta:
        model = CollectedData
        exclude = ['create_date', 'edit_date']

    indicator2 = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly', 'label': 'Indicator'}) )
    date_collected = forms.DateField(widget=DatePicker.DateInput(), required=True)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        self.helper = FormHelper()
        self.request = kwargs.pop('request')
        self.workflowlevel1 = kwargs.pop('workflowlevel1')
        self.indicator = kwargs.pop('indicator')
        self.tola_table = kwargs.pop('tola_table')
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.form_action = reverse_lazy('collecteddata_update' if instance else 'collecteddata_add', kwargs={'pk': instance.id} if instance else {'workflowlevel1': self.workflowlevel1, 'indicator': self.indicator})
        self.helper.form_id = 'collecteddata_update_form'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_tag = True
        self.helper.layout = Layout(

            HTML("""<br/>"""),

            Fieldset('Collected Data',
                'workflowlevel1', 'indicator', 'indicator2', 'site', 'date_collected', 'periodic_target', 'achieved', 'description',

            ),

            HTML("""<br/>"""),

            Fieldset('Evidence',
                'workflowlevel2','method','evidence','tola_table','update_count_tola_table',
                HTML("""<a class="output" data-toggle="modal" data-target="#tolatablemodal" href="/indicators/collecteddata_import/">Import Evidence From Tola Tables</a>"""),

            ),

                Div(
                        HTML("""<br/>
                                {% if getDisaggregationLabelStandard and not getDisaggregationValueStandard %}
                                    <div class='panel panel-default'>
                                        <!-- Default panel contents -->
                                        <div class='panel-heading'>Standard Disaggregations</div>
                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Disaggregation Level</th>
                                            <th>Actuals</th>
                                            </tr>
                                            {% for item in getDisaggregationLabelStandard %}
                                            <tr>
                                                <td>{{ item.label }}</td>
                                                <td><input type="text" name="{{ item.id }}" value=""></td>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                    </div>
                                {% else %}
                                    {% if not getDisaggregationValueStandard %}
                                        <h4>Standard Disaggregation Levels Not Entered</h4>
                                        <p>Standard disaggregations are entered in the administrator for the entire organizations.  If you are not seeing
                                        any here, please contact your system administrator.</p>
                                    {% endif %}
                                {% endif %}
                                {% if getDisaggregationLabel and not getDisaggregationValue %}
                                    <div class='panel panel-default'>
                                        <!-- Default panel contents -->
                                        <div class='panel-heading'>New Disaggregations</div>
                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Disaggregation Level</th>
                                            <th>Actuals</th>
                                            </tr>
                                            {% for item in getDisaggregationLabel %}
                                            <tr>
                                                <td>{{ item.label }}</td>
                                                <td><input type="text" name="{{ item.id }}" value=""></td>
                                            </tr>
                                            {% endfor %}
                                          </table>
                                    </div>
                                {% else %}
                                    {% if not getDisaggregationValue %}
                                        <h4>Disaggregation Levels Not Entered For This Indicator</h4>
                                        <a href="/indicators/indicator_update/{{ indicator_id }}">Add a Disaggregation</a>
                                    {% endif %}
                                {% endif %}

                                {% if getDisaggregationValue %}
                                    <div class='panel panel-default'>
                                        <!-- Default panel contents -->
                                        <div class='panel-heading'>Existing Disaggregations</div>

                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Disaggregation Level</th>
                                            <th>Actuals</th>
                                            </tr>
                                            {% for item in getDisaggregationValue %}
                                            <tr>
                                                <td>{{ item.disaggregation_label.label }}</td>
                                                <td><input type="text" name="{{ item.disaggregation_label.id }}" value="{{ item.value }}"></td>
                                            </tr>
                                            {% endfor %}
                                          </table>

                                    </div>
                                {% endif %}

                                {% if getDisaggregationValueStandard %}
                                    <div class='panel panel-default'>
                                        <!-- Default panel contents -->
                                        <div class='panel-heading'>Existing Standard Disaggregations</div>

                                          <!-- Table -->
                                          <table class="table">
                                            <tr>
                                            <th>Disaggregation Level</th>
                                            <th>Actuals</th>
                                            </tr>
                                            {% for item in getDisaggregationValueStandard %}
                                            <tr>
                                                <td>{{ item.disaggregation_label.label }}</td>
                                                <td><input type="text" name="{{ item.disaggregation_label.id }}" value="{{ item.value }}"></td>
                                            </tr>
                                            {% endfor %}
                                          </table>

                                    </div>
                                {% endif %}
                             """),
                ),

            HTML("""<br/>"""),
            FormActions(
                Submit('submit', 'Save', css_class='btn-default'),
                Reset('reset', 'Reset', css_class='btn-warning')
            )
        )

        super(CollectedDataForm, self).__init__(*args, **kwargs)

        #override the evidence queryset to use request.user for country
        self.fields['evidence'].queryset = Documentation.objects.filter(workflowlevel1=self.workflowlevel1)

        #override the level2 queryset to use request.user for country
        self.fields['workflowlevel2'].queryset = WorkflowLevel2.objects.filter(workflowlevel1=self.workflowlevel1)

        #override the country queryset to use request.user for country
        countries = getCountry(self.request.user)
        try:
            int(self.workflowlevel1)
            self.workflowlevel1 = WorkflowLevel1.objects.get(id=self.workflowlevel1)
        except TypeError:
            pass

        self.fields['periodic_target'].queryset = PeriodicTarget.objects.filter(indicator=self.indicator)

        try:
            int(self.indicator)
            self.indicator = Indicator.objects.get(id=self.indicator)
        except TypeError:
            pass

        self.fields['indicator2'].initial = self.indicator
        self.fields['indicator2'].label = "Indicator"
        self.fields['workflowlevel1'].widget = forms.HiddenInput()
        self.fields['indicator'].widget = forms.HiddenInput()
        #override the site queryset to use request.user for country
        self.fields['site'].queryset = SiteProfile.objects.filter(country__in=countries)

        self.fields['tola_table'].queryset = TolaTable.objects.filter(Q(owner=self.request.user) | Q(id=self.tola_table))
