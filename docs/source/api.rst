API
=========

Endpoints
---------
 * "users": "http://activity.toladata.io/api/users/",
 * "programs": "http://activity.toladata.io/api/programs/",
 * "sector": "http://activity.toladata.io/api/sector/",
 * "projecttype": "http://activity.toladata.io/api/projecttype/",
 * "office": "http://activity.toladata.io/api/office/",
 * "siteprofile": "http://activity.toladata.io/api/siteprofile/",
 * "country": "http://activity.toladata.io/api/country/",
 * "initiations": "http://activity.toladata.io/api/projectagreements/",
 * "tracking": "http://activity.toladata.io/api/tracking/",
 * "indicator": "http://activity.toladata.io/api/indicator/",
 * "reportingfrequency": "http://activity.toladata.io/api/reportingfrequency/",
 * "tolauser": "http://activity.toladata.io/api/tolauser/",
 * "indicatortype": "http://activity.toladata.io/api/indicatortype/",
 * "objective": "http://activity.toladata.io/api/objective/",
 * "disaggregationtype": "http://activity.toladata.io/api/disaggregationtype/",
 * "level": "http://activity.toladata.io/api/level/",
 * "externalservice": "http://activity.toladata.io/api/externalservice/",
 * "externalservicerecord": "http://activity.toladata.io/api/externalservicerecord/",
 * "strategicobjective": "http://activity.toladata.io/api/strategicobjective/",
 * "stakeholder": "http://activity.toladata.io/api/stakeholder/",
 * "stakeholdertype": "http://activity.toladata.io/api/stakeholdertype/",
 * "capacity": "http://activity.toladata.io/api/capacity/",
 * "evaluate": "http://activity.toladata.io/api/evaluate/",
 * "profiletype": "http://activity.toladata.io/api/profiletype/",
 * "province": "http://activity.toladata.io/api/province/",
 * "district": "http://activity.toladata.io/api/district/",
 * "adminlevelthree": "http://activity.toladata.io/api/adminlevelthree/",
 * "village": "http://activity.toladata.io/api/village/",
 * "contact": "http://activity.toladata.io/api/contact/",
 * "documentation": "http://activity.toladata.io/api/documentation/",
 * "collecteddata": "http://activity.toladata.io/api/collecteddata/",
 * "tolatable": "http://activity.toladata.io/api/tolatable/",
 * "disaggregationvalue": "http://activity.toladata.io/api/disaggregationvalue/",
 * "projectagreements": "http://activity.toladata.io/api/projectagreements/",
 * "loggedusers": "http://activity.toladata.io/api/loggedusers/",
 * "checklist": "http://activity.toladata.io/api/checklist/",
 * "organization": "http://activity.toladata.io/api/organization/",


Example
-------
::
    curl -H "Authorization: Token adkai39a9sdfj239m0afi2" https://activity.toladata.io/api/programs/{{id}}/`

GET /api/silo/

HTTP 200 OK
Allow: GET, POST, OPTIONS
Content-Type: application/json
Vary: Accept

::
    {
        "owner": {
            "url": "http://tables.toladata.io/api/users/2/",
            "password": "!asdfasdffd",
            "last_login": "2017-01-13T17:00:53Z",
            "is_superuser": false,
            "username": "jtest",
            "first_name": "Joe",
            "last_name": "Test",
            "email": "joe@test.com",
            "is_staff": false,
            "is_active": true,
            "date_joined": "2015-10-08T00:50:29Z",
            "groups": [],
            "user_permissions": []
        },
        "name": "NS Security Incident",
        "reads": [
            {
                "url": "http://tables.toladata.io/api/read/10/",
                "read_name": "Security Incident",
                "description": "",
                "read_url": "https://api.ona.io/api/v1/data/132211",
                "resource_id": null,
                "gsheet_id": null,
                "username": null,
                "password": null,
                "token": null,
                "file_data": null,
                "autopull_frequency": "daily",
                "autopush_frequency": null,
                "create_date": "2016-07-02T19:48:49Z",
                "edit_date": "2016-08-24T17:54:52Z",
                "owner": "http://tables.toladata.io/api/users/2/",
                "type": "http://tables.toladata.io/api/readtype/1/"
            },
            {
                "url": "http://tables.toladata.io/api/read/79/",
                "read_name": "NS Security Incident",
                "description": "Google Spreadsheet Export",
                "read_url": "https://docs.google.com/a/mercycorps.org/spreadsheets/d/1x7n0JViOqQB90W-G38QR5D2lHfJQWyZpkOUZfypWY0Y/",
                "resource_id": "1x7n0JViOqQB90W-G38QR5D2lHfJQWyZpkOUZfypWY0Y",
                "gsheet_id": null,
                "username": null,
                "password": null,
                "token": null,
                "file_data": null,
                "autopull_frequency": null,
                "autopush_frequency": null,
                "create_date": "2016-10-10T08:12:26Z",
                "edit_date": "2016-10-10T08:12:26Z",
                "owner": "http://tables.toladata.io/api/users/2/",
                "type": "http://tables.toladata.io/api/readtype/3/"
            }
        ],
        "description": null,
        "create_date": null,
        "id": 12,
        "data": "http://tables.toladata.io/api/silo/12/data/",
        "shared": [],
        "tags": [],
        "public": false
    },
