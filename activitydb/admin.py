from django.contrib import admin
from .models import Country, Province, Office, Village, Program, ProgramAdmin, Documentation, Template,District, Sector, \
     ProgramDashboard, CustomDashboard, ProjectAgreement, ProjectAgreementAdmin,ProjectComplete, ProjectCompleteAdmin, SiteProfile, Capacity, Monitor, \
    Benchmarks, Evaluate, ProjectType, ProjectTypeOther, TrainingAttendance, Beneficiary, Budget, ProfileType, FAQ, ApprovalAuthority, \
    ApprovalAuthorityAdmin, ChecklistItem, ChecklistItemAdmin,Checklist, ChecklistAdmin, DocumentationApp, ProvinceAdmin, DistrictAdmin, AdminLevelThree, AdminLevelThreeAdmin, StakeholderType, Stakeholder, \
    Contact, StakeholderAdmin, ContactAdmin, FormLibrary, FormLibraryAdmin, FormEnabled, FormEnabledAdmin, Feedback, FeedbackAdmin
from import_export import resources, fields, widgets
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin


class ProjectAgreementResource(resources.ModelResource):

    class Meta:
        model = ProjectAgreement
        widgets = {
                'create_date': {'format': '%d/%m/%Y'},
                'edit_date': {'format': '%d/%m/%Y'},
                'expected_start_date': {'format': '%d/%m/%Y'},
                }


class ProjectAgreementAdmin(ImportExportModelAdmin):
    resource_class = ProjectAgreementResource
    list_display = ('program','project_name')
    list_filter = ('program__country','office')
    pass


class SiteProfileResource(resources.ModelResource):

    country = fields.Field(column_name='country', attribute='country', widget=ForeignKeyWidget(Country, 'country'))
    office = fields.Field(column_name='office', attribute='office', widget=ForeignKeyWidget(Office, 'code'))
    district = fields.Field(column_name='admin level 2', attribute='district', widget=ForeignKeyWidget(District, 'name'))
    province = fields.Field(column_name='admin level 1', attribute='province', widget=ForeignKeyWidget(Province, 'name'))
    admin_level_three = fields.Field(column_name='admin level 3', attribute='admin_level_three__name', widget=ForeignKeyWidget(AdminLevelThree, 'name'))

    class Meta:
        model = SiteProfile
        fields = ('id','country','name','office','district','province','admin_level_three','village',\
                 'longitude','latitude')
        skip_unchanged = True
        report_skipped = False
        #import_id_fields = ['id']


class SiteProfileAdmin(ImportExportModelAdmin):

    resource_class = SiteProfileResource
    list_display = ('name','office', 'country', 'province','district','admin_level_three','village')
    list_filter = ('country__country',)
    search_fields = ('office__code','country__country')
    pass


admin.site.register(Country)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Office)
admin.site.register(District, DistrictAdmin)
admin.site.register(AdminLevelThree, AdminLevelThreeAdmin)
admin.site.register(Village)
admin.site.register(Program, ProgramAdmin)
admin.site.register(CustomDashboard)
admin.site.register(Sector)
admin.site.register(ProjectAgreement, ProjectAgreementAdmin)
admin.site.register(ProjectComplete, ProjectCompleteAdmin)
admin.site.register(Documentation)
admin.site.register(Template)
admin.site.register(SiteProfile, SiteProfileAdmin)
admin.site.register(Capacity)
admin.site.register(Monitor)
admin.site.register(Benchmarks)
admin.site.register(Evaluate)
admin.site.register(ProjectType)
admin.site.register(ProjectTypeOther)
admin.site.register(TrainingAttendance)
admin.site.register(Beneficiary)
admin.site.register(Budget)
admin.site.register(ProfileType)
admin.site.register(FAQ)
admin.site.register(ApprovalAuthority, ApprovalAuthorityAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(DocumentationApp)
admin.site.register(Stakeholder, StakeholderAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(StakeholderType)
admin.site.register(FormLibrary,FormLibraryAdmin)
admin.site.register(FormEnabled,FormEnabledAdmin)
admin.site.register(Feedback,FeedbackAdmin)







