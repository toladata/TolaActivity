import logging
import os

from django.contrib.auth.models import Group
from django.db.models import signals
from django.dispatch import receiver

from tola import DEMO_BRANCH
from tola.management.commands.loadinitialdata import (
    DEFAULT_WORKFLOWLEVEL1_ID, DEFAULT_WORKFLOWLEVEL1_NAME)
from workflow.models import (TolaUser, WorkflowLevel1, WorkflowTeam,
                             ROLE_VIEW_ONLY)

logger = logging.getLogger(__name__)


@receiver(signals.post_save, sender=TolaUser)
def add_users_to_default_wflvl1(sender, instance, **kwargs):
    """
    Demo-only feature: add new users to certain program as ViewOnly.
    """
    if os.getenv('APP_BRANCH') != DEMO_BRANCH:
        return

    if kwargs.get('created') is False:
        return

    try:
        wflvl1 = WorkflowLevel1.objects.get(id=DEFAULT_WORKFLOWLEVEL1_ID,
                                            name=DEFAULT_WORKFLOWLEVEL1_NAME)
    except WorkflowLevel1.DoesNotExist:
        logger.warning(
            'Working on branch %s but the default program "#%d: %s" does not '
            'exist. Maybe initial data was not loaded with loadinitialdata?',
        )
    else:
        role = Group.objects.get(name=ROLE_VIEW_ONLY)
        WorkflowTeam.objects.create(workflow_user=instance, role=role,
                                    workflowlevel1=wflvl1)
