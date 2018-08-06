from factory import DjangoModelFactory, post_generation, SubFactory

from formlibrary.models import (
    Beneficiary as BeneficiaryM,
    CustomForm as CustomFormM
)
from .workflow_models import (Organization,)


class Beneficiary(DjangoModelFactory):
    class Meta:
        model = BeneficiaryM

    beneficiary_name = 'Julian Lennon'
    father_name = 'John Lennon'

    @post_generation
    def workflowlevel1(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of workflowlevel1 were passed in, use them
            for workflowlevel1 in extracted:
                self.workflowlevel1.add(workflowlevel1)


class CustomForm(DjangoModelFactory):
    class Meta:
        model = CustomFormM

    name = 'Custom Form A'
    organization = SubFactory(Organization)
    public = {'org': False, 'url': False}
