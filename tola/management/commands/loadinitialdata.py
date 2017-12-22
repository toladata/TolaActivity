# -*- coding: utf-8 -*-
from cStringIO import StringIO
import logging
import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, IntegrityError, connection

import factories
from indicators.models import (Level, Frequency, Indicator, PeriodicTarget,
                               CollectedData)
from workflow.models import (
    ROLE_VIEW_ONLY, ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_ADMIN,
    ROLE_PROGRAM_TEAM, Organization, Country, TolaUser, Group, Sector,
    Stakeholder, Milestone, WorkflowLevel1, WorkflowLevel2,
    WorkflowLevel1Sector, WorkflowTeam)

logger = logging.getLogger(__name__)
DEFAULT_WORKFLOW_LEVEL_1S = [  # tuple (id, name)
    (3, 'Humanitarian Response to the Syrian Crisis'),
    (6, u'Bildung für sozial benachteiligte Kinder in Deutschland'),
]
DEFAULT_ORG = {
    'id': 1,
    'name': settings.DEFAULT_ORG,
}
DEFAULT_COUNTRY_CODES = ('DE', 'SY')


class Command(BaseCommand):
    help="""
    Loads initial factories data.

    By default, a new default organization will be created, plus countries,
    groups, sectors and indicator types.

    Passing a --demo flag will populate the database with extra sample projects,
    activities, indicators, workflowteams etc. As a pre-condition for it to
    work, all affected tables except organization, countries, groups and sectors
    should be empty. Otherwise the command will exit with an error and no
    new data will be added to the database.
    """
    APPS = ('workflow', 'formlibrary', 'customdashboard', 'reports', 'gladmap',
            'search')

    def __init__(self):
        # Note: for the lists we fill the first element with an empty value for
        # development readability (id == position).
        self._organization = None
        self._groups = ['']
        self._country_germany = None
        self._country_syria = None
        self._sectors = ['']

        self._tolauser_andrew = None
        self._users = []
        self._tolauser_ninette = None
        self._site_profiles = ['']
        self._workflowlevel1s = ['']
        self._workflowlevel2s = ['']
        self._levels = ['']
        self._frequencies = ['']
        self._indicators = ['']

    def _clear_database(self):
        """
        Clears all old data except:
        - Default organization
        - Default countries
        - Current registered users

        Before everything happens, current registered users will be reassigned
        to the default organization and to have residency in Germany.
        """
        # Check integrity
        try:
            organization = Organization.objects.get(**DEFAULT_ORG)
        except Organization.DoesNotExist:
            msg = ("Error: the default organization could not be found in the "
                   "database. Maybe you are restoring without having run the "
                   "command a first time?")
            logger.error(msg)
            sys.stderr.write("{}\n".format(msg))
            raise IntegrityError(msg)

        try:
            country = Country.objects.get(code=DEFAULT_COUNTRY_CODES[0])
            Country.objects.get(code=DEFAULT_COUNTRY_CODES[1])
        except Country.DoesNotExist:
            msg = ("Error: one or both of the default countries %s could not "
                   "be found in the database. Maybe you are restoring without "
                   "having run the command a first time?".format(
                   DEFAULT_COUNTRY_CODES))
            logger.error(msg)
            sys.stderr.write("{}\n".format(msg))
            raise IntegrityError(msg)

        # Reassign organization and country for current registered users
        TolaUser.objects.all().update(organization=organization,
                                      country=country)

        # Delete data - Kill 'Em All!
        Organization.objects.exclude(id=DEFAULT_ORG['id']).delete()
        Group.objects.all().delete()
        Country.objects.exclude(code__in=DEFAULT_COUNTRY_CODES).delete()
        Sector.objects.all().delete()
        Stakeholder.objects.all().delete()
        Milestone.objects.all().delete()
        WorkflowLevel1.objects.all().delete()
        WorkflowLevel2.objects.all().delete()
        Level.objects.all().delete()
        Frequency.objects.all().delete()
        Indicator.objects.all().delete()
        PeriodicTarget.objects.all().delete()
        CollectedData.objects.all().delete()
        WorkflowLevel1Sector.objects.all().delete()
        WorkflowTeam.objects.all().delete()

    def _create_organization(self):
        try:
            self._organization = Organization.objects.get(**DEFAULT_ORG)
        except Organization.DoesNotExist:
            self._organization = factories.Organization(
                id=DEFAULT_ORG['id'],
                name=DEFAULT_ORG['name'],
                organization_url="http://toladata.com",
                level_2_label="Project",
                level_3_label="Activity",
                level_4_label="Component",
            )

    def _create_groups(self):
        self._groups.append(factories.Group(
            id=1,
            name=ROLE_VIEW_ONLY,
        ))

        self._groups.append(factories.Group(
            id=2,
            name=ROLE_ORGANIZATION_ADMIN,
        ))

        self._groups.append(factories.Group(
            id=3,
            name=ROLE_PROGRAM_ADMIN,
        ))

        self._groups.append(factories.Group(
            id=4,
            name=ROLE_PROGRAM_TEAM,
        ))

    def _create_countries(self):
        factories.Country(
            country="Afghanistan",
            code="AF",
            latitude="34.5333",
            longitude="69.1333",
        )

        factories.Country(
            country="Pakistan",
            code="PK",
            latitude="33.6667",
            longitude="73.1667",
        )

        factories.Country(
            country="Jordan",
            code="JO",
            latitude="31.9500",
            longitude="35.9333",
        )

        factories.Country(
            country="Lebanon",
            code="LB",
            latitude="33.9000",
            longitude="35.5333",
        )

        factories.Country(
            country="Ethiopia",
            code="ET",
            latitude="9.0167",
            longitude="38.7500",
        )

        factories.Country(
            country="Timor-Leste",
            code="TL",
            latitude="-8.3",
            longitude="125.5667",
        )

        factories.Country(
            country="Kenya",
            code="KE",
            latitude="-1.2833",
            longitude="36.8167",
        )

        factories.Country(
            country="Iraq",
            code="IQ",
            latitude="33.3333",
            longitude="44.4333",
        )

        factories.Country(
            country="Nepal",
            code="NP",
            latitude="26.5333",
            longitude="86.7333",
        )

        factories.Country(
            country="Mali",
            code="ML",
            latitude="17.6500",
            longitude="0.0000",
        )

        factories.Country(
            country="United States",
            code="US",
            latitude="45",
            longitude="-120",
        )

        factories.Country(
            country="Turkey",
            code="TR",
            latitude="39.9167",
            longitude="32.8333",
        )

        self._country_syria = factories.Country(
            country="Syrian Arab Republic",
            code="SY",
            latitude="33.5000",
            longitude="36.3000",
        )

        factories.Country(
            country="China",
            code="CN",
        )

        factories.Country(
            country="India",
            code="IN",
        )

        factories.Country(
            country="Indonesia",
            code="ID",
        )

        factories.Country(
            country="Mongolia",
            code="MN",
        )

        factories.Country(
            country="Myanmar",
            code="MY",
            latitude="21.9162",
            longitude="95.9560",
        )

        factories.Country(
            country="Palestine",
            code="PS",
            latitude="31.3547",
            longitude="34.3088",
        )

        factories.Country(
            country="South Sudan",
            code="SS",
            latitude="6.8770",
            longitude="31.3070",
        )

        factories.Country(
            country="Uganda",
            code="UG",
            latitude="1.3733",
            longitude="32.2903",
        )

        self._country_germany = factories.Country(
            country="Germany",
            code="DE",
            latitude="51.1657",
            longitude="10.4515",
        )

    def _create_sectors(self):
        self._sectors.append(factories.Sector(
            id="1",  # 129"
            sector="Agriculture",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="2",  # 131"
            sector="Agribusiness",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="3",  # 132"
            sector="Fisheries",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="4",  # 133"
            sector="Basic Needs",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="5",  # 134"
            sector="Basic Health Care",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="6",  # 135"
            sector="Basic Health Infrastructure",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="7",  # 136"
            sector="Basic Nutrition",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="8",  # 137"
            sector="Basic Life Skills For Youth",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="9",  # 138"
            sector="Basic Drinking Water Supply And Basic Sanitation",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="10",  # 139"
            sector="Basic Sanitation",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="11",  # 140
            sector="Basic Education",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="12",  # 141
            sector="Capacity development",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="13",  # 142
            sector="Child Health & Nutrition",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="14",  # 143
            sector="Emergency Response",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="15",  # 144
            sector="Climate Change Adaptation & Disaster Risk Reduction",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="16",  # 145
            sector="Climate Change Adaptation",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="17",  # 146
            sector="Disaster Risk Reduction",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="18",  # 147
            sector="Resilience",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="19",  # 148
            sector="Conflict Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="20",  # 149
            sector="Peacebuilding",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="21",  # 150
            sector="Conflict Prevention And Resolution",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="22",  # 151
            sector="Early Recovery",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="23",  # 152
            sector="Economic Recovery and Livelihoods",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="24",  # 153
            sector="Basic Infrastructure Restoration",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="25",  # 154
            sector="Economic and Market Development",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="26",  # 155
            sector="Private Sector Development",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="27",  # 156
            sector="Employment Opportunities",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="28",  # 157
            sector="Livelihood Improvement",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="29",  # 158
            sector="Enterprise Development",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="30",  # 159
            sector="Entrepreneurship",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="31",  # 160
            sector="Education",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="32",  # 161
            sector="Primary Education",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="33",  # 162
            sector="Secondary Education",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="34",  # 163
            sector="Post-Secondary Education",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="35",  # 164
            sector="Vocational Training",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="36",  # 165
            sector="Informal Education/Life skills",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="37",  # 166
            sector="Shelter",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="38",  # 167
            sector="Non-food Items (NFI)",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="39",  # 168
            sector="Fuel/Energy",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="40",  # 169
            sector="Social Support",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="41",  # 170
            sector="Information Dissemination",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="42",  # 171
            sector="Energy",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="43",  # 172
            sector="Access to Electricity",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="44",  # 173
            sector="Access to Clean Cooking Facilities",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="45",  # 174
            sector="Energy Efficiency",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="46",  # 175
            sector="Renewable Energy",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="47",  # 176
            sector="Financial services",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="48",  # 177
            sector="Financial Services",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="49",  # 178
            sector="Financial Inclusion",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="50",  # 179
            sector="Cash for Work",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="51",  # 180
            sector="Food Security",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="52",  # 181
            sector="Food Assistance",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="53",  # 182
            sector="Food Access",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="54",  # 183
            sector="Food Availability",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="55",  # 184
            sector="Agriculture and Livestock",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="56",  # 185
            sector="Gender",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="57",  # 186
            sector="Governance",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="58",  # 187
            sector="Democratic Participation And Civil Society",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="59",  # 188
            sector="Education Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="60",  # 189
            sector="Water Sector Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="61",  # 190
            sector="Fishing Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="62",  # 191
            sector="Agricultural Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="63",  # 192
            sector="Health Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="64",  # 193
            sector="Population Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="65",  # 194
            sector="Public Sector Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="66",  # 195
            sector="Social Protection And Welfare Services Policy, Planning And Administration",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="67",  # 196
            sector="Employment Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="68",  # 197
            sector="Housing Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="69",  # 198
            sector="Transport Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="70",  # 199
            sector="Communications Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="71",  # 200
            sector="Energy Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="72",  # 201
            sector="Financial Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="73",  # 202
            sector="Rural Land Policy And Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="74",  # 203
            sector="Urban Land Policy And Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="75",  # 204
            sector="Environmental Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="76",  # 205
            sector="Tourism Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="77",  # 206
            sector="Trade Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="78",  # 207
            sector="Construction Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="79",  # 208
            sector="Mineral/Mining Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="80",  # 209
            sector="Industrial Policy And Administrative Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="81",  # 210
            sector="Health",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="82",  # 211
            sector="General Clinical Services",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="83",  # 212
            sector="Maternal Health and Newborn Care",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="84",  # 213
            sector="Child Healh",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="85",  # 214
            sector="Sexual Violence",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="86",  # 215
            sector="Psychosocial support",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="87",  # 216
            sector="Infectious Diseases",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="88",  # 217
            sector="Human rights",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="89",  # 218
            sector="Information Dissemination and Knowledge Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="90",  # 219
            sector="Infrastructure",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="91",  # 220
            sector="Water supply Infrastructure",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="92",  # 221
            sector="Natural Resource Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="93",  # 222
            sector="Water Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="94",  # 223
            sector="Land Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="95",  # 224
            sector="Nutrition",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="96",  # 225
            sector="Infant Feeding",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="97",  # 226
            sector="Protection",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="98",  # 227
            sector="Child Protection",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="99",  # 228
            sector="Gender-Based Violence",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="100",  # 229
            sector="Housing Land and Property",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="101",  # 230
            sector="Water, Sanitation, and Hygiene (WASH)",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="102",  # 231
            sector="Water Supply",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="103",  # 232
            sector="Hygiene Promotion",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="104",  # 233
            sector="Excreta Disposal",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="105",  # 234
            sector="Solid Waste Management",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="106",  # 235
            sector="Youth Development",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="107",  # 236
            sector="Malnutrition Prevention",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="108",  # 237
            sector="Micronutrient Deficiency Prevention",
            organization=self._organization,
        ))

        self._sectors.append(factories.Sector(
            id="109",
            sector="Children's Rights",
            organization=self._organization,
        ))

    def _create_indicator_types(self):
        factories.IndicatorType(
            id=1,
            indicator_type="Custom",
            organization=self._organization,
        )

        factories.IndicatorType(
            id=2,
            indicator_type="Donor",
            organization=self._organization,
        )

        factories.IndicatorType(
            id=3,
            indicator_type="Standard",
            organization=self._organization,
        )

    def _create_users(self):
        self._tolauser_andrew = factories.TolaUser(
            # id=9
            name="Andrew Ham",
            user=factories.User(first_name="Andrew", last_name="Ham"),
            organization=self._organization,
            country=self._country_germany,
        )

        self._tolauser_ninette = factories.TolaUser(
            # id=11
            name="Ninette Dedikari",
            user=factories.User(first_name="Ninette", last_name="Dedikari"),
            organization=self._organization,
            country=self._country_germany,
        )

    def _create_site_profiles(self):
        self._site_profiles.append(factories.SiteProfile(
            id=1,  # 5
            name="Medical Center 1 - Damascus",
            country=self._country_syria,  # 14
            latitude="33.500",
            longitude="36.300",
            created_by=self._tolauser_ninette.user,  # 11
            organization=self._organization,
        ))

        self._site_profiles.append(factories.SiteProfile(
            id=2,  # 6
            name="Medical Center 2 - Aleppo",
            country=self._country_syria,  # 14
            latitude="36.2130824982",
            longitude="37.1569335937",
            created_by=self._tolauser_ninette.user,  # 11
            organization=self._organization,
        ))

        self._site_profiles.append(factories.SiteProfile(
            id=3,  # 7
            name="Medical Center 3 - Hamma",
            country=self._country_syria,  # 14
            latitude="35.1421960686",
            longitude="36.7504394531",
            created_by=self._tolauser_ninette.user,  # 11
            organization=self._organization,
        ))

        self._site_profiles.append(factories.SiteProfile(
            id=4,  # 8,
            name="Medical Center 4 - Tartus",
            country=self._country_syria,  # 14
            latitude="34.8959",
            longitude="35.8867",
            created_by=self._tolauser_ninette.user,  # 11
            organization=self._organization,
        ))

        self._site_profiles.append(factories.SiteProfile(
            id=5,  # 9
            name="Medical Center 5 - Homs",
            country=self._country_syria,  # 14
            latitude="34.7369225399",
            longitude="36.7284667969",
            created_by=self._tolauser_ninette.user,  # 11
            organization=self._organization,
        ))

        self._site_profiles.append(factories.SiteProfile(
            id=6,
            name="Paul Schule",
            contact_leader="Direktor Paul Schule",
            country=self._country_germany,
            latitude="50.9692657293000000",
            longitude="6.9889383750000000",
            created_by=self._tolauser_ninette.user,
            organization=self._organization,
        ))

        self._site_profiles.append(factories.SiteProfile(
            id=7,
            name="Peter Schule",
            contact_leader="Direktor Peter Schule",
            country=self._country_germany,
            latitude="49.4507464458000000",
            longitude="11.0319071250000000",
            created_by=self._tolauser_ninette.user,
            organization=self._organization,
        ))

    def _create_stakeholders(self):
        factories.Stakeholder(
            id=1,  # 2
            name="Municipal Government Official",
            role="Bulk Transport Services",
            country=self._country_syria,  # 14
            organization=self._organization,
            created_by=self._tolauser_ninette.user,  # 11
        )

    def _create_milestones(self):
        factories.Milestone(
            id="1",
            name="1. Identification and Design",
            milestone_start_date="2017-07-01T10:00:00Z",  # TODO
            milestone_end_date="2018-05-11T10:00:00Z",  # TODO
            organization=self._organization,
            created_by=self._tolauser_ninette.user,  # 11
        )

        factories.Milestone(
            id="2",
            name="2. Setup and Planning",
            milestone_start_date="2017-07-01T10:00:00Z",  # TODO
            milestone_end_date="2018-05-11T10:00:00Z",  # TODO
            organization=self._organization,
            created_by=self._tolauser_ninette.user,  # 11
        )

        factories.Milestone(
            id="3",
            name="3. Implementation",
            milestone_start_date="2017-07-01T10:00:00Z",  # TODO
            milestone_end_date="2018-05-11T10:00:00Z",  # TODO
            organization=self._organization,
            created_by=self._tolauser_ninette.user,  # 11
        )

        factories.Milestone(
            id="4",
            name="4. Close Out",
            milestone_start_date="2017-07-01T10:00:00Z",  # TODO
            milestone_end_date="2018-05-11T10:00:00Z",  # TODO
            organization=self._organization,
            created_by=self._tolauser_ninette.user,  # 11
        )

        factories.Milestone(
            id="5",
            name=u"Auswahl Schulen",
            milestone_start_date="2017-07-01T10:00:00Z",  # TODO
            milestone_end_date="2018-05-11T10:00:00Z",  # TODO
            organization=self._organization,
            created_by=self._tolauser_ninette.user,  # 11
        )

        factories.Milestone(
            id="6",
            name=u"Durchführung Ideen Workshops",
            milestone_start_date="2017-07-01T10:00:00Z",  # TODO
            milestone_end_date="2018-05-11T10:00:00Z",  # TODO
            organization=self._organization,
            created_by=self._tolauser_ninette.user,  # 11
        )

        factories.Milestone(
            id="7",
            name=u"Familien Fortbildungen",
            milestone_start_date="2017-07-01T10:00:00Z",  # TODO
            milestone_end_date="2018-05-11T10:00:00Z",  # TODO
            organization=self._organization,
            created_by=self._tolauser_ninette.user,  # 11
        )

        factories.Milestone(
            id="8",
            name=u"Qualifizierung Lehrer",
            milestone_start_date="2017-07-01T10:00:00Z",  # TODO
            milestone_end_date="2018-05-11T10:00:00Z",  # TODO
            organization=self._organization,
            created_by=self._tolauser_ninette.user,  # 11
        )

    def _create_workflow_1s(self):
        self._workflowlevel1s.append(factories.WorkflowLevel1(
            id=1,  # 10
            name='Financial Assistance and Building Resilience in Conflict Areas',
            funding_status="Funded",
            organization=self._organization,
            description="<p>Build resilience among affected communities through improving access to finance</p>",
            country=[],
            start_date="2017-07-01T10:00:00Z",  # TODO use current date?
            end_date="2019-06-30T10:00:00Z",  # TODO +2y?
            user_access=[self._tolauser_andrew],  # 9
        ))

        self._workflowlevel1s.append(factories.WorkflowLevel1(
            id=2,  # 11
            name='Population Health Initiative',
            organization=self._organization,
            description="<p>Build resilience among affected communities through improving access to finance</p>",
            country=[],
            start_date="2017-07-01T10:00:00Z",  # TODO
            end_date="2019-06-30T10:00:00Z",  # TODO
            user_access=[self._tolauser_ninette],  # 11
        ))

        self._workflowlevel1s.append(factories.WorkflowLevel1(
            id=3,  # 15
            name='Humanitarian Response to the Syrian Crisis',
            funding_status="Funded",
            organization=self._organization,
            description="<p>Newly funded program</p>",
            country=[self._country_syria],  # 14
            start_date="2017-07-01T10:00:00Z",  # TODO
            end_date="2019-06-30T10:00:00Z",  # TODO
            milestone=[1, 2, 3, 4],
            user_access=[self._tolauser_andrew],  # 9
        ))

        self._workflowlevel1s.append(factories.WorkflowLevel1(
            id=4,  # 18
            name='Institutional Learning Initiative',
            organization=self._organization,
            start_date="2017-07-01T10:00:00Z",  # TODO
            end_date="2019-06-30T10:00:00Z",  # TODO
        ))

        self._workflowlevel1s.append(factories.WorkflowLevel1(
            id=5,  # 19
            name='Building resilience in Mali',
            organization=self._organization,
            start_date="2017-07-01T10:00:00Z",  # TODO
            end_date="2019-06-30T10:00:00Z",  # TODO
        ))

        self._workflowlevel1s.append(factories.WorkflowLevel1(
            id=6,
            name=u'Bildung für sozial benachteiligte Kinder in Deutschland',
            organization=self._organization,
            start_date="2017-07-01T10:00:00Z",  # TODO
            end_date="2019-06-30T10:00:00Z",  # TODO
            milestone=[5, 6, 7, 8],
        ))

    def _create_workflow_2s(self):
        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=1,  # 2
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=0,
            name='Planning: How to map out a project',
            expected_start_date="2018-01-01T11:00:00Z",  # TODO
            expected_end_date="2018-01-31T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=2,  # 3
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=1,  # 2
            name='Determine the real problem to solve',
            expected_start_date="2018-01-15T11:00:00Z",  # TODO
            expected_end_date="2018-01-19T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=3,  # 4
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=1,  # 2
            name='Identify Stakeholders',
            expected_start_date="2017-12-20T11:00:00Z",  # TODO
            expected_end_date="2018-01-26T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=4,  # 5
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=1,  # 2
            name='Define project objectives',
            expected_start_date="2018-01-01T11:00:00Z",  # TODO
            expected_end_date="2018-01-05T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=5,  # 6
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=1,  # 2
            name='Determine scope, resources and major tasks',
            expected_start_date="2018-01-08T11:00:00Z",  # TODO
            expected_end_date="2018-01-12T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=6,  # 7
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=1,  # 2
            name='Prepare for trade-offs',
            expected_start_date="2018-01-29T11:00:00Z",  # TODO
            expected_end_date="2018-01-31T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=7,  # 8
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=0,
            name='Build-up: How to get the project started',
            expected_start_date="2017-11-01T11:00:00Z",  # TODO
            expected_end_date="2017-12-31T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="",
            site=[self._site_profiles[1], self._site_profiles[2], self._site_profiles[3], self._site_profiles[4], self._site_profiles[5]],  # [5, 6, 7, 8, 9]
            stakeholder=[1],  # 2
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=8,  # 9
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=7, # 8
            name='Assemble your team',
            expected_start_date="2017-11-01T11:00:00Z",  # TODO
            expected_end_date="2017-11-10T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=9,  # 10
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=7, # 8
            name='Plan assignments',
            expected_start_date="2017-12-01T11:00:00Z",  # TODO
            expected_end_date="2017-12-08T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=10,  # 11
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=7, # 8
            name='Create the schedule',
            expected_start_date="2017-11-13T11:00:00Z",  # TODO
            expected_end_date="2017-11-17T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=11,  # 12
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=7, # 8
            name='Hold a kickoff meeting',
            expected_start_date="2017-11-27T11:00:00Z",  # TODO
            expected_end_date="2017-11-30T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=12,  # 13
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=7, # 8
            name='Develop a budget',
            expected_start_date="2017-11-20T11:00:00Z",  # TODO
            expected_end_date="2017-11-24T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=13,  # 14
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=0,
            name='Implementation: How to execute the project',
            expected_start_date="2018-02-01T11:00:00Z",  # TODO
            expected_end_date="2018-08-31T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=14,  # 15
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=13,  # 14
            name='Monitor and control procress and budget',
            expected_start_date="2018-04-02T11:00:00Z",  # TODO
            expected_end_date="2018-08-31T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=15,  # 16
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=13,  # 14
            name='Report progress',
            expected_start_date="2018-06-01T11:00:00Z",  # TODO
            expected_end_date="2018-08-31T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=16,  # 17
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=13,  # 14
            name='Hold weekly team meetings',
            description="<p>Weekly meetings held every Monday</p>",
            expected_start_date="2018-02-01T11:00:00Z",  # TODO
            expected_end_date="2018-04-30T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=17,  # 18
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=13,  # 14
            name='Manage problems',
            expected_start_date="2018-02-01T11:00:00Z",  # TODO
            expected_end_date="2018-08-31T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=18,  # 19
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=0,
            name='Closeout: How to handle end matters',
            expected_start_date="2018-09-01T11:00:00Z",  # TODO
            expected_end_date="2018-10-31T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=19,  # 20
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=18,  # 19
            name='Evaluate project performance',
            expected_start_date="2018-10-15T11:00:00Z",  # TODO
            expected_end_date="2018-10-31T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=20,  # 21
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=18,  # 19
            name='Close the project',
            expected_start_date="2018-09-03T11:00:00Z",  # TODO
            expected_end_date="2018-09-28T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=21,  # 22
            workflowlevel1=self._workflowlevel1s[3],  # 15
            parent_workflowlevel2=18,  # 19
            name='Debrief with the team',
            expected_start_date="2018-10-01T11:00:00Z",  # TODO
            expected_end_date="2018-09-30T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="open",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=22,
            workflowlevel1=self._workflowlevel1s[6],
            parent_workflowlevel2=0,
            name=u'Ansprache von 20 Partnerschulen in Berlin',
            expected_start_date="2018-10-01T11:00:00Z",  # TODO
            expected_end_date="2018-09-30T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="closed",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=23,
            workflowlevel1=self._workflowlevel1s[6],
            parent_workflowlevel2=0,
            name=u'20 Schulen in sozialen Brennpunkten identifizieren',
            expected_start_date="2018-10-01T11:00:00Z",  # TODO
            expected_end_date="2018-09-30T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="closed",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=24,
            workflowlevel1=self._workflowlevel1s[6],
            parent_workflowlevel2=0,
            name=u'Ideen zur Gestaltung der Schule finden und umstetzen',
            expected_start_date="2018-10-01T11:00:00Z",  # TODO
            expected_end_date="2018-09-30T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            on_time=False,
            progress="tracking",
            status="yellow",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=25,
            workflowlevel1=self._workflowlevel1s[6],
            parent_workflowlevel2=0,
            name=u'Qualifizierung der Lehrer',
            expected_start_date="2018-10-01T11:00:00Z",  # TODO
            expected_end_date="2018-09-30T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            on_time=False,
            progress="closed",
            status="yellow",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=26,
            workflowlevel1=self._workflowlevel1s[6],
            parent_workflowlevel2=25,
            name=u'Lehrer auswählen',
            expected_start_date="2018-10-01T11:00:00Z",  # TODO
            expected_end_date="2018-09-30T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="closed",
            status="yellow",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=27,
            workflowlevel1=self._workflowlevel1s[6],
            parent_workflowlevel2=25,
            name=u'Trainings und Supervision durchführen',
            expected_start_date="2018-10-01T11:00:00Z",  # TODO
            expected_end_date="2018-09-30T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="tracking",
            status="yellow",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=28,
            workflowlevel1=self._workflowlevel1s[6],
            parent_workflowlevel2=24,
            name=u'Ideenworkshops durchführen',
            expected_start_date="2018-10-01T11:00:00Z",  # TODO
            expected_end_date="2018-09-30T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="tracking",
            status="yellow",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=29,
            workflowlevel1=self._workflowlevel1s[6],
            parent_workflowlevel2=22,
            name=u'Direktoren ansprechen',
            expected_start_date="2018-10-01T11:00:00Z",  # TODO
            expected_end_date="2018-09-30T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="closed",
            status="green",
        ))

        self._workflowlevel2s.append(factories.WorkflowLevel2(
            id=30,
            workflowlevel1=self._workflowlevel1s[6],
            parent_workflowlevel2=24,
            name=u'Budgets zur Umsetzung finden',
            expected_start_date="2018-10-01T11:00:00Z",  # TODO
            expected_end_date="2018-09-30T11:00:00Z",  # TODO
            created_by=self._tolauser_ninette.user,  # 11
            progress="awaitingapproval",
            status="red",
        ))

    def _create_levels(self):
        self._levels.append(factories.Level(
            id=1,  # 7
            name="Goal",
            description="Improved health and survival of Syrian communities affected by conflict",
            color="navy",
            organization=self._organization,
            parent_id="0",
            workflowlevel1=self._workflowlevel1s[3],  # 15
            sort=0,
        ))

        self._levels.append(factories.Level(
            id=2,  # 8
            name="Intermediate Result",
            description="Improved recovery from injuries as a result of conflict",
            color="red",
            organization=self._organization,
            parent_id="1",  # 7
            workflowlevel1=self._workflowlevel1s[3],  # 15
            sort=1,
        ))

        self._levels.append(factories.Level(
            id=3,  # 9
            name="Outcome 1",
            description="Emergency medical services improve in areas where emergency medical kits are provided",
            color="blue",
            organization=self._organization,
            parent_id="2",  # 8
            workflowlevel1=self._workflowlevel1s[3],  # 15
            sort=2,
        ))

        self._levels.append(factories.Level(
            id=4,  # 10
            name="Outcome 2",
            description="Community members with improved knowledge of hygiene practices",
            color="blue",
            organization=self._organization,
            parent_id="2",  # 8
            workflowlevel1=self._workflowlevel1s[3],  # 15
            sort=2,
        ))

        self._levels.append(factories.Level(
            id=5,  # 11
            name="Output 1",
            description="Emergency Medical Kits are delivered to mobile medical units in conflict-affected populations",
            color="green",
            organization=self._organization,
            parent_id="3",  # 9
            workflowlevel1=self._workflowlevel1s[3],  # 15
            sort=3,
        ))

        self._levels.append(factories.Level(
            id=6,  # 12
            name="Output 2",
            description="Treat injuries and emergency medical needs of affected communities",
            color="green",
            organization=self._organization,
            parent_id="3",  # 9
            workflowlevel1=self._workflowlevel1s[3],  # 15
            sort=3,
        ))

        self._levels.append(factories.Level(
            id=7,  # 13
            name="Output 3",
            description="Hand Washing Knowledge and Capacity",
            color="green",
            organization=self._organization,
            parent_id="4",  # 10
            workflowlevel1=self._workflowlevel1s[3],  # 15
            sort=3,
        ))

        self._levels.append(factories.Level(
            id=8,  # 14
            name="Output 4",
            description="Household Water Quality is Improved",
            color="green",
            organization=self._organization,
            parent_id="4",  # 10
            workflowlevel1=self._workflowlevel1s[3],  # 15
            sort=3,
        ))

        self._levels.append(factories.Level(
            id=9,
            name=(u"Impact: Verwirklichung des Kinderrechts auf Bildung in "
                  u"Deutschland"),
            description=(u"Verwirklichung der Rechte Kindern aus sozial "
                         u"benachteiligten Bevölkerungsgruppen auf qualitativ "
                         u"hochwertige Bildung und Entwicklung"),
            color="red",
            organization=self._organization,
            parent_id="0",
            workflowlevel1=self._workflowlevel1s[6],
            sort=0,
        ))

        self._levels.append(factories.Level(
            id=10,
            name=u"Outcome: Gute Bildung und Lernen ermöglichen",
            description=(u"Ziel ist es, Kindern unabhängig von ihrem "
                         u"Hintergrund und ihrer Herkunft die Möglichkeit auf "
                         u"gute Bildung und erfolgreiches Lernen zu "
                         u"ermöglichen"),
            color="blue",
            organization=self._organization,
            parent_id="9",
            workflowlevel1=self._workflowlevel1s[6],
            sort=1,
        ))

        self._levels.append(factories.Level(
            id=11,
            name=u"Outcome: Kooperation zwischen Eltern/Lehrern verbessern",
            description=(u"Ziel ist es, eine stabile Beziehung zwischen "
                        u"Eltern und Lehrern zu bauen, Eltern in die "
                         u"Aktivitäten der Schule einzubeziehen und eine "
                         u"stabile Kommunikation aufzubauen."),
            color="blue",
            organization=self._organization,
            parent_id="9",
            workflowlevel1=self._workflowlevel1s[6],
            sort=1,
        ))

        self._levels.append(factories.Level(
            id=12,
            name=u"Outcome: Schulen familienfreundlicher gestalten",
            description=(u"Ziel ist es, Schulen nicht nur als Raum zum Lernen, "
                         u"sondern auch zum Leben zu gestalten. Eine offene "
                         u"und vertrauensvolle Atmosphäre zu kreieren, in dem "
                         u"die ganze Persönlichkeit gesehen und gefördert "
                         u"wird."),
            color="green",
            organization=self._organization,
            parent_id="9",
            workflowlevel1=self._workflowlevel1s[6],
            sort=1,
        ))

        self._levels.append(factories.Level(
            id=13,
            name=u"Output: Schulungen für Familien durchführen",
            description=u"",
            color="green",
            organization=self._organization,
            parent_id="10",
            workflowlevel1=self._workflowlevel1s[6],
            sort=2,
        ))

        self._levels.append(factories.Level(
            id=14,
            name=u"Output: Elternbeteiligung stärken",
            description=u"",
            color="green",
            organization=self._organization,
            parent_id="11",
            workflowlevel1=self._workflowlevel1s[6],
            sort=2,
        ))

        self._levels.append(factories.Level(
            id=15,
            name=u"Output: Partnerschaftliches Verhältnis etablieren",
            description=u"",
            color="green",
            organization=self._organization,
            parent_id="11",
            workflowlevel1=self._workflowlevel1s[6],
            sort=2,
        ))

        self._levels.append(factories.Level(
            id=16,
            name=u"Output: Fortbildungen für Lehrer",
            description=u"",
            color="green",
            organization=self._organization,
            parent_id="10",
            workflowlevel1=self._workflowlevel1s[6],
            sort=2,
        ))

        self._levels.append(factories.Level(
            id=17,
            name=u"Output: Ideen partizipativ entwickeln und umsetzen",
            description=u"",
            color="green",
            organization=self._organization,
            parent_id="12",
            workflowlevel1=self._workflowlevel1s[6],
            sort=2,
        ))

        self._levels.append(factories.Level(
            id=18,
            name=u"Output: Sprachbarrieren abbauen",
            description=u"",
            color="green",
            organization=self._organization,
            parent_id="11",
            workflowlevel1=self._workflowlevel1s[6],
            sort=2,
        ))

    def _create_frequencies(self):
        self._frequencies.append(factories.Frequency(
            id=1,  # 2
            frequency="Quarterly",
            description="Quarterly",
            organization=self._organization,
        ))

        self._frequencies.append(factories.Frequency(
            id=2,  # 4
            frequency="Monthly",
            description="Monthly",
            organization=self._organization,
        ))

        self._frequencies.append(factories.Frequency(
            id=3,  # 5
            frequency="Semi Annual",
            description="Semi Annual",
            organization=self._organization,
        ))

        self._frequencies.append(factories.Frequency(
            id=4,  # 7
            frequency="Annual",
            description="Annual",
            organization=self._organization,
        ))

        self._frequencies.append(factories.Frequency(
            id=5,  # 8
            frequency="Baseline, Endline",
            description="Baseline, Endline",
            organization=self._organization,
        ))

        self._frequencies.append(factories.Frequency(
            id=6,  # 9
            frequency="Weekly",
            description="Weekly",
            organization=self._organization,
        ))

        self._frequencies.append(factories.Frequency(
            id=7,  # 10
            frequency="Baseline, midline, endline",
            description="Baseline, midline, endline",
            organization=self._organization,
        ))

        self._frequencies.append(factories.Frequency(
            id=8,  # 11
            frequency="Bi-weekly",
            description="Bi-weekly",
            organization=self._organization,
        ))

        self._frequencies.append(factories.Frequency(
            id=9,  # 12
            frequency="Monthly, Quarterly, Annually",
            description="Monthly, Quarterly, Annually",
            organization=self._organization,
        ))

        self._frequencies.append(factories.Frequency(
            id=10,  # 16
            frequency="End of cycle",
            description="End of cycle",
            organization=self._organization,
        ))

    def _create_indicators(self):
        self._indicators.append(factories.Indicator(
            id=1,  # 2
            level=self._levels[1],  # 7
            name="# of individuals in a need of humanitarian assistance",
            number="1",
            lop_target=7500,
            key_performance_indicator=True,
            created_by=self._tolauser_ninette.user,  # 11
            workflowlevel1=[self._workflowlevel1s[3]],  # 15
        ))

        self._indicators.append(factories.Indicator(
            id=2,  # 3
            level=self._levels[2],  # 8
            name="% of injured community members who make full recovery",
            number="1.1",
            lop_target=70,
            key_performance_indicator=False,
            created_by=self._tolauser_ninette.user,  # 11
            workflowlevel1=[self._workflowlevel1s[3]],  # 15
        ))

        self._indicators.append(factories.Indicator(
            id=3,  # 4
            level=self._levels[3],  # 9
            name="% of mobile medical units who have adequate supply of emergency medical kits",
            number="2.1",
            lop_target=80,
            key_performance_indicator=False,
            created_by=self._tolauser_ninette.user,  # 11
            workflowlevel1=[self._workflowlevel1s[3]],  # 15
        ))

        self._indicators.append(factories.Indicator(
            id=4,  # 5
            level=self._levels[4],  # 10
            name="% of respondents who know 3 of 5 critical times to wash hands",
            number="3.1",
            lop_target=75,
            key_performance_indicator=False,
            created_by=self._tolauser_ninette.user,  # 11
            workflowlevel1=[self._workflowlevel1s[3]],  # 15
        ))

        self._indicators.append(factories.Indicator(
            id=5,  # 6
            level=self._levels[5],  # 11
            name="# of medical kits provided to partner mobile medical units",
            number="2.1.1",
            lop_target=2500,
            key_performance_indicator=False,
            created_by=self._tolauser_ninette.user,  # 11
            workflowlevel1=[self._workflowlevel1s[3]],  # 15
        ))

        self._indicators.append(factories.Indicator(
            id=6,  # 7
            level=self._levels[5],  # 11
            name="% of emergency medical kits distributed within two weeks of identification of critical need",
            number="2.1.2",
            lop_target=60,
            key_performance_indicator=False,
            created_by=self._tolauser_ninette.user,  # 11
            workflowlevel1=[self._workflowlevel1s[3]],  # 15
        ))

        self._indicators.append(factories.Indicator(
            id=7,  # 8
            level=self._levels[3],  # 9
            name="# of beneficiaries treated",
            number="2.2.1",
            lop_target=500,
            key_performance_indicator=False,
            created_by=self._tolauser_ninette.user,  # 11
            workflowlevel1=[self._workflowlevel1s[3]],  # 15
        ))

        self._indicators.append(factories.Indicator(
            id=8,  # 9
            level=self._levels[6],  # 12
            name="# of locations set up by mobile medical units",
            number="2.2.2",
            lop_target=10,
            key_performance_indicator=False,
            created_by=self._tolauser_ninette.user,  # 11
            workflowlevel1=[self._workflowlevel1s[3]],  # 15
        ))

        self._indicators.append(factories.Indicator(
            id=9,  # 10
            level=self._levels[6],  # 12
            name="# of days mobile medical units spent at each location",
            number="2.2.3",
            lop_target=5,
            key_performance_indicator=False,
            created_by=self._tolauser_ninette.user,  # 11
            workflowlevel1=[self._workflowlevel1s[3]],  # 15
        ))

        self._indicators.append(factories.Indicator(
            id=10,  # 11
            level=self._levels[7],  # 13
            name="# of people receiving hygiene promotion",
            number="3.1.1",
            lop_target=5000,
            key_performance_indicator=False,
            created_by=self._tolauser_ninette.user,  # 11
            workflowlevel1=[self._workflowlevel1s[3]],  # 15
        ))

        self._indicators.append(factories.Indicator(
            id=11,  # 12
            level=self._levels[8],  # 14
            name="# of people receiving household water quality education",
            number="3.2.1",
            lop_target=5000,
            key_performance_indicator=False,
            created_by=self._tolauser_ninette.user,  # 11
            workflowlevel1=[self._workflowlevel1s[3]],  # 15
        ))

        self._indicators.append(factories.Indicator(
            id=12,  # 13
            level=self._levels[8],  # 14
            name="# of individuals in acute need of humanitarian assistance",
            number="1",
            lop_target=7500,
            sector=self._sectors[44],  # 173
            key_performance_indicator=True,
            created_by=self._tolauser_ninette.user,  # 11
            workflowlevel1=[self._workflowlevel1s[3]],  # 15
        ))

        self._indicators.append(factories.Indicator(
            id=13,
            level=self._levels[9],
            name=u"Anzahl aktive Initiativen",
            lop_target=5500,
            key_performance_indicator=True,
            created_by=self._tolauser_ninette.user,
            reporting_frequency=self._frequencies[9],
            workflowlevel1=[self._workflowlevel1s[6]],
        ))

        self._indicators.append(factories.Indicator(
            id=14,
            level=self._levels[13],
            name=u"Anzahl Schulungen",
            number="5000",
            lop_target=50000,
            key_performance_indicator=True,
            created_by=self._tolauser_ninette.user,
            reporting_frequency=self._frequencies[9],
            method_of_analysis="Questionnaire",
            workflowlevel1=[self._workflowlevel1s[6]],
        ))

        self._indicators.append(factories.Indicator(
            id=15,
            level=self._levels[12],
            name=u"Ideenwerkstätten",
            lop_target=15000,
            key_performance_indicator=False,
            created_by=self._tolauser_ninette.user,
            reporting_frequency=self._frequencies[9],
            workflowlevel1=[self._workflowlevel1s[6]],
        ))

        self._indicators.append(factories.Indicator(
            id=16,
            level=self._levels[9],
            name=u"Anzahl direkt erreichter Kinder",
            lop_target=250000,
            key_performance_indicator=True,
            approval_submitted_by=self._tolauser_andrew,
            created_by=self._tolauser_ninette.user,
            reporting_frequency=self._frequencies[9],
            workflowlevel1=[self._workflowlevel1s[6]],
        ))

        self._indicators.append(factories.Indicator(
            id=17,
            level=self._levels[11],
            name=u"Mehrsprachige Informationsmaterialien (10 Sprachen)",
            lop_target=600000,
            sector=self._sectors[11],
            key_performance_indicator=False,
            approval_submitted_by=self._tolauser_andrew,
            created_by=self._tolauser_ninette.user,
            reporting_frequency=self._frequencies[9],
            workflowlevel1=[self._workflowlevel1s[6]],
        ))

    def _create_periodic_targets(self):
        factories.PeriodicTarget(
            id="1",  # 1
            period="February 2018",
            target="500.00",
            indicator=self._indicators[1],  # 2
        )

        factories.PeriodicTarget(
            id="2",  # 2
            period="March 2018",
            target="1000.00",
            indicator=self._indicators[1],  # 2
        )

        factories.PeriodicTarget(
            id="3",  # 3
            period="April 2018",
            target="1000.00",
            indicator=self._indicators[1],  # 2
        )

        factories.PeriodicTarget(
            id=4,  # 4
            period="May 2018",
            target="1500.00",
            indicator=self._indicators[1],  # 2
        )

        factories.PeriodicTarget(
            id=5,  # 5
            period="June 2018",
            target="1500.00",
            indicator=self._indicators[1],  # 2
        )

        factories.PeriodicTarget(
            id=6,  # 6
            period="July 2018",
            target="1000.00",
            indicator=self._indicators[1],  # 2
        )

        factories.PeriodicTarget(
            id=7,  # 10
            period="August 2018",
            target="70.00",
            indicator=self._indicators[2],  # 3
        )

        factories.PeriodicTarget(
            id=8,  # 11
            period="February 2018",
            target="500.00",
            indicator=self._indicators[12],  # 13
        )

        factories.PeriodicTarget(
            id=9,  # 12
            period="March 2018",
            target="500.00",
            indicator=self._indicators[12],  # 13
        )

        factories.PeriodicTarget(
            id=10,  # 13
            period="April 2018",
            target="1000.00",
            indicator=self._indicators[12],  # 13
        )

        factories.PeriodicTarget(
            id=11,  # 14
            period="May 2018",
            target="1000.00",
            indicator=self._indicators[12],  # 13
        )

        factories.PeriodicTarget(
            id=12,  # 15
            period="June 2018",
            target="1500.00",
            indicator=self._indicators[12],  # 13
        )

        factories.PeriodicTarget(
            id=13,  # 16
            period="July 2018",
            target="1500.00",
            indicator=self._indicators[12],  # 13
        )

        factories.PeriodicTarget(
            id=14,  # 17
            period="August 2018",
            target="1500.00",
            indicator=self._indicators[12],  # 13
        )

        factories.PeriodicTarget(
            id=15,  # 18
            period="August 2018",
            target="80.00",
            indicator=self._indicators[3],  # 4
        )

        factories.PeriodicTarget(
            id=16,  # 19
            period="February 2018",
            target="100.00",
            indicator=self._indicators[7],  # 8
        )

        factories.PeriodicTarget(
            id=17,  # 20
            period="March 2018",
            target="100.00",
            indicator=self._indicators[7],  # 8
        )

        factories.PeriodicTarget(
            id=18,  # 21
            period="April 2018",
            target="100.00",
            indicator=self._indicators[7],  # 8
        )

        factories.PeriodicTarget(
            id=19,  # 22
            period="May 2018",
            target="100.00",
            indicator=self._indicators[7],  # 8
        )

        factories.PeriodicTarget(
            id=20,  # 23
            period="June 2018",
            target="100.00",
            indicator=self._indicators[7],  # 8
        )

        factories.PeriodicTarget(
            id=21,  # 24
            period="July 2018",
            target="50.00",
            indicator=self._indicators[7],  # 8
        )

        factories.PeriodicTarget(
            id=22,  # 26
            period="August 2018",
            target="75.00",
            indicator=self._indicators[4],  # 5
        )

        factories.PeriodicTarget(
            id=23,  # 27
            period="February 2018",
            target="250.00",
            indicator=self._indicators[5],  # 6
        )

        factories.PeriodicTarget(
            id=24,  # 28
            period="March 2018",
            target="250.00",
            indicator=self._indicators[5],  # 6
        )

        factories.PeriodicTarget(
            id=25,  # 29
            period="April 2018",
            target="500.00",
            indicator=self._indicators[5],  # 6
        )

        factories.PeriodicTarget(
            id=26,  # 30
            period="May 2018",
            target="500.00",
            indicator=self._indicators[5],  # 6
        )

        factories.PeriodicTarget(
            id=27,  # 34
            period="August 2018",
            target="60.00",
            indicator=self._indicators[6],  # 7
        )

        factories.PeriodicTarget(
            id=28,  # 35
            period="February 2018",
            target="1.00",
            indicator=self._indicators[8],  # 9
        )

        factories.PeriodicTarget(
            id=29,  # 36
            period="March 2018",
            target="2.00",
            indicator=self._indicators[8],  # 9
        )

        factories.PeriodicTarget(
            id=30,  # 37
            period="April 2018",
            target="3.00",
            indicator=self._indicators[8],  # 9
        )

        factories.PeriodicTarget(
            id=31,  # 38
            period="May 2018",
            target="2.00",
            indicator=self._indicators[8],  # 9
        )

        factories.PeriodicTarget(
            id=32,  # 39
            period="June 2018",
            target="1.00",
            indicator=self._indicators[8],  # 9
        )

        factories.PeriodicTarget(
            id=33,  # 40
            period="August 2018",
            target="1.00",
            indicator=self._indicators[8],  # 9
        )

        factories.PeriodicTarget(
            id=34,  # 41
            period="August 2018",
            target="5.00",
            indicator=self._indicators[9],  # 10
        )

        factories.PeriodicTarget(
            id=35,  # 42
            period="July 2018",
            target="2500.00",
            indicator=self._indicators[10],  # 11
        )

        factories.PeriodicTarget(
            id=36,  # 43
            period="August 2018",
            target="2500.00",
            indicator=self._indicators[10],  # 11
        )

        factories.PeriodicTarget(
            id=37,  # 44
            period="July 2018",
            target="2500.00",
            indicator=self._indicators[11],  # 12
        )

        factories.PeriodicTarget(
            id=38,  # 45
            period="August 2018",
            target="2500.00",
            indicator=self._indicators[11],  # 12
        )

    def _create_collected_data(self):
        factories.CollectedData(
            id=1,
            periodic_target_id="1",  # 1
            achieved="500.00",
            indicator=self._indicators[1],  # 2
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[1]],  # 5
        )

        factories.CollectedData(
            id=2,
            periodic_target_id="2",  # 2
            achieved="500.00",
            indicator=self._indicators[1],  # 2
            workflowlevel1=self._workflowlevel1s[3], # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]]  # 6
        )

        factories.CollectedData(
            id=3,
            periodic_target_id="3",  # 3
            achieved="1000.00",
            indicator=self._indicators[1],  # 2
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[3]],  # 7
        )

        factories.CollectedData(
            id=4,
            periodic_target_id="5",  # 5
            achieved="1000.00",
            indicator=self._indicators[1],  # 2
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[4]],  # 8
        )

        factories.CollectedData(
            id=5,
            periodic_target_id="4",  # 4
            achieved="1000.00",
            indicator=self._indicators[1],  # 2
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[5]],  # 9
        )

        factories.CollectedData(
            id=6,
            periodic_target_id="6",  # 6
            achieved="1500.00",
            indicator=self._indicators[1],  # 2
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[5]],  # 9
        )

        factories.CollectedData(
            id=7,
            periodic_target_id="6",  # 6
            achieved="1500.00",
            indicator=self._indicators[1],  # 2
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[1]],  # 5
        )

        factories.CollectedData(
            id=8,
            periodic_target_id="8",  # 11
            achieved="500.00",
            indicator=self._indicators[12],  # 13
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[1]],  # 5
        )

        factories.CollectedData(
            id=9,
            periodic_target_id="9",  # 12
            achieved="500.00",
            indicator=self._indicators[12],  # 13
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=10,
            periodic_target_id="10",  # 13
            achieved="1000.00",
            indicator=self._indicators[12],  # 13
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[3]],  # 7
        )

        factories.CollectedData(
            id=11,
            periodic_target_id="11",  # 14
            achieved="1000.00",
            indicator=self._indicators[12],  # 13
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[4]],  # 8
        )

        factories.CollectedData(
            id=12,
            periodic_target_id="12",  # 15
            achieved="1500.00",
            indicator=self._indicators[12],  # 13
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[5]],  # 9
        )

        factories.CollectedData(
            id=13,
            periodic_target_id="13",  # 16
            achieved="1500.00",
            indicator=self._indicators[12],  # 13
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=14,
            periodic_target_id="14",  # 17
            achieved="500.00",
            indicator=self._indicators[12],  # 13
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[1]],  # 5
        )

        factories.CollectedData(
            id=15,
            periodic_target_id="7",  # 10
            achieved="65.00",
            indicator=self._indicators[2],  # 3
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=16,
            periodic_target_id="15",  # 18
            achieved="78.00",
            indicator=self._indicators[3],  # 4
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[1]],  # 5
        )

        factories.CollectedData(
            id=17,
            periodic_target_id="16",  # 19
            achieved="75.00",
            indicator=self._indicators[7],  # 8
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[1]],  # 5
        )

        factories.CollectedData(
            id=18,
            periodic_target_id="17",  # 20
            achieved="100.00",
            indicator=self._indicators[7],  # 8
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=19,
            periodic_target_id="18",  # 21
            achieved="100.00",
            indicator=self._indicators[7],  # 8
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[3]],  # 7
        )

        factories.CollectedData(
            id=20,
            periodic_target_id="19",  # 22
            achieved="90.00",
            indicator=self._indicators[7],  # 8
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[4]],  # 8
        )

        factories.CollectedData(
            id=21,
            periodic_target_id="20",  # 23
            achieved="125.00",
            indicator=self._indicators[7],  # 8
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[5]],  # 9
        )

        factories.CollectedData(
            id=22,
            periodic_target_id="21",  # 24
            achieved="50.00",
            indicator=self._indicators[7],  # 8
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=23,
            periodic_target_id="22",  # 26
            achieved="55.00",
            indicator=self._indicators[4],  # 5
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=24,
            periodic_target_id="34",  # 41
            achieved="4.50",
            indicator=self._indicators[9],  # 10
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[1], self._site_profiles[2], self._site_profiles[3], self._site_profiles[4], self._site_profiles[5]],  # [5, 6, 7, 8, 9]
        )

        factories.CollectedData(
            id=25,
            periodic_target_id="23",  # 27
            achieved="500.00",
            indicator=self._indicators[5],  # 6
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[1]],  # 5
        )

        factories.CollectedData(
            id=26,
            periodic_target_id="24",  # 28
            achieved="500.00",
            indicator=self._indicators[5],  # 6
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=27,
            periodic_target_id="25",  # 29
            achieved="1000.00",
            indicator=self._indicators[5],  # 6
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[3]],  # 7
        )

        factories.CollectedData(
            id=28,
            periodic_target_id="26",  # 30
            achieved="300.00",
            indicator=self._indicators[5],  # 6
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[4]],  # 8
        )

        factories.CollectedData(
            id=29,
            periodic_target_id="27",  # 34
            achieved="55.00",
            indicator=self._indicators[6],  # 7
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=30,
            periodic_target_id="28",  # 35
            achieved="1.00",
            indicator=self._indicators[8],  # 9
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[1]],  # 5
        )

        factories.CollectedData(
            id=31,
            periodic_target_id="29",  # 36
            achieved="2.00",
            indicator=self._indicators[8],  # 9
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=32,
            periodic_target_id="30",  # 37,
            achieved="3.00",
            indicator=self._indicators[8],  # 9
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[3]],  # 7
        )

        factories.CollectedData(
            id=33,
            periodic_target_id="31",  # 38
            achieved="2.00",
            indicator=self._indicators[8],  # 9
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[4]],  # 8
        )

        factories.CollectedData(
            id=34,
            periodic_target_id="32",  # 39
            achieved="1.00",
            indicator=self._indicators[8],  # 9
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=35,
            periodic_target_id="33",  # 40
            achieved="1.00",
            indicator=self._indicators[8],  # 9
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[1]],  # 5
        )

        factories.CollectedData(
            id=36,
            periodic_target_id="35",  # 42
            achieved="2500.00",
            indicator=self._indicators[10],  # 11
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=37,
            periodic_target_id="36",  # 43
            achieved="2000.00",
            indicator=self._indicators[10],  # 11
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=38,
            periodic_target_id="37",  # 44
            achieved="2500.00",
            indicator=self._indicators[11],  # 12
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[1]],  # 5
        )

        factories.CollectedData(
            id=39,
            periodic_target_id="38",  # 45
            achieved="2000.00",
            indicator=self._indicators[11],  # 12
            workflowlevel1=self._workflowlevel1s[3],  # 15
            created_by=self._tolauser_ninette.user,  # 11
            site=[self._site_profiles[2]],  # 6
        )

        factories.CollectedData(
            id=40,
            achieved="1500.00",
            indicator=self._indicators[13],
            workflowlevel1=self._workflowlevel1s[6],
            created_by=self._tolauser_ninette.user,
            site=[self._site_profiles[6]],
        )

        factories.CollectedData(
            id=41,
            achieved="23000.00",
            indicator=self._indicators[14],
            workflowlevel1=self._workflowlevel1s[6],
            created_by=self._tolauser_ninette.user,
        )

        factories.CollectedData(
            id=42,
            achieved="3700.00",
            indicator=self._indicators[15],
            workflowlevel1=self._workflowlevel1s[6],
            created_by=self._tolauser_ninette.user,
        )

        factories.CollectedData(
            id=43,
            achieved="125000.00",
            indicator=self._indicators[16],
            workflowlevel1=self._workflowlevel1s[6],
            created_by=self._tolauser_ninette.user,
        )

        factories.CollectedData(
            id=44,
            achieved="500.00",
            indicator=self._indicators[13],
            workflowlevel1=self._workflowlevel1s[6],
            created_by=self._tolauser_ninette.user,
            site=[self._site_profiles[6]],
        )

        factories.CollectedData(
            id=45,
            achieved="2300.00",
            indicator=self._indicators[13],
            workflowlevel1=self._workflowlevel1s[6],
            created_by=self._tolauser_ninette.user,
        )

        factories.CollectedData(
            id=46,
            achieved="700.00",
            indicator=self._indicators[13],
            workflowlevel1=self._workflowlevel1s[6],
            created_by=self._tolauser_ninette.user,
            site=[self._site_profiles[7]],
        )

    def _create_workflowlevel1_sectors(self):
        factories.WorkflowLevel1Sector(
            id=1,
            workflowlevel1=self._workflowlevel1s[3],  # 15
            sector=self._sectors[14],  # 143
            sub_sector=[self._sectors[37], self._sectors[38], self._sectors[39], self._sectors[40], self._sectors[41]],  # [166, 167, 168, 169, 170]
        )

        factories.WorkflowLevel1Sector(
            id=2,
            workflowlevel1=self._workflowlevel1s[3],  # 15
            sector=self._sectors[5],  # 134
            sub_sector=[self._sectors[13], self._sectors[83], self._sectors[84]],  # [142, 212, 213]
        )

        factories.WorkflowLevel1Sector(
            id=3,
            workflowlevel1=self._workflowlevel1s[3],  # 15
            sector=self._sectors[101],  # 230
            sub_sector=[self._sectors[10], self._sectors[102], self._sectors[103], self._sectors[104], self._sectors[105]],  # [139, 231, 232, 233, 234]
        )

        factories.WorkflowLevel1Sector(
            id=4,
            workflowlevel1=self._workflowlevel1s[1],  # 10
            sector=self._sectors[49],  # 178,
            sub_sector=[self._sectors[14]],  # [143]
        )

        factories.WorkflowLevel1Sector(
            id=5,
            workflowlevel1=self._workflowlevel1s[6],
            sector=self._sectors[31],
            sub_sector=[self._sectors[36], self._sectors[34], self._sectors[32], self._sectors[33], self._sectors[35]],
        )

        factories.WorkflowLevel1Sector(
            id=6,
            workflowlevel1=self._workflowlevel1s[6],
            sector=self._sectors[109],
            sub_sector=[self._sectors[84], self._sectors[98], self._sectors[31]],
        )

    def _create_workflowteams(self):
        factories.WorkflowTeam(
            id=1,  # 2
            workflow_user=self._tolauser_andrew,  # 9
            workflowlevel1=self._workflowlevel1s[1],  # 10
            role=self._groups[3],  # 3
        )

        factories.WorkflowTeam(
            id=2,  # 3
            workflow_user=self._tolauser_ninette,  # 11
            workflowlevel1=self._workflowlevel1s[2],  # 11
            role=self._groups[3],  # 3
        )

        factories.WorkflowTeam(
            id=3,  # 4
            workflow_user=self._tolauser_andrew,  # 9
            workflowlevel1=self._workflowlevel1s[2],  # 11
            role=self._groups[3],  # 3
        )

        factories.WorkflowTeam(
            id=4,  # 13
            workflow_user=self._tolauser_ninette,  # 11
            workflowlevel1=self._workflowlevel1s[1],  # 10
            role=self._groups[3],  # 3
        )

        factories.WorkflowTeam(
            id=5,  # 16
            workflow_user=self._tolauser_andrew,  # 9
            workflowlevel1=self._workflowlevel1s[3],  # 15
            role=self._groups[3],  # 3
        )

        factories.WorkflowTeam(
            id=6,  # 17
            workflow_user=self._tolauser_ninette,  # 11
            workflowlevel1=self._workflowlevel1s[3],  # 15
            role=self._groups[3],  # 3
        )

    def _reset_sql_sequences(self):
        """
        After adding to database all rows using hardcoded IDs, the primary key
        counter of each table is not autoupdated. This method resets all
        primary keys for all affected apps.
        """
        os.environ['DJANGO_COLORS'] = 'nocolor'

        for app in self.APPS:
            buf = StringIO()
            call_command('sqlsequencereset', app, stdout=buf)

            buf.seek(0)
            sql_commands = buf.getvalue().splitlines()

            sql_commands_clean = []
            for command in sql_commands:
                # As we are already inside a transaction thanks to the
                # transaction.atomic decorator, we don't need
                # the COMMIT and BEGIN statements. If there was some problem
                # we are automatically rolling back the transaction.
                if command not in ('COMMIT;', 'BEGIN;'):
                    sql_commands_clean.append(command)

            cursor = connection.cursor()
            cursor.execute("\n".join(sql_commands_clean))

    def _assign_workflowteam_current_users(self):
        role = Group.objects.get(name=ROLE_VIEW_ONLY)
        wflvl1_0 = WorkflowLevel1.objects.get(
            id=DEFAULT_WORKFLOW_LEVEL_1S[0][0])
        wflvl1_1 = WorkflowLevel1.objects.get(
            id=DEFAULT_WORKFLOW_LEVEL_1S[1][0])
        tola_user_ids = TolaUser.objects.values_list('id', flat=True).all()

        wfteams_0 = [
            WorkflowTeam(workflow_user_id=user_id, role=role,
                         workflowlevel1=wflvl1_0)
            for user_id in tola_user_ids
        ]
        wfteams_1 = [
            WorkflowTeam(workflow_user_id=user_id, role=role,
                         workflowlevel1=wflvl1_1)
            for user_id in tola_user_ids
        ]
        WorkflowTeam.objects.bulk_create(wfteams_0)
        WorkflowTeam.objects.bulk_create(wfteams_1)

    def add_arguments(self, parser):
        parser.add_argument('--demo', action='store_true',
                            help='Loads extra demo data')
        parser.add_argument('--restore', action='store_true',
                            help=('Restores back demo data deleting old '
                                  'previous one (except users)'))

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEFAULT_ORG:
            msg = ('A DEFAULT_ORG needs to be set up in the configuration to '
                   'run the script.')
            logger.error(msg)
            sys.stderr.write("{}\n".format(msg))
            raise ImproperlyConfigured(msg)

        if options['restore']:
            self._clear_database()

        self._create_organization()
        self._create_groups()
        self._create_countries()
        self._create_sectors()
        self._create_indicator_types()

        if options['demo'] or options['restore']:
            try:
                self._create_users()
                self._create_site_profiles()
                self._create_stakeholders()
                self._create_milestones()
                self._create_workflow_1s()
                self._create_workflow_2s()
                self._create_levels()
                self._create_frequencies()
                self._create_indicators()
                self._create_periodic_targets()
                self._create_collected_data()
                self._create_workflowlevel1_sectors()
                self._create_workflowteams()
            except IntegrityError:
                msg = ("Error: the data could not be populated in the "
                       "database. Check that the affected database tables are "
                       "empty.")
                logger.error(msg)
                sys.stderr.write("{}\n".format(msg))
                raise

        self._reset_sql_sequences()

        if options['restore']:
            self._assign_workflowteam_current_users()
