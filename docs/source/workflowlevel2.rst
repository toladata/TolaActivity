Workflowlevel2
***************

Endpoint
---------
 * "workflowlevel2": "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel2/",


This endpoint provides access to submitted workflowlevel2 in JSON format.



GET JSON List of all Workflowlevel2s
------------------------------------

Lists the workflowlevel2 endpoints accessible to requesting user

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel2/
  </pre>

Example
^^^^^^^^
::

    curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel2/


Response
^^^^^^^^^
::

    [
      {
        "url": "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel2/1/",
        "id": 1,
        "level2_uuid": "82efae6b-4f52-422e-ba75-7ce4ec2c9733",
        "short": true,
        "parent_workflowlevel2": 94,
        "date_of_request": null,
        "name": "1.1 Determine the real problem to solve",
        "description": null,
        "short_name": null,
        "staff_responsible": null,
        "effect_or_impact": null,
        "expected_start_date": null,
        "expected_end_date": null,
        "total_estimated_budget": "0.00",
        "justification_background": null,
        "risks_assumptions": null,
        "description_of_government_involvement": null,
        "description_of_community_involvement": null,
        "actual_start_date": null,
        "actual_end_date": null,
        "actual_duration": null,
        "on_time": true,
        "no_explanation": null,
        "actual_cost": "0.00",
        "actual_cost_date": null,
        "budget_variance": null,
        "explanation_of_variance": null,
        "total_cost": "0.00",
        "agency_cost": "0.00",
        "community_handover": false,
        "capacity_built": null,
        "quality_assured": null,
        "issues_and_challenges": null,
        "lessons_learned": null,
        "sort": 0,
        "create_date": "2017-10-27T16:06:18.375806Z",
        "edit_date": "2017-10-27T16:06:59.092287Z",
        "status": "green",
        "progress": "open",
        "workflowlevel1": "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/16/",
        "milestone": "http://dev-v2.tolaactivity.app.tola.io/api/milestone/3/",
        "sector": "http://dev-v2.tolaactivity.app.tola.io/api/sector/2/",
        "office": null,
        "partners": null,
        "local_currency": null,
        "donor_currency": null,
        "owner": null,
        "sub_sector": ["http://dev-v2.tolaactivity.app.tola.io/api/sector/16/"],
        "site": ["http://dev-v2.tolaactivity.app.tola.io/api/siteprofile/6/"],
        "stakeholder": ["http://dev-v2.tolaactivity.app.tola.io/api/stakeholder/5/"],
        "approval": [],
        "indicators": ["http://dev-v2.tolaactivity.app.tola.io/api/indicator/16/"]
      },
      ...
    ]

GET JSON List of workflowlevel2 end points using limit operators
----------------------------------------------------------------

Lists the workflowlevel2 endpoints accesible to the requesting user based on 'start'
and/or 'limit' query parameters. Use the start parameter to skip a number
of records and the limit parameter to limit the number of records returned.

.. raw:: html

    <pre class="prettyprint">
    <b>GET</b> /api/workflowlevel2/</code>?<code>start</code>=<code>start_value</code>
    </pre>

::
    curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel2/?start=5
    

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel2/</code><code>limit</code>=<code>limit_value</code>
  </pre>

::

	curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel2/?limit=2

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel2/<code>{pk}</code>?<code>start</code>=<code>start_value</code>&</code><code>limit</code>=<code>limit_value</code>
  </pre>

::

	 curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel2/?start=3&limit=4



GET JSON List of data end points filter by workflowlevel1 name
---------------------------------------------------------------

Lists the data endpoints accessible to requesting user, for the specified
``workflowlevel1 name`` as a query parameter.

.. raw:: html


  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel2/?<code>workflowlevel1_name</code>=<code>workflowlevel1_name</code>
  </pre>

Example
^^^^^^^^^
::

       curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel2/?workflowlevel1_name=Financial Assistance to Affected Communities


GET JSON List of data end points filter by country
--------------------------------------------------

Lists the workflowlevel2 endpoints accessible to requesting user, for the specified
``country`` as a query parameter.

.. raw:: html


  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel2/?<code>country_country</code>=<code>country_country</code>
  </pre>

Example
^^^^^^^^^
::

       curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel2/?country_country=Afghanistan



Retrieve a specific workflowlevel2
----------------------------------
Provides a list of json submitted data for a specific workflowlevel2.

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/workflowlevel2/<code>{id}</code></pre>

Example
^^^^^^^^^
::

      curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel2/5/"

Response
^^^^^^^^^
::
  {
    "url": "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel2/5/",
    "id": 5,
    "level2_uuid": "c430da67-bd00-4842-ace4-676e5f77805f",
    "short": true,
    "parent_workflowlevel2": 32,
    "date_of_request": null,
    "name": "1. Needs Assessment",
    "description": null,
    "short_name": null,
    "staff_responsible": null,
    "effect_or_impact": null,
    "expected_start_date": "2018-01-15T11:00:00Z",
    "expected_end_date": "2018-01-31T11:00:00Z",
    "total_estimated_budget": "0.00",
    "justification_background": null,
    "risks_assumptions": null,
    "description_of_government_involvement": null,
    "description_of_community_involvement": null,
    "actual_start_date": null,
    "actual_end_date": null,
    "actual_duration": null,
    "on_time": true,
    "no_explanation": null,
    "actual_cost": "0.00",
    "actual_cost_date": null,
    "budget_variance": null,
    "explanation_of_variance": null,
    "total_cost": "0.00",
    "agency_cost": "0.00",
    "community_handover": false,
    "capacity_built": null,
    "quality_assured": null,
    "issues_and_challenges": null,
    "lessons_learned": null,
    "sort": 0,
    "create_date": "2017-10-26T11:28:47.003428Z",
    "edit_date": "2017-10-26T11:39:52.798341Z",
    "status": "green",
    "progress": "open",
    "workflowlevel1": "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/11/",
    "milestone": null,
    "sector": null,
    "office": null,
    "partners": null,
    "local_currency": null,
    "donor_currency": null,
    "owner": null,
    "sub_sector": [],
    "site": [],
    "stakeholder": [],
    "approval": [],
    "indicators": []
  }




Paginate data of a specific form
---------------------------------
Returns a list of json submitted data for a specific form using page number and the number of items per page. Use the ``page`` parameter to specify page number and ``page_size`` parameter is used to set the custom page size.


Example
^^^^^^^^
::

      curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel2/1.json?page=1&page_size=4


Create a new workflowlevel2
----------------------------

.. raw:: html

  <pre class="prettyprint">
  <b>POST</b> /api/workflowlevel2/</pre>

Example
-------
::

        {
            "name": "My workflowlevel2",
            "level2_uuid": "11111",
            "workflowlevel1":  "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/11/"
        }

Response
--------

::

      {
        "url": "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel2/33/",
        "id": 33,
        "level2_uuid": "11111",
        "short": true,
        "parent_workflowlevel2": 0,
        "date_of_request": null,
        "name": "My workflowlevel2",
        "description": null,
        "short_name": null,
        "staff_responsible": null,
        "effect_or_impact": null,
        "expected_start_date": "2018-01-15T11:00:00Z",
        "expected_end_date": "2018-01-31T11:00:00Z",
        "total_estimated_budget": "0.00",
        "justification_background": null,
        "risks_assumptions": null,
        "description_of_government_involvement": null,
        "description_of_community_involvement": null,
        "actual_start_date": null,
        "actual_end_date": null,
        "actual_duration": null,
        "on_time": true,
        "no_explanation": null,
        "actual_cost": "0.00",
        "actual_cost_date": null,
        "budget_variance": null,
        "explanation_of_variance": null,
        "total_cost": "0.00",
        "agency_cost": "0.00",
        "community_handover": false,
        "capacity_built": null,
        "quality_assured": null,
        "issues_and_challenges": null,
        "lessons_learned": null,
        "sort": 0,
        "create_date": "2017-10-26T11:28:47.003428Z",
        "edit_date": "2017-10-26T11:39:52.798341Z",
        "status": "green",
        "progress": "open",
        "workflowlevel1": "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/11/",
        "milestone": null,
        "sector": null,
        "office": null,
        "partners": null,
        "local_currency": null,
        "donor_currency": null,
        "owner": null,
        "sub_sector": [],
        "site": [],
        "stakeholder": [],
        "approval": [],
        "indicators": []
    }
