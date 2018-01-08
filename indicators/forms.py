from django.core.urlresolvers import reverse_lazy
from indicators.models import Indicator, PeriodicTarget, CollectedData, Objective, StrategicObjective, TolaTable, DisaggregationType
from workflow.models import Program, SiteProfile, Documentation, ProjectAgreement, TolaUser
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
            #{'program': forms.Select()}
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
        self.program = kwargs.pop('program')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse_lazy('indicator_update', kwargs={'pk': indicator.id})
        self.helper.form_id = 'indicator_update_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_tag = False
        self.helper.layout = Layout(

            TabHolder(
                Tab('Summary',
                     Fieldset('',
                        'program','sector','objectives','strategic_objectives',
                        ),
                ),
                Tab('Performance',
                     Fieldset('',
                        'name', 'level', 'number', 'source', 'definition', 'justification', 'disaggregation','indicator_type',PrependedText('key_performance_indicator', False)
                        ),
                ),
                Tab('Targets',
                    Fieldset('',
                             'unit_of_measure', 'lop_target', 'rationale_for_target', 'baseline', 'target_frequency', 'target_frequency_start', 'target_frequency_custom', 'target_frequency_num_periods'
                             ),
                    Fieldset('',
                        HTML("""
                            <div id="div_id_create_targets_btn" class="form-group">
                                <div class="controls col-sm-offset-4 col-sm-2">
                                    <button id="create_targets_btn" class="btn btn-primary">Create targets</button>
                                </div>
                            </div>
                        """)
                    ),
                    Fieldset('',
                        HTML("""
                            <div class="container-fluid" style="background-color: #F5F5F5; margin: 0px -30px -32px -30px;">
                                <div class="row">
                                    <div class="col-sm-offset-2 col-sm-8" style="padding-left: 1px;">
                                        <h4>Periodic Targets</h4>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-offset-2 col-sm-8" style="background-color: #FFFFFF; margin-top:1px; margin-bottom:5px;">
                                        <table class="table table-condensed" id="periodic_targets_table">
                                            <tbody>
                                                {% for pt in periodic_targets %}
                                                    <tr id="{{pt.pk}}">
                                                        <td style="padding:1px; border-top: 0px; border-bottom: 1px solid #ddd; vertical-align: middle;">
                                                            {% if forloop.last %}
                                                                <a href="{% url 'pt_delete' pt.id %}" id="deleteLastPT" class="detelebtn" style="color:red;"><span class=" glyphicon glyphicon-remove-circle"></span></a>
                                                            {% endif %}
                                                        </td>
                                                        <td style="padding:1px; border-top: 0px; border-bottom: 1px solid #ddd; vertical-align: middle;">
                                                            <div style="line-height:1;"><strong>{{ pt.period }}</strong></div>
                                                            <div style="line-height:0.8;"><small>{{ pt.start_date }} - {{ pt.end_date}}</small></div>
                                                        </td>
                                                        <td align="right" style="padding:1px; border-top: 0px; border-bottom: 1px solid #ddd; vertical-align: middle;">
                                                            <input type="number" id="pt-{{ pt.id }}" name="{{ pt.period }}" value="{{ pt.target }}" class="form-control" style="width: 50%;">
                                                        </td>
                                                    </tr>
                                                {% endfor %}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-offset-2 col-sm-8" style="padding-left: 1px; margin-bottom:20px;">
                                        <a href="#" style="padding-left: 1px;" class="button btn-lg btn-link"><span class=" glyphicon glyphicon-plus-sign"></span> Add a target</a>
                                    </div>
                                </div>
                            </div>
                        """),
                    ),
                ),
                Tab('Data Acquisition',
                    Fieldset('',
                        'means_of_verification','data_collection_method', 'data_collection_frequency', 'data_points', 'responsible_person',
                        ),
                ),
                Tab('Analysis and Reporting',
                    Fieldset('',
                        'method_of_analysis','information_use', 'reporting_frequency', 'quality_assurance', 'data_issues', 'indicator_changes', 'comments','notes'
                    ),
                ),
                Tab('Approval',
                    Fieldset('',
                        'approval_submitted_by', 'approved_by',
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

            # HTML("""<hr/>"""),
            # FormActions(
            #     Submit('submit', 'Save', css_class='btn-default'),
            #     Reset('reset', 'Reset', css_class='btn-default')
            # )
        )

        super(IndicatorForm, self).__init__(*args, **kwargs)

        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        self.fields['program'].queryset = Program.objects.filter(funding_status="Funded", country__in=countries)
        self.fields['disaggregation'].queryset = DisaggregationType.objects.filter(country__in=countries).filter(standard=False)
        self.fields['objectives'].queryset = Objective.objects.all().filter(program__id__in=self.program)
        self.fields['strategic_objectives'].queryset = StrategicObjective.objects.filter(country__in=countries)
        self.fields['approved_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()
        self.fields['approval_submitted_by'].queryset = TolaUser.objects.filter(country__in=countries).distinct()
        self.fields['program'].widget.attrs['readonly'] = "readonly"
        self.fields['target_frequency_start'].widget = DatePicker.DateInput()
        # self.fields['target_frequency_start'].help_text = 'This field is required'
        # self.fields['target_frequency'].required = False
        if self.instance.target_frequency:
            self.fields['target_frequency'].widget.attrs['readonly'] = "readonly"
            #self.fields['target_frequency'].widget.attrs['disabled'] = "disabled"
            self.fields['target_frequency_custom'].widget = forms.HiddenInput()
            self.fields['target_frequency_start'].widget = forms.HiddenInput()
            self.fields['target_frequency_num_periods'].widget = forms.HiddenInput()

class CollectedDataForm(forms.ModelForm):

    class Meta:
        model = CollectedData
        exclude = ['create_date', 'edit_date']

    program2 =  forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly', 'label': 'Program'}) )
    indicator2 = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly', 'label': 'Indicator'}) )
    date_collected = forms.DateField(widget=DatePicker.DateInput(), required=True)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        self.helper = FormHelper()
        self.request = kwargs.pop('request')
        self.program = kwargs.pop('program')
        self.indicator = kwargs.pop('indicator', None)
        self.tola_table = kwargs.pop('tola_table')
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.form_action = reverse_lazy('collecteddata_update' if instance else 'collecteddata_add', kwargs={'pk': instance.id} if instance else {'program': self.program, 'indicator': self.indicator})
        self.helper.form_id = 'collecteddata_update_form'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_tag = True
        self.helper.layout = Layout(

            HTML("""<br/>"""),

            Fieldset('Collected Data',
                'program', 'program2', 'indicator', 'indicator2', 'site', 'date_collected', 'periodic_target', 'achieved', 'description',

            ),

            HTML("""<br/>"""),

            Fieldset('Evidence',
                'agreement', 'evidence','tola_table','update_count_tola_table',
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

        #override the program queryset to use request.user for country
        self.fields['evidence'].queryset = Documentation.objects.filter(program=self.program)

        #override the program queryset to use request.user for country
        self.fields['agreement'].queryset = ProjectAgreement.objects.filter(program=self.program)
        self.fields['agreement'].label = "Project"

        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        #self.fields['program'].queryset = Program.objects.filter(funding_status="Funded", country__in=countries).distinct()
        try:
            int(self.program)
            self.program = Program.objects.get(id=self.program)
        except TypeError:
            pass

        self.fields['periodic_target'].queryset = PeriodicTarget.objects.filter(indicator=self.indicator)

        self.fields['program2'].initial = self.program
        self.fields['program2'].label = "Program"

        try:
            int(self.indicator)
            self.indicator = Indicator.objects.get(id=self.indicator)
        except TypeError:
            pass

        self.fields['indicator2'].initial = self.indicator
        self.fields['indicator2'].label = "Indicator"
        self.fields['program'].widget = forms.HiddenInput()
        self.fields['indicator'].widget = forms.HiddenInput()
        #override the program queryset to use request.user for country
        self.fields['site'].queryset = SiteProfile.objects.filter(country__in=countries)

        #self.fields['indicator'].queryset = Indicator.objects.filter(name__isnull=False, program__country__in=countries)
        self.fields['tola_table'].queryset = TolaTable.objects.filter(Q(owner=self.request.user) | Q(id=self.tola_table))

