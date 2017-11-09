Workflowlevel1
**************

Endpoint
---------
 * "workflowlevel1": "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/"


This endpoint provides access to submitted workflowlevel1 in JSON format




GET JSON List of all Workflowlevel1s
------------------------------------

Lists the workflowlevel1 endpoints accessible to requesting user

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel1/
  </pre>

Example
^^^^^^^^
::

    curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/


Response
^^^^^^^^^
::

    [
      {
        "url": "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/1/",
        "id": 1,
        "status": "green",
        "budget": null,
        "actuals": null,
        "difference": 0,
        "level1_uuid": "69825d8e-c2e8-4748-9ea5-20a3d89df6be",
        "unique_id": null,
        "name": "Afforestation program in Ethiopia",
        "funding_status": "",
        "cost_center": "",
        "description": "",
        "public_dashboard": false,
        "start_date": null,
        "end_date": null,
        "create_date": "2017-11-08T05:16:30.205438Z",
        "edit_date": "2017-11-08T08:41:23.503795Z",
        "sort": 0,
        "organization": "http://dev-v2.tolaactivity.app.tola.io/api/organization/1/",
        "portfolio": null,
        "fund_code": [],
        "award": ["http://demo.tolaactivity.app.tola.io/api/award/2/"],
        "sector": [ "http://demo.tolaactivity.app.tola.io/api/sector/109/"],
        "sub_sector": ["http://demo.tolaactivity.app.tola.io/api/sector/100/",
            "http://demo.tolaactivity.app.tola.io/api/sector/198/"],
        "country": ["http://demo.tolaactivity.app.tola.io/api/country/2/"],
        "milestone": ["http://demo.tolaactivity.app.tola.io/api/milestone/2/"],
        "user_access": [
            "http://dev-v2.tolaactivity.app.tola.io/api/tolauser/28/"
        ]
      },
      ...
    ]

GET JSON List of workflowlevel1 end points using limit operators
-----------------------------------------------------------------

Lists the workflowlevel1 endpoints accesible to the requesting user based on 'start'
and/or 'limit' query parameters. Use the start parameter to skip a number
of records and the limit parameter to limit the number of records returned.

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel1/</code>?<code>start</code>=<code>start_value</code>
  </pre>

::

    curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/?start=5
    

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel1/</code><code>limit</code>=<code>limit_value</code>
  </pre>

::

	curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/?limit=2

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel1/<code>{pk}</code>?<code>start</code>=<code>start_value</code>&</code><code>limit</code>=<code>limit_value</code>
  </pre>

::

	 curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/?start=3&limit=4



GET JSON List of data end points filter by country
--------------------------------------------------

Lists the data endpoints accessible to requesting user, for the specified
``country`` as a query parameter.

.. raw:: html


  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel1/?<code>name</code>=<code>country</code>
  </pre>

Example
^^^^^^^^^
::

       curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/?name=Financial Assistance to Affected Communities


GET JSON List of data end points filter by country
--------------------------------------------------

Lists the workflowlevel1 endpoints accessible to requesting user, for the specified
``country`` as a query parameter.

.. raw:: html


  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel1/?<code>country_country</code>=<code>ountry</code>
  </pre>

Example
^^^^^^^^^
::

       curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/?country_country=Afghanistan


Retrieve a specific workflowlevel1
-----------------------------------
Provides a list of json submitted data for a specific workflowlevel1.

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel1/<code>{id}</code></pre>

Example
^^^^^^^^^
::

      curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/3

Response
^^^^^^^^^
::

  {
    "url": "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/3/",
    "id": 3,
    "status": "",
    "budget": 0.0,
    "actuals": 0.0,
    "difference": 0,
    "level1_uuid": "ecf9a83e-abec-4488-ab85-9cb5fea296d7",
    "unique_id": null,
    "name": "Building Resilience in Mali",
    "funding_status": "",
    "cost_center": "",
    "description": "",
    "public_dashboard": false,
    "start_date": "2017-11-01T11:00:00Z",
    "end_date": "2018-11-30T11:00:00Z",
    "create_date": "2017-11-08T13:29:09.729031Z",
    "edit_date": "2017-11-08T13:29:10.003933Z",
    "sort": 0,
    "organization": "http://dev-v2.tolaactivity.app.tola.io/api/organization/2/",
    "portfolio": null,
    "fund_code": [],
    "award": [],
    "sector": [],
    "sub_sector": [],
    "country": [],
    "milestone": [],
    "user_access": [
            "http://dev-v2.tolaactivity.app.tola.io/api/tolauser/34/"
        ]
  }




Paginate data of a specific form
----------------------------------
Returns a list of json submitted data for a specific form using page number and the number of items per page. Use the ``page`` parameter to specify page number and ``page_size`` parameter is used to set the custom page size.


Example
^^^^^^^^
::

      curl -H "Authorization: Token xxxxxxxxxxxx2"http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/1.json?page=1&page_size=4


Create a new workflowlevel1
----------------------------

.. raw:: html

  <pre class="prettyprint">
  <b>POST</b> /api/workflowlevel1/</pre>

Example
-------
::

        {
            'name': 'My workflowlevel1',
            'level1_uuid': '1111',
            'country':  ["http://activity.toladata.io/api/country/1/"]
        }

Response
--------

::

        {
        "url": "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/22/",
        "id": 22,
        "status": "",
        "budget": 0.0,
        "actuals": 0.0,
        "difference": 0,
        "level1_uuid": "1111",
        "unique_id": null,
        "name": "My workflowlevel1",
        "funding_status": "",
        "cost_center": null,
        "description": "",
        "public_dashboard": false,
        "start_date": "2018-01-01T11:00:00Z",
        "end_date": "2018-12-31T11:00:00Z",
        "create_date": "2017-10-30T11:17:10Z",
        "edit_date": "2017-11-07T13:38:13.093921Z",
        "sort": 0,
        "organization": "http://dev-v2.tolaactivity.app.tola.io/api/organization/1/",
        "portfolio": null,
        "fund_code": [],
        "award": [],
        "sector": [],
        "sub_sector": [],
        "country": [],
        "milestone": [],
        "user_access": []
    
    }



