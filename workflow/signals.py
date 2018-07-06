import logging
import os

try:
    from chargebee import APIError
    from chargebee.models import Subscription
except ImportError:
    pass
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User, Group
from django.db.models import signals
from django.dispatch import receiver
from django.template import loader

from tola import DEMO_BRANCH, utils, track_sync as tsync
from tola.management.commands.loadinitialdata import DEFAULT_WORKFLOW_LEVEL_1S
from workflow.models import (Dashboard, Organization, TolaUser,
                             WorkflowLevel1, WorkflowTeam, WorkflowLevel2,
                             ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_ADMIN,
                             ROLE_PROGRAM_TEAM, ROLE_VIEW_ONLY,
                             DEFAULT_PROGRAM_NAME)

logger = logging.getLogger(__name__)


@receiver(signals.pre_save, sender=WorkflowLevel2)
def pre_save_handler(sender, instance, *args, **kwargs):
    instance.full_clean()


def notify_excess_org_admin(organization, extra_context):
    org_admins = User.objects.values_list(
        'first_name', 'last_name', 'email').filter(
        tola_user__organization=organization,
        groups__name=ROLE_ORGANIZATION_ADMIN
    )

    for org_admin in org_admins:
        # create the used context for the E-mail templates
        context = {
            'org_admin_name': '{} {}'.format(org_admin[0], org_admin[1]),
        }
        context.update(extra_context)
        text_content = loader.render_to_string(
            'email/organization/exceed_seats.txt', context, using=None)
        html_content = loader.render_to_string(
            'email/organization/exceed_seats.html', context, using=None)

        # send the invitation email
        msg = EmailMultiAlternatives(
            subject='Edit user exceeding notification',
            body=text_content,
            to=[org_admin[2]],
            bcc=[settings.SALES_TEAM_EMAIL],
            reply_to=[settings.DEFAULT_REPLY_TO]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


def generate_public_url_token(instance):
    token_generator = utils.TokenGenerator()
    token = token_generator.make_token(
        instance, Dashboard.PUBLIC_URL)
    return token


# DASHBOARD SIGNALS
@receiver(signals.pre_save, sender=Dashboard)
def add_public_url_token(sender, instance, **kwargs):
    """
    Create a new public URL token when the dashboard is set to PUBLIC_URL
    or remove the token if it's not public via URL anymore
    """
    if (not instance.public_url_token and
            instance.public == Dashboard.PUBLIC_URL):
        public_url_token = generate_public_url_token(instance)
        instance.public_url_token = public_url_token
    elif (instance.public_url_token and
          instance.public != Dashboard.PUBLIC_URL):
        instance.public_url_token = None


# TOLA USER SIGNALS
@receiver(signals.post_save, sender=TolaUser)
def add_users_to_demo_default_wflvl1(sender, instance, **kwargs):
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


@receiver(signals.post_save, sender=TolaUser)
def add_users_to_default_wflvl1(sender, instance, **kwargs):
    if not settings.SET_PROGRAM_ADMIN_DEFAULT:
        return

    if (settings.SET_PROGRAM_ADMIN_DEFAULT and
            not settings.CREATE_DEFAULT_PROGRAM):
        logger.warning('SET_PROGRAM_ADMIN_DEFAULT is set to "True" but'
                       'CREATE_DEFAULT_PROGRAM is set to "False"')
        return

    workflowlevel1 = WorkflowLevel1.objects.get(
        organization=instance.organization,
        name__icontains=DEFAULT_PROGRAM_NAME)
    role = Group.objects.get(name=ROLE_PROGRAM_ADMIN)
    WorkflowTeam.objects.get_or_create(workflow_user=instance, role=role,
                                       workflowlevel1=workflowlevel1)


# ORGANIZATION SIGNALS
@receiver(signals.post_save, sender=Organization)
def create_default_program(sender, instance, **kwargs):
    if not settings.CREATE_DEFAULT_PROGRAM:
        return

    if kwargs.get('created') is False:
        return

    WorkflowLevel1.objects.create(
        name=DEFAULT_PROGRAM_NAME, organization=instance)


# WORKFLOWTEAM SIGNALS
@receiver(signals.pre_save, sender=WorkflowTeam)
def check_seats_save_team(sender, instance, **kwargs):
    """
    Validate, increase or decrease the amount of used seats
    based on the roles
    """
    instance.full_clean()
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
    sub_id = org.chargebee_subscription_id
    if not sub_id:
        logger.info('The organization {} does not have a '
                    'subscription'.format(org.name))
        return

    user_gained_seat = False

    # If the user is a Program Admin or Member
    # They should have a seat in the subscription
    if count == 0 and instance.role.name in [ROLE_PROGRAM_ADMIN,
                                             ROLE_PROGRAM_TEAM]:
        user_gained_seat = True
        used_seats += 1
    elif count == 1 and instance.role.name == ROLE_VIEW_ONLY:
        used_seats -= 1

    org.chargebee_used_seats = used_seats
    org.save()
    # Load subscription data from ChargeBee
    try:
        result = Subscription.retrieve(sub_id)
        subscription = result.subscription
    except APIError as e:
        logger.warn(e)
    else:
        # Validate the amount of available seats based on the subscription
        available_seats = subscription.plan_quantity
        if org.chargebee_used_seats > available_seats and user_gained_seat:
            extra_context = {
                'used_seats': used_seats,
                'available_seats': available_seats,
                'payment_portal_url': settings.PAYMENT_PORTAL_URL
            }
            notify_excess_org_admin(org, extra_context)


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
    if (os.getenv('APP_BRANCH') == DEMO_BRANCH or
            kwargs['action'] not in ['post_add', 'post_remove'] or
            kwargs['model'] != Group):
        return

    try:
        tola_user = TolaUser.objects.get(user=instance)
    except TolaUser.DoesNotExist as e:
        logger.info(e)
    else:
        changed_groups = Group.objects.values_list('name', flat=True).filter(
            id__in=kwargs['pk_set'])
        count = WorkflowTeam.objects.filter(
            workflow_user=tola_user,
            role__name__in=[ROLE_PROGRAM_ADMIN, ROLE_PROGRAM_TEAM]
        ).count()

        # Update the amount of used seats
        org = tola_user.organization
        used_seats = org.chargebee_used_seats
        user_gained_seats = False

        # If the user is an Org Admin, he's able to edit the program.
        # Therefore, he should have a seat in the subscription
        if count == 0 and ROLE_ORGANIZATION_ADMIN in changed_groups:
            if kwargs['action'] == 'post_add':
                user_gained_seats = True
                used_seats += 1
            elif kwargs['action'] == 'post_remove':
                used_seats -= 1

        org.chargebee_used_seats = used_seats
        org.save()

        # Load subscription data from ChargeBee
        sub_id = org.chargebee_subscription_id
        if not sub_id:
            logger.info('The organization {} does not have a '
                        'subscription'.format(tola_user.organization.name))
            return

        try:
            result = Subscription.retrieve(sub_id)
            subscription = result.subscription
        except APIError as e:
            logger.warn(e)
        else:
            # Validate the amount of available seats based on the subscription
            available_seats = subscription.plan_quantity
            if org.chargebee_used_seats > available_seats \
                    and user_gained_seats:
                extra_context = {
                    'used_seats': used_seats,
                    'available_seats': available_seats,
                    'payment_portal_url': settings.PAYMENT_PORTAL_URL
                }
                notify_excess_org_admin(org, extra_context)


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
