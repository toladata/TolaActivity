from django.core.management.base import BaseCommand, CommandError
import factories


class Command(BaseCommand):

    def _create_workflow_data(self, wkflvl1_name, wkflvl2_names, indicator_name,
                              objective_names, sector_names, org):
        sectors = [factories.Sector(sector=name) for name in sector_names]
        wkflvl1 = factories.WorkflowLevel1(
            name=wkflvl1_name, cost_center=12345, sector=sectors,
            organization=org)
        for name in wkflvl2_names:
            wkflvl2 = factories.WorkflowLevel2(name=name,
                                               workflowlevel1=wkflvl1)
        for name in objective_names:
            factories.Objective(name=name, workflowlevel1=wkflvl1)

        indicator = factories.Indicator(name=indicator_name,
                                        workflowlevel1=[wkflvl1])
        factories.CollectedData(workflowlevel1=wkflvl1, workflowlevel2=wkflvl2,
                                indicator=indicator)

    def handle(self, *args, **options):
        org = factories.Organization(
            id=1,
            name='TolaData',
            level_1_label='Program',
            level_2_label='Project',
            level_3_label='Activity',
            level_4_label='Component'
        )

        self._generate_workflows(
            'Construction Project',
            ['1.1 Determine the real problem to solve',
             '1.2 Identify survey respondents and contact details'],
            '# of people receiving household water quality education',
            ['Promote sustainable development practices in communities'],
            [],
            org
        )

        self._generate_workflows(
            'Population Health Initiative',
            ['1.1 Develop brief survey',
             '1.2 Identify the stakeholders'],
            '# of medical kits provided to partner mobile medical units',
            ['Community members with improved knowledge of hygiene practices'],
            ['Basic Needs', 'Public Health', 'Information Dissemination'],
            org
        )

        self._generate_workflows(
            'SOS for Syria',
            ['1.1 Define project objectives',
             '1.2 Determine scope, resources and major tasks',
             '1.3 Research existing resources that can be adapted'],
            '% of injured community members who make full recovery',
            ['Improved recovery from injuries as a result of conflict',
             'Improved health of Syrian Communities Affected by Conflict'],
            ['Protection', 'Emergency'],
            org
        )

        self._generate_workflows(
            'Humanitarian Response to the Syrian Crisis',
            ['Send survey to respondents and allow completion',
             'Prepare for trade-offs'],
            '# of locations set up by mobile medical units',
            ['Improved recovery from injuries as a result of conflict'],
            ['Conflict Management'],
            org
        )

        self._generate_workflows(
            'Building Wells in South Sudan',
            ['1. Needs Assessment',
             '1.1 Identify education resource gaps from needs assessment',
             '2. Planning: How to map out a project',
             '2.1 Assemble your team'],
            'Number of beneficiaries registered',
            ['20% increase in incomes'],
            ['Resilience', 'Education Support'],
            org
        )
