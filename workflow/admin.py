from .models import *
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin, ExportMixin
from tola.util import getCountry
from admin_report.mixins import ChartReportAdmin
from simple_history.admin import SimpleHistoryAdmin


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
    list_display = ('workflowlevel1','workflowlevel2')
    list_filter = ('workflowlevel1__country',)
    pass


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


class WorkflowLevel2Admin(ImportExportModelAdmin):
    resource_class = WorkflowLevel2Resource
    list_display = ('workflowlevel1', 'name', 'short', 'create_date')
    list_filter = ('workflowlevel1__country', 'office', 'short')
    display = 'name'

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Filter by logged in users allowable countries
        user_countries = getCountry(request.user)
        #if not request.user.user.is_superuser:
        return queryset.filter(country__in=user_countries)

    pass


# Resource for CSV export
class CountryResource(resources.ModelResource):

    class Meta:
        model = Country


class CountryAdmin(ImportExportModelAdmin):
    resource_class = CountryResource
    list_display = ('country','code','organization','create_date', 'edit_date')
    list_filter = ('country','organization__name')


# Resource for CSV export
class SiteProfileResource(resources.ModelResource):
    country = fields.Field(column_name='country', attribute='country', widget=ForeignKeyWidget(Country, 'country'))
    type = fields.Field(column_name='type', attribute='type', widget=ForeignKeyWidget(ProfileType, 'profile'))
    office = fields.Field(column_name='office', attribute='office', widget=ForeignKeyWidget(Office, 'code'))
    district = fields.Field(column_name='admin level 2', attribute='district', widget=ForeignKeyWidget(District, 'name'))
    province = fields.Field(column_name='admin level 1', attribute='province', widget=ForeignKeyWidget(Province, 'name'))
    admin_level_three = fields.Field(column_name='admin level 3', attribute='admin_level_three', widget=ForeignKeyWidget(AdminLevelThree, 'name'))

    class Meta:
        model = SiteProfile
        skip_unchanged = True
        report_skipped = False
        #import_id_fields = ['id']


class SiteProfileAdmin(ImportExportModelAdmin):
    resource_class = SiteProfileResource
    list_display = ('name','office', 'country', 'province','district','admin_level_three','village')
    list_filter = ('country__country',)
    search_fields = ('office__code','country__country')
    pass


class WorkflowLevel1Admin(admin.ModelAdmin):
    list_display = ('countries','name','unique_id', 'description','funding_status')
    search_fields = ('name','unique_id')
    list_filter = ('funding_status','country','funding_status')
    display = 'Program'


class WorkflowTeamAdmin(admin.ModelAdmin):
    list_display = ('workflow_user','budget_limit','workflowlevel1s','country')
    display = 'Workflow Team'
    search_fields = ('workflow_user__user__username','workflowlevel1__name', 'workflow_user__user__last_name', 'country__country')
    list_filter = ('create_date','country')


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
            return '%s' % (user.user.email)

    class Meta:
        model = TolaUserProxy
        fields = ('title', 'name', 'user','country','create_date', 'email' )
        export_order = ('title', 'name', 'user','country','email','create_date')


class ReportTolaUserProxyAdmin(ChartReportAdmin, ExportMixin, admin.ModelAdmin ):

    resource_class = TolaUserProxyResource

    def get_queryset(self, request):

        qs = super(ReportTolaUserProxyAdmin, self).get_queryset(request)
        return qs.filter(user__is_active= True)

    list_display = ('title','name', 'user','email', 'country', 'create_date')
    list_filter = ('country', 'create_date', 'user__is_staff')

    def email(self, data):
        auth_users = User.objects.all()
        for a_user in auth_users:
            if data.user == a_user:
                email = a_user.email
        return email


class TolaSitesAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency_name')
    display = 'Tola Site'
    list_filter = ('name',)
    search_fields = ('name','agency_name')


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
    search_fields = ('name','user')


class TolaUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    display = 'Tola User'
    list_filter = ('country', 'user__is_staff',)
    search_fields = ('name','country__country','title')


class FormGuidanceAdmin(admin.ModelAdmin):
    list_display = ( 'form', 'guidance', 'guidance_link', 'create_date',)
    display = 'Form Guidance'


class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'create_date', 'edit_date')
    display = 'Project Type'


class SectorAdmin(admin.ModelAdmin):
    list_display = ('sector', 'create_date', 'edit_date')
    display = 'Sector'


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'create_date', 'edit_date')
    display = 'Contact'
    list_filter = ('create_date','country')
    search_fields = ('name','country','title','city')


class FundCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Fund Code'


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('source_currency','target_currency', 'current_rate', 'conversion_date')
    display = 'Currency Conversion'


class ApprovalTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    display = 'Approval Types'


class ApprovalWorkflowAdmin(admin.ModelAdmin):
    list_display = ('approval_type','section')
    display = 'Approval Workflow'


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'create_date')
    search_fields = ('name','country__country')
    list_filter = ('create_date','country')
    display = 'Admin Boundary 1'


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'create_date')
    search_fields = ('create_date','province')
    list_filter = ('province__country__country','province')
    display = 'Admin Boundary 2'


class AdminLevelThreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'create_date')
    search_fields = ('name','district__name')
    list_filter = ('district__province__country__country','district')
    display = 'Admin Boundary 3'


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country', 'create_date', 'edit_date')
    search_fields = ('name','country__country','code')
    list_filter = ('create_date','country__country')
    display = 'Office'


class ProfileTypeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'create_date', 'edit_date')
    display = 'ProfileType'


class LandTypeAdmin(admin.ModelAdmin):
    list_display = ('classify_land', 'create_date', 'edit_date')
    display = 'Land Type'


class WorkflowLevel3Admin(admin.ModelAdmin):
    list_display = ('description', 'create_date', 'edit_date')
    display = 'Workflow Level 3'


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('contributor', 'description_of_contribution', 'proposed_value', 'create_date', 'edit_date')
    display = 'Budget'


class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('name','country')
    list_filter = ('country','workflowlevel2')


class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('item','checklist','in_file')
    list_filter = ('checklist','global_item')


class WorkflowModulesAdmin(admin.ModelAdmin):
    list_display = ('workflowlevel2',)
    list_filter = ('workflowlevel2',)


class StakeholderTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Stakeholder Types'
    list_filter = ('create_date',)
    search_fields = ('name',)


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


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(AdminLevelThree, AdminLevelThreeAdmin)
admin.site.register(Village)
admin.site.register(WorkflowLevel1, SimpleHistoryAdmin)
admin.site.register(Sector)
admin.site.register(WorkflowLevel2, SimpleHistoryAdmin)
admin.site.register(Documentation,DocumentationAdmin)
admin.site.register(SiteProfile, SimpleHistoryAdmin)
admin.site.register(WorkflowLevel3, WorkflowLevel3Admin)
admin.site.register(ProjectType, ProjectTypeAdmin)
admin.site.register(Budget)
admin.site.register(ProfileType)
admin.site.register(WorkflowTeam, WorkflowTeamAdmin)
admin.site.register(ChecklistItem, ChecklistItemAdmin)
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(Stakeholder, StakeholderAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(StakeholderType)
admin.site.register(TolaUser,TolaUserAdmin)
admin.site.register(TolaSites,TolaSitesAdmin)
admin.site.register(FormGuidance,FormGuidanceAdmin)
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

