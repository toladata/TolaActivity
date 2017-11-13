Tola Data JSON Rest Api Endpoints and Authentication
====================================================

Endpoints
---------
    *"users": "http://demo.tolaactivity.app.tola.io/api/users/",
    *"groups": "http://demo.tolaactivity.app.tola.io/api/groups/",
    *"tolauser": "http://demo.tolaactivity.app.tola.io/api/tolauser/",
    *"tolauserfilter": "http://demo.tolaactivity.app.tola.io/api/tolauserfilter/",
    *"organization": "http://demo.tolaactivity.app.tola.io/api/organization/",
    *"country": "http://demo.tolaactivity.app.tola.io/api/country/",
    *"award": "http://demo.tolaactivity.app.tola.io/api/award/",
    *"workflowlevel1": "http://demo.tolaactivity.app.tola.io/api/workflowlevel1/",
    *"workflowlevel2": "http://demo.tolaactivity.app.tola.io/api/workflowlevel2/",
    *"workflowlevel2sort": "http://demo.tolaactivity.app.tola.io/api/workflowlevel2sort/",
    *"workflowmodules": "http://demo.tolaactivity.app.tola.io/api/workflowmodules/",
    *"workflowteam": "http://demo.tolaactivity.app.tola.io/api/workflowteam/",
    *"workflowlevel1sector": "http://demo.tolaactivity.app.tola.io/api/workflowlevel1sector/",
    *"approvaltype": "http://demo.tolaactivity.app.tola.io/api/approvaltype/",
    *"approvalworkflow": "http://demo.tolaactivity.app.tola.io/api/approvalworkflow/",
    *"milestone": "http://demo.tolaactivity.app.tola.io/api/milestone/",
    *"checklist": "http://demo.tolaactivity.app.tola.io/api/checklist/",
    *"sector": "http://demo.tolaactivity.app.tola.io/api/sector/",
    *"projecttype": "http://demo.tolaactivity.app.tola.io/api/projecttype/",
    *"office": "http://demo.tolaactivity.app.tola.io/api/office/",
    *"budget": "http://demo.tolaactivity.app.tola.io/api/budget/",
    *"fundcode": "http://demo.tolaactivity.app.tola.io/api/fundcode/",
    *"siteprofile": "http://demo.tolaactivity.app.tola.io/api/siteprofile/",
    *"adminboundaryone": "http://demo.tolaactivity.app.tola.io/api/adminboundaryone/",
    *"adminboundarytwo": "http://demo.tolaactivity.app.tola.io/api/adminboundarytwo/",
    *"adminboundarythree": "http://demo.tolaactivity.app.tola.io/api/adminboundarythree/",
    *"adminboundaryfour": "http://demo.tolaactivity.app.tola.io/api/adminboundaryfour/",
    *"frequency": "http://demo.tolaactivity.app.tola.io/api/frequency/",
    *"indicatortype": "http://demo.tolaactivity.app.tola.io/api/indicatortype/",
    *"indicator": "http://demo.tolaactivity.app.tola.io/api/indicator/",
    *"objective": "http://demo.tolaactivity.app.tola.io/api/objective/",
    *"strategicobjective": "http://demo.tolaactivity.app.tola.io/api/strategicobjective/",
    *"level": "http://demo.tolaactivity.app.tola.io/api/level/",
    *"externalservice": "http://demo.tolaactivity.app.tola.io/api/externalservice/",
    *"externalservicerecord": "http://demo.tolaactivity.app.tola.io/api/externalservicerecord/",
    *"stakeholder": "http://demo.tolaactivity.app.tola.io/api/stakeholder/",
    *"stakeholdertype": "http://demo.tolaactivity.app.tola.io/api/stakeholdertype/",
    *"profiletype": "http://demo.tolaactivity.app.tola.io/api/profiletype/",
    *"contact": "http://demo.tolaactivity.app.tola.io/api/contact/",
    *"documentation": "http://demo.tolaactivity.app.tola.io/api/documentation/",
    *"collecteddata": "http://demo.tolaactivity.app.tola.io/api/collecteddata/",
    *"periodictarget": "http://demo.tolaactivity.app.tola.io/api/periodictarget/",
    *"tolatable": "http://demo.tolaactivity.app.tola.io/api/tolatable/",
    *"disaggregationtype": "http://demo.tolaactivity.app.tola.io/api/disaggregationtype/",
    *"dissagregationlabel": "http://demo.tolaactivity.app.tola.io/api/dissagregationlabel/",
    *"disaggregationvalue": "http://demo.tolaactivity.app.tola.io/api/disaggregationvalue/",
    *"currency": "http://demo.tolaactivity.app.tola.io/api/currency/",
    *"beneficiary": "http://demo.tolaactivity.app.tola.io/api/beneficiary/",
    *"riskregister": "http://demo.tolaactivity.app.tola.io/api/riskregister/",
    *"issueregister": "http://demo.tolaactivity.app.tola.io/api/issueregister/",
    *"fieldtype": "http://demo.tolaactivity.app.tola.io/api/fieldtype/",
    *"customformfield": "http://demo.tolaactivity.app.tola.io/api/customformfield/",
    *"customform": "http://demo.tolaactivity.app.tola.io/api/customform/",
    *"codedfield": "http://demo.tolaactivity.app.tola.io/api/codedfield/",
    *"codedfieldvalues": "http://demo.tolaactivity.app.tola.io/api/codedfieldvalues/",
    *"landtype": "http://demo.tolaactivity.app.tola.io/api/landtype/",
    *"internationalization": "http://demo.tolaactivity.app.tola.io/api/internationalization/",
    *"portfolio": "http://demo.tolaactivity.app.tola.io/api/portfolio/",
    *"sectorrelated": "http://demo.tolaactivity.app.tola.io/api/sectorrelated/",
    *"pindicators": "http://demo.tolaactivity.app.tola.io/api/pindicators/",
    *"binary": "http://demo.tolaactivity.app.tola.io/api/binary/"


Status Codes
-------------
*200 - Successful[GET, PATCH, PUT]
*201 - Instance successfully created [POST]
*204 - Instance successfully deleted [DELETE]
*404 - Instance was not found

Request based Authentication
-----------------------------
Tola JSON API endpoints support API Token Authentication through the Authorization header.



Token Authentication
---------------------
Example using curl:

curl -X GET http://dev-v2.tolaactivity.app.tola.io/api/ -H "Authorization: Token TOKEN_KEY xxxxxxx"


Status Codes
-------------
* 200 - Successful[GET, PATCH, PUT]
* 201 - Instance successfully created [POST]
* 204 - Instance successfully deleted [DELETE]
* 404 - Instance was not found

Request based Authentication
-----------------------------
Tola JSON API endpoints support API Token Authentication through the Authorization header.



Token Authentication
--------------------


Example
^^^^^^^
::
    curl -H "Authorization: Token TOKEN_KEY xxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/

.. raw:: html

GET /api/workflowlevel1/

HTTP 200 OK
Allow: GET, POST, OPTIONS
Content-Type: application/json
Vary: Accept

Response
^^^^^^^^
::

    [
        {
        "url": "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/1/",
        "id": 124,
        "status": "green",
        "difference": null,
        "level1_uuid": "69825d8e-c2e8-4748-9ea5-20a3d89",
        "unique_id": "null",
        "name": "Building Resilience in Mali",
        "funding_status": "funded",
        "cost_center": "23",
        "description": "",
        "public_dashboard": false,
        "start_date": "2017-11-01T12:35:09.070032Z",
        "end_date": "2017-11-01T12:35:09.070032Z",
        "create_date": "2017-11-01T12:35:09.070032Z",
        "edit_date": "2017-11-01T12:35:09.070037Z",
        "sort": 0,
        "organization": "http://dev-v2.tolaactivity.app.tola.io/api/organization/17/",
        "portfolio": null,
        "fund_code": [],
        "award": ["http://demo.tolaactivity.app.tola.io/api/award/6/"],
        "sector": [
            "http://dev-v2.tolaactivity.app.tola.io/api/sector/177/"
        ],
        "sub_sector": [
            "http://dev-v2.tolaactivity.app.tola.io/api/sector/287/"

        ],
        "country": [
            "http://dev-v2.tolaactivity.app.tola.io/api/country/1/"
        ],
        "milestone": [
            "http://dev-v2.tolaactivity.app.tola.io/api/milestone/13/"
        ],
        "user_access": [
            "http://dev-v2.tolaactivity.app.tola.io/api/tolauser/57/"
        ]
        },

    ]
