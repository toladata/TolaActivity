from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *
from crispy_forms.layout import Layout, Submit, Reset
from django import forms
from .models import CustomDashboard, DashboardTheme, DashboardComponent, ComponentDataSource


class CustomDashboardCreateForm(forms.ModelForm):

    class Meta:
        model = CustomDashboard
        exclude = ['create_date', 'edit_date', 'component_map', 'components']

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
        self.helper.add_input(Submit('submit', 'Save'))
        super(CustomDashboardCreateForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Commit is already set to false
        obj = super(CustomDashboardCreateForm, self).save(*args, **kwargs)
        return obj
        
class CustomDashboardModalForm(forms.ModelForm):
    
    class Meta:
        model = CustomDashboard
        exclude = ['create_date', 'edit_date', 'component_map', 'components']

    def __init__(self, *args, **kwargs):

        #get the user object from request to check permissions
        self.request = kwargs.pop("request")
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
        self.helper.add_input(Submit('submit', 'Save'))
        
        super(CustomDashboardModalForm, self).__init__(*args, **kwargs)
   
class CustomDashboardMapForm(forms.ModelForm):
    
    class Meta:
        model = CustomDashboard
        exclude = ['create_date', 'edit_date']

    def __init__(self, *args, **kwargs):

        #get the user object from request to check permissions
        self.request = kwargs.pop("request")
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
        
        super(CustomDashboardMapForm, self).__init__(*args, **kwargs)
   
class CustomDashboardForm(forms.ModelForm):

    class Meta:
        model = CustomDashboard
        exclude = ['create_date', 'edit_date']

    # components_offered = forms.ModelChoiceField(queryset=getDashboardComponents.filter(component_type=value)) 

    def __init__(self, *args, **kwargs):

        #get the user object from request to check permissions
        self.request = kwargs.pop("request")
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
        self.helper.form_id = "dashboard"
        self.helper.layout = Layout(
            HTML("""<br/>"""),
            TabHolder(
                Tab('Build Your View',
                    Fieldset("Step 1: View Properties",
                        HTML("""
                            <div class='panel panel-default'>
                              <!-- Default panel contents -->
                              {% if getCustomDashboard %}
                                  <!-- Table -->
                                  <table class="table">
                                    <tr >
                                    <th>Name</th>
                                    <th>Description</th>
                                    <th>Public?</th>
                                    <th>Theme</th>
                                    <th>Program</th>
                                    <th></th>
                                    </tr>
                                    <tr>
                                        <td>{{ getCustomDashboard.dashboard_name }}</td>
                                        <td>{{ getCustomDashboard.dashboard_description }}</td>
                                        <td> {% if getCustomDashboard.is_public == 1 %} Yes {% else %} No {% endif %}</td>
                                        <td>{{ getCustomDashboard.theme }}</td>
                                        <td>{{ getCustomDashboard.program }}</td>
                                        <td> <a class="dashboards" data-toggle="modal" data-target="#myModal" href='/configurabledashboard/edit/{{pk}}'>Edit</a> </td>
                                    </tr>
                                  </table>
                                  <a class="dashboard_components btn btn-primary" data-target="#add-components" data-toggle="tab">Next Step: Add Components</a>      
                                  <a class="dashboards btn btn-link" style='float: right;' href='/configurabledashboard/delete/{{pk}}' data-toggle="modal" data-target="#myModal">Cancel / Return to Menu</a>
                              {% endif %}
                            </div>
                            """),
                        ),
                    ),
                Tab('Add Components',
                    Fieldset("Step 2: Place Components on Your Page",
                        HTML("""
                            <div class='panel panel-default'>
                                <div class='panel panel-heading'>Layout For Your Page:</div>
                                <div class='panel panel-body'>
                                    {% if getCustomDashboard.theme == 'test_theme' %}
                                        Layout Image for Test Theme Goes Here<br><br>
                                    {% elif getCustomDashboard.theme %}
                                        Layout Image for your Theme Goes Here: {{getCustomDashboard.theme}}<br><br>
                                    {% endif %}
                                <div class='panel panel-default'>
                                    <div class='panel panel-body'>
                                        <table class="table">
                                            <tr>
                                                <th>Layout Position</th>
                                                <th>Component Type</th>
                                                <th>Select Existing Component</th>
                                                <th></th>
                                                <th>Add New Component</th>
                                            </tr>
                                            {% for key, value in getDashboardLayoutList.items %}
                                                <tr>
                                                    <td> {{key}} </td>
                                                    <td> {{value}} </td>
                                                    <td> {{getCustomDashboard.componentset}} 
                                                        <div class="form-group"> 
                                                            <select class="form-control" id="component_selector">
                                                            {% for component in getDashboardComponents %}
                                                                {% if component.component_type == value %}
                                                                    <option value={{component.id}}> {{component.component_name}} </option>
                                                                {% endif %}
                                                            {% empty %}
                                                                <option value=0> None </option>
                                                            {% endfor %}
                                                            </select>
                                                        </div>
                                                    </td>
                                                    <td></td>
                                                    <td><a class="dashboards" data-toggle="modal" data-target="#myModal" href='/configurabledashboard/component_add/{{getCustomDashboard.id}}/'>New</a></td>
                                                </tr>
                                            {% endfor %}
                                        </table>
                                    <div>
                                    <div class="panel panel-footer">Don't see a component or need to edit an existing component?<br>
                                        <a class="dashboards" data-toggle="modal" data-target="#myModal" href='/configurabledashboard/component/{{pk}}'> View Component Inventory </a></td>
                                    </div>
                                </div>
                            </div>
                            </div>
                                <div>
                                    <a class="btn btn-primary" data-target="#add-dashboard-data-sources" data-toggle="tab">Next Step: Add Data Sources</a>
                                </div>
                            </div>
                            """),
                        ),
                        PrependedAppendedText('forms.ModelChoiceField(queryset=getDashboardComponents.filter(component_type=value)'),
                    ),
                Tab('Add Data Sources',
                    Fieldset("Step 3: Add Data Sources for Components",
                        HTML("""
                            <div class='panel panel-default'>
                                <div class='panel panel-heading'>Assigned Data Sources</div>
                                <div class='panel panel-body'>Layout Image for your Theme Goes Here<br><br>
                                <div class='panel panel-default'>
                                    <div class='panel panel-body'>
                                        <table class="table">
                                            <tr> 
                                                <th>Position</th>
                                                <th>Component Type</th>
                                                <th>Component Name</th>
                                                <th>Data Type</th>
                                                <th>Data Source Type</th>
                                                <th>Select Data Source(s)</th>
                                                <th></th>
                                                <th>Add New Data Source</th>
                                            </tr>
                                            {% if getComponentOrder.items %}
                                                {% for key, component in getComponentOrder.items %}
                                                    <tr>
                                                        <td>{{key}}</td>
                                                        <td>{% if component.component_type %}
                                                                {{component.component_type}}
                                                            {% else %} Not Mapped {% endif %} </td>
                                                        <td>{% if component.component_name %}
                                                                {{component.component_name}}
                                                            {% else %} N/A {% endif %} </td>
                                                        <td>{% if component.data_reqiored %}
                                                                {{component.data_required}}
                                                            {% else %} N/A {% endif %} </td>
                                                        <td><div class="form-group" style="width: 75%;"> 
                                                                <select class="form-control" id="sel2">
                                                                    <option value="external"> External </option>
                                                                    <option value="internal"> Internal </option>
                                                                </select>
                                                            </div></td>
                                                        <td> <div class="form-group"> 
                                                                <select class="form-control" id="sel3">
                                                                        <option value=0> None </option>
                                                                        {% for data in getDataSources %}
                                                                            {% if data.data_type == component.data_required %}
                                                                                <option value=data.id> {{data.data_name}} </option>
                                                                            {% endif %}
                                                                        {% endfor %}
                                                                </select>
                                                            </div>
                                                        </td>
                                                        <td></td>
                                                            <td> <a class="dashboards" data-toggle="modal" data-target="#myModal" href='configurabledashboard/data_add/'> New </a></td>                     
                                                    </tr>
                                                {% endfor %}
                                            {% else %}
                                                <tr>
                                                    <td>*Missing Map*</td>
                                                    <td>*Missing Map*</td>
                                                    <td>*Missing Map*</td>
                                                    <td>*Missing Map*</td>
                                                    <td>*Missing Map*</td>
                                                    <td>*Missing Map*</td>
                                                    <td>*Missing Map*</td>
                                                    <td>*Missing Map*</td>
                                                </tr>
                                            {% endif %}
                                        </table>
                                    <div>
                                    <div class="panel panel-footer">Don't see your data source or need to edit an existing data source?<br>
                                        <a class="dashboards" data-toggle="modal" data-target="#myModal" href='configurabledashboard/data/{{pk}}/'> View All Data Sources</a></td>
                                    </div>
                                </div>
                            </div>
                            </div>
                                <div>
                                    <a class="btn btn-primary" data-target="#assign-data" data-toggle="tab">Next Step: Assign Data Values</a>
                                </div>
                            </div>
                            """),
                        ),
                    ),
                Tab('Assign Data',
                    Fieldset("Step 4: Assign Data Values",
                        HTML("""
                            <div class='panel panel-default'>
                                <table class="table">
                                    <tr>
                                        <th>Component</th>
                                        <th>Data Type</th>
                                        <th>Data Source</th>
                                        <th>Data Set</th>
                                    </tr>
                                    {% for component in getDashboardComponents %}
                                    <tr>
                                        <td>{{component.component_name}}</td>
                                        <td> {% if component.data_map %}
                                            Insert rows for each data map position
                                            {% else %}
                                            No Component Map
                                            {% endif %}    
                                        </td>
                                        <td> Either (1) data source listed in the data_map or a list of {{component.data_sources}}  </td>
                                        <td>  Either (1) data filter listed in the data_map or a list of data filteres </td>   
                                    </tr>
                                    {% endfor %}
                                </table>
                                <div class="panel-footer">
                                <a class="btn btn-primary" data-target="#preview-submit" data-toggle="tab">Next Step: Preview & Submit</a>
                                </div>
                            </div>
                            """),
                        ),
                    ),
                Tab('Preview & Submit',
                    Fieldset("Step 5: Preview & Finalize ",
                        HTML("""
                            <div class='panel panel-body'>
                                {% if getCustomDashboard %}
                                    <a class="btn btn-info" data-toggle="modal" data-target="#myPreviewModal" aria-hidden="true" href="/workflow/custom_dashboard_preview/{{ pk }}">Preview Dashboard</a>
                                {% else %}
                                    No dashboard to display.
                                {% endif %}
                                <p></p><p>To keep this dashboard, select "Save" below.  </p>
                            </div>
                            <div id="myPreviewModal" class="modal fade" role="dialog">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header"></div>
                                        <div class="modal-body"></div>
                                        <div class="modal-footer">
                                            <button type="button" class="btn btn-primary" data-dismiss="modal">Close</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """),
                        ),
                        FormActions(
                            Submit('submit', 'Save', css_class='btn-default'),
                            Reset('reset', 'Reset', css_class='btn-warning'),
                        ),
                    ),
                ),
                HTML("""<br/>"""),

        )

    # component_selection = forms.ChoiceField(
    #     choices=[],
    #     initial='None',
    #     required=True,
    # )
        super(CustomDashboardForm, self).__init__(*args, **kwargs)

        #here go the filters and overrides

class CustomDashboardDetailForm(forms.ModelForm):
    class Meta:
        model = CustomDashboard
        exclude = ['create_date', 'edit_date','global_item']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        # self.helper = FormHelper()
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-sm-2'
        # self.helper.field_class = 'col-sm-6'
        # self.helper.form_error_title = 'Form Errors'
        # self.helper.error_text_inline = True
        # self.helper.help_text_inline = True
        # self.helper.html5_required = True

        super(CustomDashbaordDetailForm, self).__init__(*args, **kwargs)

## Dashboard Theme Form Classes
class DashboardThemeCreateForm(forms.ModelForm):

    class Meta:
        model = DashboardTheme
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
        super(DashboardThemeCreateForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Commit is already set to false
        obj = super(DashboardThemeCreateForm, self).save(*args, **kwargs)
        return obj

class DashboardThemeForm(forms.ModelForm):

    class Meta:
        model = DashboardTheme
        exclude = ['create_date', 'edit_date']

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
        self.helper.form_tag = False
        self.helper.form_id = "dashboard_theme"
        # self.helper.add_input(Submit('submit', 'Save'))

        super(DashboardThemeForm, self).__init__(*args, **kwargs)

## --------Dashboard Component Form Classes-------------
class DashboardComponentCreateForm(forms.ModelForm):

    class Meta:
        model = DashboardComponent
        exclude = ['create_date', 'edit_date','data_sources']

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
        self.helper.form_tag = False
        self.helper.form_id = "new-component"         
        self.helper.layout = Layout(

            HTML("""<br/>"""),

                'component_name' ,'component_description','is_public','component_type','data_required','data_sources',

        )

        super(DashboardComponentCreateForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Commit is already set to false
        obj = super(DashboardComponentCreateForm, self).save(*args, **kwargs)
        return obj

class DashboardComponentForm(forms.ModelForm):

    class Meta:
        model = DashboardComponent
        exclude = ['create_date', 'edit_date']

    def __init__(self, *args, **kwargs):

        #get the user object from request to check permissions
        self.request = kwargs.pop("request")
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
        self.helper.add_input(Submit('submit', 'Save'))

        super(DashboardComponentForm, self).__init__(*args, **kwargs)

class DashboardComponentUpdateForm(forms.ModelForm):
    
    class Meta:
        model = DashboardComponent
        exclude = ['create_date', 'edit_date']

    def __init__(self, *args, **kwargs):

        # get the user object from request to check permissions
        self.request = kwargs.pop("request")
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
        
        super(DashboardComponentUpdateForm, self).__init__(*args, **kwargs)

## --------Data Source Form Classes-------------
class ComponentDataSourceCreateForm(forms.ModelForm):

    class Meta:
        model = ComponentDataSource
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
        self.helper.form_tag = False   
        self.helper.form_id = "data-source" 
        super(ComponentDataSourceCreateForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        obj = super(ComponentDataSourceCreateForm, self).save(*args, **kwargs)
        return obj

class ComponentDataSourceForm(forms.ModelForm):

    class Meta:
        model = ComponentDataSource
        exclude = ['create_date', 'edit_date', 'data_filter_key']

    def __init__(self, *args, **kwargs):

        #get the user object from request to check permissions
        self.request = kwargs.pop('request')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2 col-sm-2'
        self.helper.field_class = 'col-md-6 col-sm-6'
        self.helper.form_error_title = 'Form Errors'
        self.helper.error_text_inline = True
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.form_tag = True
        self.helper.form_id = "component_data_source"
        self.helper.add_input(Submit('submit', 'Save'))

        super(ComponentDataSourceForm, self).__init__(*args, **kwargs)

class ComponentDataSourceUpdateForm(forms.ModelForm):
    
    class Meta:
        model = ComponentDataSource
        exclude = ['create_date', 'edit_date']

    def __init__(self, *args, **kwargs):

        #get the user object from request to check permissions
        self.request = kwargs.pop("request")
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
        self.helper.add_input(Submit('submit', 'Save'))
        
        super(ComponentDataSourceUpdateForm, self).__init__(*args, **kwargs)
   