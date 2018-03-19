from django.core.urlresolvers import reverse_lazy
from indicators.models import Indicator, PeriodicTarget, CollectedData, Objective, StrategicObjective, TolaTable, DisaggregationType
from workflow.models import Program, SiteProfile, Documentation, ProjectComplete, TolaUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset, Div
from functools import partial
from django import forms
from tola.util import getCountry
from django.db.models import Q
from datetime import datetime

class DatePicker(forms.DateInput):
    """
    Use in form to create a Jquery datepicker element
    """
    template_name = 'datepicker.html'

    DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class IndicatorForm(forms.ModelForm):
    program2 =  forms.CharField(widget=forms.TextInput(
                        attrs={'readonly':'readonly', 'label': 'Program'}
                    ))
    program = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Indicator
        exclude = ['program', 'create_date','edit_date']
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
        indicator = kwargs.get('instance', None)
        self.request = kwargs.pop('request')
        self.programval = kwargs.pop('program')

        super(IndicatorForm, self).__init__(*args, **kwargs)
        self.fields['program2'].initial = indicator.programs
        self.fields['program'].initial = self.programval.id

        countries = getCountry(self.request.user)
        self.fields['disaggregation'].queryset = DisaggregationType.objects.filter(
            country__in=countries).filter(standard=False)
        self.fields['objectives'].queryset = Objective.objects.filter(
            program__id__in=[self.programval.id])
        self.fields['strategic_objectives'].queryset = StrategicObjective.objects.filter(
            country__in=countries)
        self.fields['approved_by'].queryset = TolaUser.objects.filter(
            country__in=countries).distinct()
        self.fields['approval_submitted_by'].queryset = TolaUser.objects.filter(
            country__in=countries).distinct()

        # self.fields['target_frequency_start'].widget = DatePicker.DateInput()
        self.fields['name'].required = True
        self.fields['unit_of_measure'].required = True
        self.fields['target_frequency'].required = True

        self.fields['target_frequency_start'].widget.attrs['class'] = 'monthPicker'
        if self.instance.target_frequency and self.instance.target_frequency != Indicator.LOP:
            self.fields['target_frequency'].widget.attrs['readonly'] = "readonly"

class CollectedDataForm(forms.ModelForm):

    class Meta:
        model = CollectedData
        exclude = ['create_date', 'edit_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }
    def clean_date_collected(self):
        date_collected = self.cleaned_data['date_collected']
        date_collected = datetime.strftime(date_collected, '%Y-%m-%d')
        return date_collected

    program2 =  forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly', 'label': 'Program'}) )
    indicator2 = forms.CharField( widget=forms.TextInput(attrs={'readonly':'readonly', 'label': 'Indicator'}) )
    target_frequency = forms.CharField()
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
        self.helper.label_class = 'col-sm-4'
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
                'program', 'program2', 'indicator', 'indicator2', 'target_frequency', 'site', 'date_collected', 'periodic_target', 'achieved', 'description',

            ),
            Fieldset('Evidence',
                'complete', 'evidence','tola_table','update_count_tola_table',
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
        self.fields['complete'].queryset = ProjectComplete.objects.filter(program=self.program)
        self.fields['complete'].label = "Project"

        #override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        #self.fields['program'].queryset = Program.objects.filter(funding_status="Funded", country__in=countries).distinct()
        try:
            int(self.program)
            self.program = Program.objects.get(id=self.program)
        except TypeError:
            pass

        self.fields['periodic_target'].queryset = PeriodicTarget.objects.filter(indicator=self.indicator).order_by('customsort','create_date', 'period')

        self.fields['program2'].initial = self.program
        self.fields['program2'].label = "Program"

        try:
            int(self.indicator)
            self.indicator = Indicator.objects.get(id=self.indicator)
        except TypeError as e:
            pass

        self.fields['indicator2'].initial = self.indicator.name
        self.fields['indicator2'].label = "Indicator"
        self.fields['program'].widget = forms.HiddenInput()
        self.fields['indicator'].widget = forms.HiddenInput()
        self.fields['target_frequency'].initial = self.indicator.target_frequency
        self.fields['target_frequency'].widget = forms.HiddenInput()
        #override the program queryset to use request.user for country
        self.fields['site'].queryset = SiteProfile.objects.filter(country__in=countries)

        #self.fields['indicator'].queryset = Indicator.objects.filter(name__isnull=False, program__country__in=countries)
        self.fields['tola_table'].queryset = TolaTable.objects.filter(Q(owner=self.request.user) | Q(id=self.tola_table))
        self.fields['periodic_target'].label = 'Measure against target*'
        self.fields['achieved'].label = 'Actual value'
        self.fields['date_collected'].help_text = ' '
