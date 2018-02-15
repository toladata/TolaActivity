from admin_report.mixins import ChartReportAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export.widgets import ForeignKeyWidget
from simple_history.admin import SimpleHistoryAdmin

from .models import (Country, Documentation, WorkflowLevel2,
                     Organization, AdminLevelOne, Office, AdminLevelTwo,
                     AdminLevelThree, AdminLevelFour, WorkflowLevel1, Sector,
                     WorkflowLevel2, WorkflowLevel2Sort, Documentation,
                     SiteProfile, ProjectType,  Budget,
                     ProfileType, WorkflowTeam, ChecklistItem, Checklist,
                     Stakeholder, Contact, StakeholderType, TolaUser, TolaSites,
                     FormGuidance, TolaUserProxy, TolaBookmarks, Currency,
                     ApprovalWorkflow, ApprovalType, FundCode, RiskRegister,
                     IssueRegister, CodedField, WorkflowModules, Milestone,
                     Portfolio, SectorRelated, WorkflowLevel1Sector)


# Resource for CSV export
class DocumentationResource(resources.ModelResource):
    country = fields.Field(column_name='country', attribute='country', widget=ForeignKeyWidget(Country, 'country'))
    workflowlevel1 = fields.Field(column_name='workflowlevel1', attribute='workflowlevel1', widget=ForeignKeyWidget(WorkflowLevel1, 'name'))
    workflowlevel2 = fields.Field(column_name='workflowlevel2', attribute='workflowlevel2', widget=ForeignKeyWidget(WorkflowLevel2, 'name'))

    class Meta:
        model = Documentation
        widgets = {
                'create_date': {'format': '%d/%m/%Y'},
                'edit_date': {'format': '%d/%m/%Y'},
                'expected_start_date': {'format': '%d/%m/%Y'},
                }


class DocumentationAdmin(ImportExportModelAdmin):
    resource_class = DocumentationResource
    list_display = ('workflowlevel1', 'workflowlevel2')
    list_filter = ('workflowlevel1__country',)


# Resource for CSV export
class WorkflowLevel2Resource(resources.ModelResource):
    class Meta:
        model = WorkflowLevel2
        widgets = {
                'create_date': {'format': '%d/%m/%Y'},
                'edit_date': {'format': '%d/%m/%Y'},
                'expected_start_date': {'format': '%d/%m/%Y'},
                'expected_end_date': {'format': '%d/%m/%Y'},
                'actual_start_date': {'format': '%d/%m/%Y'},
                'actual_end_date': {'format': '%d/%m/%Y'},
                }


# Resource for CSV export
class CountryResource(resources.ModelResource):

    class Meta:
        model = Country


class CountryAdmin(ImportExportModelAdmin):
    resource_class = CountryResource
    list_display = ('country', 'code', 'create_date', 'edit_date')
    list_filter = ('country',)


# Resource for CSV export
class SiteProfileResource(resources.ModelResource):
    country = fields.Field(column_name='country', attribute='country', widget=ForeignKeyWidget(Country, 'country'))
    type = fields.Field(column_name='type', attribute='type', widget=ForeignKeyWidget(ProfileType, 'profile'))
    office = fields.Field(column_name='office', attribute='office', widget=ForeignKeyWidget(Office, 'code'))
    adminlevelone = fields.Field(column_name='admin level 1', attribute='adminlevelone', widget=ForeignKeyWidget(AdminLevelOne, 'name'))
    adminleveltwo = fields.Field(column_name='admin level 2', attribute='adminleveltwo', widget=ForeignKeyWidget(AdminLevelTwo, 'name'))
    admin_level_three = fields.Field(column_name='admin level 3', attribute='admin_level_three', widget=ForeignKeyWidget(AdminLevelThree, 'name'))

    class Meta:
        model = SiteProfile
        skip_unchanged = True
        report_skipped = False


class WorkflowTeamAdmin(admin.ModelAdmin):
    list_display = ('workflow_user', 'budget_limit', 'workflowlevel1',
                    'country')
    display = 'Workflow Team'
    search_fields = ('workflow_user__user__username', 'workflowlevel1__name',
                     'workflow_user__user__last_name', 'country__country')
    list_filter = ('create_date', 'country')


class StakeholderAdmin(ImportExportModelAdmin):
    list_display = ('name', 'type', 'country', 'create_date')
    display = 'Stakeholder List'
    list_filter = ('country', 'type')


class RiskRegisterAdmin(ImportExportModelAdmin):
    list_display = ('name', 'type', 'workflowlevel2')
    display = 'Risk Register'
    list_filter = ('workflowlevel2', 'type')


class IssueRegisterAdmin(ImportExportModelAdmin):
    list_display = ('name', 'type', 'workflowlevel2')
    display = 'Issue Register'
    list_filter = ('workflowlevel2', 'type')


class CodedFieldAdmin(ImportExportModelAdmin):
    list_display = ('name', 'type','is_universal')
    display = 'Coded Fields'
    list_filter = ('type', 'is_universal')


class TolaUserProxyResource(resources.ModelResource):
    country = fields.Field(column_name='country', attribute='country', widget=ForeignKeyWidget(Country, 'country'))
    user = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'username'))
    email = fields.Field()

    def dehydrate_email(self, user):
            return '%s' % user.user.email

    class Meta:
        model = TolaUserProxy
        fields = ('title', 'name', 'user', 'country', 'create_date', 'email')
        export_order = ('title', 'name', 'user', 'country', 'email',
                        'create_date')


class ReportTolaUserProxyAdmin(ChartReportAdmin, ExportMixin, admin.ModelAdmin):

    resource_class = TolaUserProxyResource

    def get_queryset(self, request):
        qs = super(ReportTolaUserProxyAdmin, self).get_queryset(request)
        return qs.filter(user__is_active=True)

    list_display = ('title', 'name', 'user', 'email', 'country', 'create_date')
    list_filter = ('country', 'create_date', 'user__is_staff')

    def email(self, data):
        return data.user.email


class TolaSitesAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency_name')
    display = 'Tola Site'
    list_filter = ('name',)
    search_fields = ('name', 'agency_name')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Organization'


class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Milestone'


class TolaBookmarksAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    display = 'Tola User Bookmarks'
    list_filter = ('user__name',)
    search_fields = ('name', 'user')


class TolaUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'organization')
    display = 'Tola User'
    list_filter = ('country', 'user__is_staff', 'organization')
    search_fields = ('name', 'country__country', 'title')


class FormGuidanceAdmin(admin.ModelAdmin):
    list_display = ('form', 'guidance', 'guidance_link', 'create_date')
    display = 'Form Guidance'


class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'create_date', 'edit_date')
    display = 'Project Type'


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'create_date', 'edit_date')
    display = 'Contact'
    list_filter = ('create_date','country')
    search_fields = ('name','country','title','city')


class FundCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Fund Code'


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('source_currency', 'target_currency', 'current_rate',
                    'conversion_date')
    display = 'Currency Conversion'


class ApprovalTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    display = 'Approval Types'


class ApprovalWorkflowAdmin(admin.ModelAdmin):
    list_display = ('approval_type','section')
    display = 'Approval Workflow'


class AdminLevelOneAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'create_date')
    search_fields = ('name', 'country__country')
    list_filter = ('create_date', 'country')
    display = 'Admin Boundary 1'


class AdminLevelTwoAdmin(admin.ModelAdmin):
    list_display = ('name', 'adminlevelone', 'create_date')
    search_fields = ('create_date', 'adminlevelone')
    list_filter = ('adminlevelone__country__country', 'adminlevelone')
    display = 'Admin Boundary 2'


class AdminLevelThreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'adminleveltwo', 'create_date')
    search_fields = ('name', 'adminleveltwo__name')
    list_filter = ('adminleveltwo__adminlevelone__country__country','name')
    display = 'Admin Boundary 3'


class AdminLevelFourAdmin(admin.ModelAdmin):
    list_display = ('name', 'adminlevelthree', 'create_date')
    search_fields = ('name', 'adminlevelthree__name')
    list_filter = ('adminlevelthree__adminleveltwo__adminlevelone__country__country','name')
    display = 'Admin Boundary 3'


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country', 'create_date', 'edit_date')
    search_fields = ('name', 'country__country', 'code')
    list_filter = ('create_date', 'country__country')
    display = 'Office'


class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country', 'workflowlevel2')


class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'checklist', 'in_file')
    list_filter = ('checklist', 'global_item')


class WorkflowModulesAdmin(admin.ModelAdmin):
    list_display = ('workflowlevel2',)
    list_filter = ('workflowlevel2',)


class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Portfolio'
    list_filter = ('create_date',)
    search_fields = ('name',)


class SectorRelatedAdmin(admin.ModelAdmin):
    list_display = ('sector', 'sector_related')
    display = 'Sector Related'
    list_filter = ('sector',)
    search_fields = ('sector',)


class WorkflowLevel1SectorAdmin(admin.ModelAdmin):
    list_display = ('sector', 'workflowlevel1')
    display = 'WorkflowLevel1 Sectors'
    list_filter = ('workflowlevel1',)
    search_fields = ('sector', 'workflowlevel1')


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(AdminLevelOne, AdminLevelOneAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(AdminLevelTwo, AdminLevelTwoAdmin)
admin.site.register(AdminLevelThree, AdminLevelThreeAdmin)
admin.site.register(AdminLevelFour, AdminLevelFourAdmin)
admin.site.register(WorkflowLevel1, SimpleHistoryAdmin)
admin.site.register(Sector)
admin.site.register(WorkflowLevel2, SimpleHistoryAdmin)
admin.site.register(WorkflowLevel2Sort)
admin.site.register(Documentation, DocumentationAdmin)
admin.site.register(SiteProfile, SimpleHistoryAdmin)
admin.site.register(ProjectType, ProjectTypeAdmin)
admin.site.register(Budget)
admin.site.register(ProfileType)
admin.site.register(WorkflowTeam, WorkflowTeamAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(Stakeholder, StakeholderAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(StakeholderType)
admin.site.register(TolaUser, TolaUserAdmin)
admin.site.register(TolaSites, TolaSitesAdmin)
admin.site.register(FormGuidance, FormGuidanceAdmin)
admin.site.register(TolaUserProxy, ReportTolaUserProxyAdmin)
admin.site.register(TolaBookmarks, TolaBookmarksAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ApprovalWorkflow, ApprovalWorkflowAdmin)
admin.site.register(ApprovalType, ApprovalTypeAdmin)
admin.site.register(FundCode, FundCodeAdmin)
admin.site.register(RiskRegister, RiskRegisterAdmin)
admin.site.register(IssueRegister, IssueRegisterAdmin)
admin.site.register(CodedField, CodedFieldAdmin)
admin.site.register(WorkflowModules, WorkflowModulesAdmin)
admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(SectorRelated, SectorRelatedAdmin)
admin.site.register(WorkflowLevel1Sector, WorkflowLevel1SectorAdmin)
