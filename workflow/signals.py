import logging
import os

try:
    from chargebee import Subscription
except ImportError:
    pass
from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models import signals
from django.dispatch import receiver

from tola import DEMO_BRANCH, track_sync as tsync
from tola.management.commands.loadinitialdata import DEFAULT_WORKFLOW_LEVEL_1S
from workflow.models import (Organization, TolaUser, WorkflowLevel1,
                             WorkflowTeam, ROLE_ORGANIZATION_ADMIN,
                             ROLE_PROGRAM_ADMIN, ROLE_PROGRAM_TEAM,
                             ROLE_VIEW_ONLY)

logger = logging.getLogger(__name__)


def get_addon_by_id(addon_id, addons):
    for addon in addons:
        if addon.id == addon_id:
            return addon

    return None


# TOLA USER SIGNALS
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
        wflvl1_0 = WorkflowLevel1.objects.get(
            id=DEFAULT_WORKFLOW_LEVEL_1S[0][0],
            name=DEFAULT_WORKFLOW_LEVEL_1S[0][1])
        wflvl1_1 = WorkflowLevel1.objects.get(
            id=DEFAULT_WORKFLOW_LEVEL_1S[1][0],
            name=DEFAULT_WORKFLOW_LEVEL_1S[1][1])
    except WorkflowLevel1.DoesNotExist:
        logger.warning(
            'Working on branch "%s" but any of the default programs does not '
            'exist. Maybe initial data was not loaded with loadinitialdata?',
            os.environ['APP_BRANCH']
        )
    else:
        role = Group.objects.get(name=ROLE_VIEW_ONLY)
        WorkflowTeam.objects.create(workflow_user=instance, role=role,
                                    workflowlevel1=wflvl1_0)
        WorkflowTeam.objects.create(workflow_user=instance, role=role,
                                    workflowlevel1=wflvl1_1)


# WORKFLOWTEAM SIGNALS
@receiver(signals.pre_save, sender=WorkflowTeam)
def check_seats_save_team(sender, instance, **kwargs):
    """
    Validate, increase or decrease the amount of used seats
    based on the roles
    """
    if os.getenv('APP_BRANCH') == DEMO_BRANCH:
        return

    user = instance.workflow_user.user
    org = instance.workflow_user.organization
    if ROLE_ORGANIZATION_ADMIN in user.groups.values_list('name', flat=True):
        return

    used_seats = org.chargebee_used_seats
    count = WorkflowTeam.objects.filter(
        workflow_user=instance.workflow_user,
        role__name__in=[ROLE_PROGRAM_ADMIN, ROLE_PROGRAM_TEAM]
    ).count()
    # Load subscription data from ChargeBee

    sub_id = org.chargebee_subscription_id
    if not sub_id:
        logger.info('The organization {} does not have a '
                    'subscription'.format(org.name))
        return
    result = Subscription.retrieve(sub_id)
    sub_addons = result.subscription.addons

    # If the user is a Program Admin or Member
    # They should have a seat in the subscription
    if count == 0 and instance.role.name in [ROLE_PROGRAM_ADMIN,
                                             ROLE_PROGRAM_TEAM]:
        used_seats += 1
    elif count == 1 and instance.role.name == ROLE_VIEW_ONLY:
        used_seats -= 1

    org.chargebee_used_seats = used_seats
    org.save()

    # Validate the amount of available seats based on the subscription
    user_addon = get_addon_by_id('user', sub_addons)
    if user_addon:
        available_seats = user_addon.quantity
        if available_seats < org.chargebee_used_seats:
            # TODO: Notify the Org admin
            pass


@receiver(signals.pre_delete, sender=WorkflowTeam)
def check_seats_delete_team(sender, instance, **kwargs):
    """
    Validate, increase or decrease the amount of used seats
    based on the roles
    """
    if os.getenv('APP_BRANCH') == DEMO_BRANCH:
        return

    user = instance.workflow_user.user
    org = instance.workflow_user.organization
    if ROLE_ORGANIZATION_ADMIN in user.groups.values_list('name', flat=True):
        return

    count = WorkflowTeam.objects.filter(
        workflow_user=instance.workflow_user,
        role__name__in=[ROLE_PROGRAM_ADMIN, ROLE_PROGRAM_TEAM]
    ).count()

    # If the user is a Program Admin or Member
    # They should have a seat in the subscription
    if count == 1 and instance.role.name in [ROLE_PROGRAM_ADMIN,
                                             ROLE_PROGRAM_TEAM]:
        org.chargebee_used_seats -= 1
        org.save()


# M2M SIGNALS
@receiver(signals.m2m_changed)
def check_seats_save_user_groups(sender, instance, **kwargs):
    """
    Validate, increase or decrease the amount of used seats
    based on the roles
    """
    if kwargs['model'] != Group or kwargs['action'] != 'post_add':
        return
    if os.getenv('APP_BRANCH') == DEMO_BRANCH:
        return

    try:
        tola_user = TolaUser.objects.get(user=instance)
    except TolaUser.DoesNotExist as e:
        logger.info(e)
    else:
        added_groups = Group.objects.values_list('name', flat=True).filter(
            id__in=kwargs['pk_set'])
        count = WorkflowTeam.objects.filter(
            workflow_user=tola_user,
            role__name__in=[ROLE_PROGRAM_ADMIN, ROLE_PROGRAM_TEAM]
        ).count()

        # Load subscription data from ChargeBee
        org = tola_user.organization
        used_seats = org.chargebee_used_seats
        sub_id = org.chargebee_subscription_id
        if not sub_id:
            logger.info('The organization {} does not have a '
                        'subscription'.format(tola_user.organization.name))
            return
        result = Subscription.retrieve(sub_id)
        sub_addons = result.subscription.addons

        # If the user is a Org Admin, he's able to edit the program.
        # Therefore, he should have a seat in the subscription
        if count == 0 and ROLE_ORGANIZATION_ADMIN in added_groups:
            used_seats += 1
        elif count == 0 and ROLE_VIEW_ONLY in added_groups:
            used_seats -= 1

            # Update the amount of used seats
        org.chargebee_used_seats = used_seats
        org.save()

        # Validate the amount of available seats based on the subscription
        user_addon = get_addon_by_id('user', sub_addons)
        if user_addon:
            available_seats = user_addon.quantity
            if available_seats < org.chargebee_used_seats:
                # TODO: Notify the Org admin
                pass


# ORGANIZATION SIGNALS
@receiver(signals.post_save, sender=Organization)
def sync_save_track_organization(sender, instance, **kwargs):
    if settings.TOLA_TRACK_SYNC_ENABLED:
        if kwargs.get('created'):
            tsync.create_instance(instance)
        else:
            tsync.update_instance(instance)


@receiver(signals.post_delete, sender=Organization)
def sync_delete_track_organization(sender, instance, **kwargs):
    if settings.TOLA_TRACK_SYNC_ENABLED:
        tsync.delete_instance(instance)


# WORKFLOWLEVEL1 SIGNALS
@receiver(signals.post_save, sender=WorkflowLevel1)
def sync_save_track_workflowlevel1(sender, instance, **kwargs):
    if settings.TOLA_TRACK_SYNC_ENABLED:
        if kwargs.get('created'):
            tsync.create_instance(instance)
        else:
            tsync.update_instance(instance)


@receiver(signals.post_delete, sender=WorkflowLevel1)
def sync_delete_track_workflowlevel1(sender, instance, **kwargs):
    if settings.TOLA_TRACK_SYNC_ENABLED:
        tsync.delete_instance(instance)
