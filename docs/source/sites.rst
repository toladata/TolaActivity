Siteprofile
***********

Endpoint
---------
 * "siteprofile": "http://dev-v2.tolaactivity.app.tola.io/api/siteprofile/"


This endpoint provides access to submitted siteprofiles in JSON format.



GET JSON List of all Siteprofiles
---------------------------------

Lists the siteprofile endpoints accessible to requesting user

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/siteprofile/
  </pre>

Example
^^^^^^^^
::

    curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/siteprofile/


Response
^^^^^^^^^
::

    [  {
        "url": "http://dev-v2.tolaactivity.app.tola.io/api/siteprofile/1/",
        "id": 1,
        "site_uuid": "d34f89b4-914b-47d9-942a-90c66aec7333",
        "name": "Cash distribution center - Helmand",
        "contact_leader": "",
        "date_of_firstcontact": null,
        "contact_number": "",
        "num_members": "",
        "info_source": null,
        "total_num_households": null,
        "avg_household_size": "0.00000000000000",
        "total_population": null,
        "total_male": null,
        "total_female": null,
        "total_land": null,
        "total_agricultural_land": null,
        "total_rainfed_land": null,
        "total_horticultural_land": null,
        "total_literate_peoples": null,
        "literate_males": null,
        "literate_females": null,
        "literacy_rate": null,
        "populations_owning_land": null,
        "avg_landholding_size": "0.00000000000000",
        "households_owning_livestock": null,
        "animal_type": null,
        "latitude": "9.0167000000000000",
        "longitude": "38.7500000000000000",
        "status": false,
        "create_date": "2017-10-24T16:21:34.275568Z",
        "edit_date": "2017-10-24T16:21:34.275575Z",
        "type": null,
        "office": null,
        "classify_land": null,
        "country": "http://dev-v2.tolaactivity.app.tola.io/api/country/5/",
        "province": "http://demo.tolaactivity.app.tola.io/api/adminboundaryone/1/",
        "district": "http://demo.tolaactivity.app.tola.io/api/adminboundarytwo/1/",
        "admin_level_three": "http://demo.tolaactivity.app.tola.io/api/adminboundarythree/1/",
        "village": "http://demo.tolaactivity.app.tola.io/api/adminboundaryfour/1/",
        "organization": "http://dev-v2.tolaactivity.app.tola.io/api/organization/3/",
        "owner": "http://demo.tolaactivity.app.tola.io/api/users/35/",
        "approval": []
      },
      ...
    ]

GET JSON List of siteprofile endpoints using limit operators
------------------------------------------------------------

Lists the siteprofile endpoints accesible to the requesting user based on 'start'
and/or 'limit' query parameters. Use the start parameter to skip a number
of records and the limit parameter to limit the number of records returned.

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/siteprofile/</code>?<code>start</code>=<code>start_value</code>
  </pre>

::

    curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/siteprofile/?start=5
    

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/siteprofile/</code><code>limit</code>=<code>limit_value</code>
  </pre>

::

	curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/siteprofile/?limit=2

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/siteprofile/<code>{pk}</code>?<code>start</code>=<code>start_value</code>&</code><code>limit</code>=<code>limit_value</code>
  </pre>

::

	 curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/siteprofile/?start=3&limit=4





GET JSON List of siteprofile end points filter by country
----------------------------------------------------------

Lists the siteprofile endpoints accessible to requesting user, for the specified
``country`` as a query parameter.

.. raw:: html


  <pre class="prettyprint">
  <b>GET</b> /api/siteprofile/?<code>country_country</code>=<code>country</code>
  </pre>

Example
^^^^^^^^^
::

       curl -H "Authorization: Token xxxxxxxxxxxx" http://dev-v2.tolaactivity.app.tola.io/api/siteprofile/?country_country=Afghanistan


Retrieve a specific Siteprofile
-------------------------------
Provides a list of json submitted data for a specific siteprofile.

.. raw:: html

  <pre class="prettyprint">
  <b>GET</b> /api/siteprofile/<code>{id}</code></pre>

Example
^^^^^^^^^
::

      curl -H "Authorization: Token xxxxxxxxxxxx"http://dev-v2.tolaactivity.app.tola.io/api/siteprofile/1

Response
^^^^^^^^^
::

  {
    "url": "http://dev-v2.tolaactivity.app.tola.io/api/siteprofile/1/",
    "id": 1,
    "site_uuid": "67a57504-1f62-45fd-88de-c10dce51a0e7",
    "name": "Cash distribution center - Kandahar",
    "contact_leader": null,
    "date_of_firstcontact": null,
    "contact_number": null,
    "num_members": null,
    "info_source": null,
    "total_num_households": null,
    "avg_household_size": "0.00000000000000",
    "total_population": null,
    "total_male": null,
    "total_female": null,
    "total_land": null,
    "total_agricultural_land": null,
    "total_rainfed_land": null,
    "total_horticultural_land": null,
    "total_literate_peoples": null,
    "literate_males": null,
    "literate_females": null,
    "literacy_rate": null,
    "populations_owning_land": null,
    "avg_landholding_size": "0.00000000000000",
    "households_owning_livestock": null,
    "animal_type": null,
    "latitude": "31.6289000000000000",
    "longitude": "65.7372000000000000",
    "status": true,
    "create_date": "2017-10-12T15:59:37Z",
    "edit_date": "2017-10-12T15:59:37Z",
    "type": null,
    "office": null,
    "classify_land": null,
    "country": "http://dev-v2.tolaactivity.app.tola.io/api/country/1/",
    "province": null,
    "district": null,
    "admin_level_three": null,
    "village": null,
    "organization": "http://dev-v2.tolaactivity.app.tola.io/api/organization/1/",
    "owner": null,
    "approval": []
  }

Paginate data of a specific form
----------------------------------
Returns a list of json submitted data for a specific form using page number and the number of items per page. Use the ``page`` parameter to specify page number and ``page_size`` parameter is used to set the custom page size.

Example
^^^^^^^^
::

      curl -H "Authorization: Token xxxxxxxxxxxx" dev-v2.tolaactivity.app.tola.io/api/siteprofile/20.json?page=1&page_size=4
