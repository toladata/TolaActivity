Stakeholder
***********

Endpoint
---------
 * “stakeholder”: “http://dev-v2.tolaactivity.app.tola.io/api/stakeholder/”


This endpoint provides access to submitted stakeholders in JSON format.



GET JSON List of all Stakeholders
---------------------------------

Lists the stakeholder endpoints accessible to requesting user

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/stakeholder/
  </pre>

Example
^^^^^^^^
::

    curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/stakeholder/


Response
^^^^^^^^^
::

    [
      {
        "url": "http://dev-v2.tolaactivity.app.tola.io/api/stakeholder/1/",
        "id": 1,
        "stakeholder_uuid": "be328490-c1c9-472f-95e2-8e36dd8ed30c",
        "name": "Afghan Economic Development Services",
        "role": null,
        "contribution": null,
        "stakeholder_register": true,
        "create_date": "2017-10-13T08:00:58Z",
        "edit_date": "2017-10-13T12:01:45.744794Z",
        "type": "http://dev-v2.tolaactivity.app.tola.io/api/stakeholdertype/3/",
        "country": "http://dev-v2.tolaactivity.app.tola.io/api/country/1/",
        "organization": "http://dev-v2.tolaactivity.app.tola.io/api/organization/1/",
        "formal_relationship_document": null,
        "vetting_document": null,
        "owner": "http://demo.tolaactivity.app.tola.io/api/users/16/",
        "contact": [],
        "workflowlevel1": [
            "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/8/"
        ],
        "sectors": ["http://demo.tolaactivity.app.tola.io/api/sector/100/","http://demo.tolaactivity.app.tola.io/api/sector/109/"],
        "approval": []
      },
      ...
    ]

GET JSON List of stakeholder endpoints using limit operators
-------------------------------------------------------------

Lists the stakeholder endpoints accesible to the requesting user based on 'start'
and/or 'limit' query parameters. Use the start parameter to skip a number
of records and the limit parameter to limit the number of records returned.

.. raw:: html

    <pre class="prettyprint">
    <b>GET</b> /api/stakeholder/</code>?<code>start</code>=<code>start_value</code>
    </pre>

::

    curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/stakeholder/?start=5
    

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/stakeholder/</code><code>limit</code>=<code>limit_value</code>
  </pre>

::

	curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/stakeholder/?limit=2

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/stakeholder/<code>{pk}</code>?<code>start</code>=<code>start_value</code>&</code><code>limit</code>=<code>limit_value</code>
  </pre>

::

	 curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/stakeholder/?start=3&limit=4



GET JSON List of stakeholder endpoints filter by  workflowlevel1
-----------------------------------------------------------------

Lists the data endpoints accessible to requesting user, for the specified
``workflowlevel1 `` as a query parameter.

.. raw:: html


  <pre class="prettyprint">
  <b>GET</b> /api/stakeholder/?<code>workflowlevel1_name</code>=<code>workflowlevel1_name</code>
  </pre>

Example
^^^^^^^^^
::

       curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/stakeholder/?workflowlevel1_name=Financial Assistance to Affected Communities


GET JSON List of stakeholder end points filter by country
---------------------------------------------------------

Lists the stakeholder endpoints accessible to requesting user, for the specified
``country`` as a query parameter.

.. raw:: html


  <pre class="prettyprint">
  <b>GET</b> /api/stakeholder/?<code>country_country</code>=<code>ountry</code>
  </pre>

Example
^^^^^^^^^
::

       curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/stakeholder/?country_country=Afghanistan


Retrieve a specific stakeholder
------------------------------
Provides a list of json submitted data for a specific stakeholder.

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/stakeholder/<code>{id}</code></pre>

Example
^^^^^^^^^
::

      curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/stakeholder/2

Response
^^^^^^^^^
::

  {
    "url": "http://dev-v2.tolaactivity.app.tola.io/api/stakeholder/2",
    "id": 2,
    "stakeholder_uuid": "7c9b89ed-c23b-4980-884e-0b9bdc70324a",
    "name": "Afghanistan Research Institute",
    "role": null,
    "contribution": null,
    "stakeholder_register": true,
    "create_date": "2017-10-13T15:49:16.714196Z",
    "edit_date": "2017-10-13T15:49:16.714201Z",
    "type": "http://dev-v2.tolaactivity.app.tola.io/api/stakeholdertype/6/",
    "country": "http://dev-v2.tolaactivity.app.tola.io/api/country/1/",
    "organization": "http://dev-v2.tolaactivity.app.tola.io/api/organization/1/",
    "formal_relationship_document": null,
    "vetting_document": null,
    "owner": null,
    "contact": [],
    "workflowlevel1": [
            "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/8/"
        ],
    "sectors": [],
    "approval": []
  }

Paginate data of a specific form
-------------------------------------------
Returns a list of json submitted data for a specific form using page number and the number of items per page. Use the ``page`` parameter to specify page number and ``page_size`` parameter is used to set the custom page size.

Example
^^^^^^^^
::

      curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/stakeholder/20.json?page=1&page_size=4
