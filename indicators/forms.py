from datetime import datetime
from functools import partial
from django.db.models import Q
from django import forms

from indicators.models import (
    Indicator, PeriodicTarget, CollectedData, Objective, StrategicObjective,
    TolaTable, DisaggregationType
)
from workflow.models import (
    Program, SiteProfile, Documentation, ProjectComplete, TolaUser
)
from tola.util import getCountry


class DatePicker(forms.DateInput):
    """
    Use in form to create a Jquery datepicker element
    Usage:
        self.fields['some_date_field'].widget = DatePicker.DateInput()
    """
    template_name = 'datepicker.html'
    DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class IndicatorForm(forms.ModelForm):
    program2 = forms.CharField(
        widget=forms.TextInput(
            attrs={'readonly': 'readonly', 'label': 'Program'}
        )
    )
    unit_of_measure_type = forms.ChoiceField(
        choices=Indicator.UNIT_OF_MEASURE_TYPES,
        widget=forms.RadioSelect(),
    )
    cumulative_choices = (
        (1, None),
        (2, True),
        (3, False)
    )
    is_cumulative = forms.ChoiceField(
        choices=cumulative_choices,
        widget=forms.RadioSelect())

    program = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Indicator
        exclude = ['program', 'create_date', 'edit_date']
        widgets = {
            # {'program': forms.Select()}
            'definition': forms.Textarea(attrs={'rows': 4}),
            'justification': forms.Textarea(attrs={'rows': 4}),
            'quality_assurance': forms.Textarea(attrs={'rows': 4}),
            'data_issues': forms.Textarea(attrs={'rows': 4}),
            'indicator_changes': forms.Textarea(attrs={'rows': 4}),
            'comments': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'rationale_for_target': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        indicator = kwargs.get('instance', None)
        if not indicator.unit_of_measure_type:
            kwargs['initial']['unit_of_measure_type'] = \
                Indicator.UNIT_OF_MEASURE_TYPES[0][0]
        self.request = kwargs.pop('request')
        self.programval = kwargs.pop('program')

        super(IndicatorForm, self).__init__(*args, **kwargs)

        self.fields['program2'].initial = indicator.programs
        self.fields['program'].initial = self.programval.id

        countries = getCountry(self.request.user)
        self.fields['disaggregation'].queryset = DisaggregationType.objects\
            .filter(country__in=countries, standard=True)
        self.fields['objectives'].queryset = Objective.objects.filter(
            program__id__in=[self.programval.id])
        self.fields['strategic_objectives'].queryset = StrategicObjective\
            .objects.filter(country__in=countries)
        self.fields['approved_by'].queryset = TolaUser.objects.filter(
            country__in=countries).distinct()
        self.fields['approval_submitted_by'].queryset = TolaUser.objects\
            .filter(country__in=countries).distinct()
        self.fields['name'].required = True
        self.fields['unit_of_measure'].required = True
        self.fields['target_frequency'].required = True
        self.fields['target_frequency_start'].widget\
            .attrs['class'] = 'monthPicker'
        # self.fields['is_cumulative'].widget = forms.RadioSelect()
        if self.instance.target_frequency and \
                self.instance.target_frequency != Indicator.LOP:
            self.fields['target_frequency'].widget.attrs['readonly'] \
                    = "readonly"


class CollectedDataForm(forms.ModelForm):

    class Meta:
        model = CollectedData
        exclude = ['create_date', 'edit_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_date_collected(self):
        date_collected = self.cleaned_data['date_collected']
        date_collected = datetime.strftime(date_collected, '%Y-%m-%d')
        return date_collected

    program2 = forms.CharField(
        widget=forms.TextInput(
            attrs={'readonly': 'readonly', 'label': 'Program'}
        )
    )
    indicator2 = forms.CharField(
        widget=forms.TextInput(
            attrs={'readonly': 'readonly', 'label': 'Indicator'}
        )
    )
    target_frequency = forms.CharField()
    date_collected = forms.DateField(widget=DatePicker.DateInput(),
                                     required=True)

    def __init__(self, *args, **kwargs):
        # instance = kwargs.get('instance', None)
        self.request = kwargs.pop('request')
        self.program = kwargs.pop('program')
        self.indicator = kwargs.pop('indicator', None)
        self.tola_table = kwargs.pop('tola_table')
        super(CollectedDataForm, self).__init__(*args, **kwargs)

        # override the program queryset to use request.user for country
        self.fields['evidence'].queryset = Documentation.objects\
            .filter(program=self.program)

        # override the program queryset to use request.user for country
        self.fields['complete'].queryset = ProjectComplete.objects\
            .filter(program=self.program)
        self.fields['complete'].label = "Project"

        # override the program queryset to use request.user for country
        countries = getCountry(self.request.user)
        # self.fields['program'].queryset = Program.objects\
        #   .filter(funding_status="Funded", country__in=countries).distinct()
        try:
            int(self.program)
            self.program = Program.objects.get(id=self.program)
        except TypeError:
            pass

        self.fields['periodic_target'].queryset = PeriodicTarget.objects\
            .filter(indicator=self.indicator)\
            .order_by('customsort', 'create_date', 'period')

        self.fields['program2'].initial = self.program
        self.fields['program2'].label = "Program"

        try:
            int(self.indicator)
            self.indicator = Indicator.objects.get(id=self.indicator)
        except TypeError:
            pass

        self.fields['indicator2'].initial = self.indicator.name
        self.fields['indicator2'].label = "Indicator"
        self.fields['program'].widget = forms.HiddenInput()
        self.fields['indicator'].widget = forms.HiddenInput()
        self.fields['target_frequency'].initial = self.indicator\
            .target_frequency
        self.fields['target_frequency'].widget = forms.HiddenInput()
        self.fields['site'].queryset = SiteProfile.objects\
            .filter(country__in=countries)
        self.fields['tola_table'].queryset = TolaTable.objects\
            .filter(Q(owner=self.request.user) | Q(id=self.tola_table))
        self.fields['periodic_target'].label = 'Measure against target*'
        self.fields['achieved'].label = 'Actual value'
        self.fields['date_collected'].help_text = ' '
