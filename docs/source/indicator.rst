Indicator
**********

Endpoint
--------
 * “indicator”: “http://dev-v2.tolaactivity.app.tola.io/api/indicator/”,


This endpoint provides access to submitted indicators in JSON format.



GET JSON List of all Indicators
--------------------------------

Lists the indicator endpoints accessible to requesting user

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/indicator/
  </pre>

Example
^^^^^^^
::

    curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/indicator/


Response
^^^^^^^^^
::

    [
      {
        "url": "http://dev-v2.tolaactivity.app.tola.io/api/indicator/1/",
        "id": 1,
        "indicator_uuid": "6279914f-c4a5-4673",
        "name": "Number of people that receive training (gullies, water and soil conservation and land restoration) on land restoration practices",
        "number": "2.0.3",
        "source": "Training sheets, monitoring visits, trainees action plan",
        "definition": "",
        "justification": "",
        "unit_of_measure": "people",
        "baseline": "",
        "lop_target": 2520,
        "rationale_for_target": "",
        "means_of_verification": "Training sheets, monitoring visits, trainees action plan",
        "data_collection_method": "training sheets",
        "data_points": "",
        "responsible_person": "Partner",
        "method_of_analysis": "",
        "information_use": "",
        "quality_assurance": "",
        "data_issues": "",
        "indicator_changes": "",
        "comments": "",
        "key_performance_indicator": false,
        "create_date": "2017-11-01T13:10:55.687997Z",
        "edit_date": "2017-11-01T13:10:55.688009Z",
        "notes": "",
        "level": "http://demo.tolaactivity.app.tola.io/api/level/10/",
        "data_collection_frequency": "http://demo.tolaactivity.app.tola.io/api/frequency/2/",
        "reporting_frequency": "http://demo.tolaactivity.app.tola.io/api/frequency/3/",
        "sector": "http://demo.tolaactivity.app.tola.io/api/sector/187/",
        "approved_by": null,
        "approval_submitted_by": null,
        "external_service_record": null,
        "owner": "http://dev-v2.tolaactivity.app.tola.io/api/users/62/",
        "indicator_type": [
             "http://dev-v2.tolaactivity.app.tola.io/api/indicatortype/7/"
          ],
        "objectives": [
            "http://dev-v2.tolaactivity.app.tola.io/api/objective/12/"
          ],
        "strategic_objectives": ["http://dev-v2.tolaactivity.app.tola.io/api/strategicobjective/2/"],
        "disaggregation": [],
        "workflowlevel1": [
          "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/1/"
        ],
        "sub_sector": [
          "http://dev-v2.tolaactivity.app.tola.io/api/sector/1/"
        ]
      },
      ...
    ]

GET JSON List of indicator endpoints using limit operators
----------------------------------------------------------

Lists the indicator endpoints accesible to the requesting user based on 'start'
and/or 'limit' query parameters. Use the start parameter to skip a number
of records and the limit parameter to limit the number of records returned.

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/indicator/</code>?<code>start</code>=<code>start_value</code>
  </pre>

::
    curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/indicator/?start=5
    


.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/indicator/</code><code>limit</code>=<code>limit_value</code>
  </pre>

::

	curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/indicator/?limit=2

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/indicator/<code>{pk}</code>?<code>start</code>=<code>start_value</code>&</code><code>limit</code>=<code>limit_value</code>
  </pre>

::

	 curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/indicator/?start=3&limit=4



GET JSON List of indicator endpoints filter by workflowlevel1 name
------------------------------------------------------------------

Lists the data endpoints accessible to requesting user, for the specified
``workflowlevel1 name`` as a query parameter.

.. raw:: html


  <pre class="prettyprint">
  <b>GET</b> /api/indicator/?<code>workflowlevel1_name</code>=<code>workflowlevel1_name</code>
  </pre>

Example
::

       curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/indicator/?workflowlevel1_name=Financial Assistance to Affected Communities


=======
^^^^^^^^
::

       curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/indicator/?workflowlevel1_name=Financial Assistance to Affected Communities


Retrieve a specific Indicator
------------------------------
Provides a list of json submitted data for a specific indicator.

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/indicator/<code>{id}</code></pre>

Example
^^^^^^^^^
::

      curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/indicator/3

Response
^^^^^^^^^
::
  {
     "url": "http://dev-v2.tolaactivity.app.tola.io/api/indicator/3/",
      "id": 3,
      "actuals": null,
      "indicator_uuid": "78374b06-d70f-4e0a",
      "name": "% of respondents who know 3 of 5 critical times to wash hands",
      "number": "3.1",
      "source": null,
      "definition": "",
      "justification": "",
      "unit_of_measure": null,
      "baseline": null,
      "lop_target": 90,
      "rationale_for_target": "",
      "means_of_verification": null,
      "data_collection_method": null,
      "data_points": "",
      "responsible_person": null,
      "method_of_analysis": null,
      "information_use": null,
      "quality_assurance": "",
      "data_issues": "",
      "indicator_changes": "",
      "comments": "",
      "key_performance_indicator": true,
      "create_date": "2017-10-13T13:57:33.150073Z",
      "edit_date": "2017-11-02T12:31:48.071533Z",
      "notes": "",
      "level": "http://dev-v2.tolaactivity.app.tola.io/api/level/13/",
      "data_collection_frequency": null,
      "reporting_frequency": null,
      "sector": "http://dev-v2.tolaactivity.app.tola.io/api/sector/109/",
      "approved_by": null,
      "approval_submitted_by": null,
      "external_service_record": null,
      "owner": null,
      "indicator_type": [],
      "objectives": [],
      "strategic_objectives": [],
      "disaggregation": [],
      "workflowlevel1": [
            "http://dev-v2.tolaactivity.app.tola.io/api/workflowlevel1/4/"
        ],
      "sub_sector": [
            "http://dev-v2.tolaactivity.app.tola.io/api/sector/196/"
        ]
  }

Paginate data of a specific formslack
-------------------------------------------
Returns a list of json submitted data for a specific form using page number and the number of items per page. Use the ``page`` parameter to specify page number and ``page_size`` parameter is used to set the custom page size.

Example
^^^^^^^^
::

      curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/indicator/20.json?page=1&page_size=4

