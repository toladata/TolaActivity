from factory import DjangoModelFactory, SubFactory, post_generation

from indicators.models import (
    Indicator as IndicatorM,
)
from workflow_models import WorkflowLevel1


class Indicator(DjangoModelFactory):
    class Meta:
        model = IndicatorM

    name = 'Building resilience in Mali'

    @post_generation
    def workflowlevel1(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of workflowlevel1 were passed in, use them
            for workflowlevel1 in extracted:
                self.workflowlevel1.add(workflowlevel1)
