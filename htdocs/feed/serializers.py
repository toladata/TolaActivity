from django.forms import widgets
from rest_framework import serializers
from activitydb.models import ProjectProposal, Program, Sector, ProjectType, Office, Community, Country, ProjectComplete, ProjectAgreement, ProjectTypeOther
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class ProposalSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProjectProposal

class ProgramSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Program


class SectorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sector


class ProjectTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProjectType


class OfficeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Office


class CommunitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Community


class CompleteSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProjectComplete


class AgreementSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProjectAgreement


class CountrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Country


class ProjectTypeOtherSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProjectTypeOther