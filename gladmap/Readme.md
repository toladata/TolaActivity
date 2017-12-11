# GLADMap

The GLADMap Django application for TolaActivity is based on the previous 
project ([GitHub Repo](https://github.com/toladata/GLADMap)). 
It has the goal to integrate Global Administrative Boundaries into Tola [GADM](http://www.gadm.org/).

**This project is currently in development and incomplete.**

Core of the GLADMap tool is a collection of scripts to download gadm files and convert them into GeoJSON to add them to
 our database.

* Step 1: run `scripts/download_boundaries.py` before doing so adjust the `list_country` list to contain the required 
companies.
* Step 2: run `scripts/convert_to_geojson.py` to convert the downloaded files and add them to the Django db

### Todo
Several steps are open to make GLADMap a fully usable tool for Tola.

* Re-evaluate data storage. PostGres JSON storage offers significant performance improvements compared to binary storage
in postgres or mysql but it still lacks effiency when doing geographic calculations 
(for example: find admin district for a certain point). Other systems like [PostGIS](http://postgis.net/) might offer
improvement.
* Improve APIs. A first implementation for some geo calculations (Find district fitting coordinates, find point, 
check coordinates) can be found in `geo.py`. This scripts need to be improved and extended for future applications as
the performance is currently not optimized. There is also an API to create new boundaries from a leaflet drawing 
which can be found in `views.py`. 
* Check frontend. A first frontend for visualizing boundaries and drawing new shapes can be found under 
`templates/leaflet test`