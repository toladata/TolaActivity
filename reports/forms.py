from django.core.urlresolvers import reverse_lazy

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *

from .models import *
from activitydb.models import Country, Program, Sector


class FilterForm(forms.Form):

    country = forms.ModelChoiceField(
        queryset = Country.objects.all(),
        required = False,
        empty_label = None,
        widget = forms.SelectMultiple(),
    )
    program = forms.ModelChoiceField(
        queryset = Program.objects.all(),
        required = False,
        empty_label = None,
        widget = forms.SelectMultiple(),
    )
    sector = forms.ModelChoiceField(
        queryset = Sector.objects.all(),
        empty_label = '',
        required = False,
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.html5_required = True
        self.helper.form_id = "filter_form"
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('region', css_class="input-sm"),
            Field('country', css_class="input-sm"),
            Field('program', css_class="input-sm"),
            Field('sector', css_class='input-sm'),
        )
        self.helper.form_method = 'get'
        self.helper.form_action = '/reports/filter/'
        self.helper.add_input(Submit('submit', 'Submit', css_class='btn-sm'))
        self.helper.add_input(Reset('reset', 'Reset', css_id='id_search_form_reset_btn', css_class='btn-warning btn-sm'))
        super(FilterForm, self).__init__(*args, **kwargs)
