Authentication and Status Codes
****

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

curl -X GET http://dev-v2.tolaactivity.app.tola.io/api/ -H "Authorization: Token TOKEN_KEY" 