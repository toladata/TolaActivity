#Search
###Configuration

###Updating the index
The search index automatically updates itself whenever an object is saved. In a freshly configured, clean environment 
there is no need to manually update the search index.

If the search index was corrupted or the database is build upon an import of old data the index has to be manually
 populated.

To do this first make sure that no index exists for the configured environment.

Check ElasticSearch that no index exists with the index prefix defined in ```$ELASTICSEARCH_INDEX_PREFIX```
Run ```GET /_cat/indices?v``` on the cluster to see existing indices. If the prefix is already in use check the 
configuration of other instances for conflicting settings and, if safe, 
delete the indices by running ```DELETE /prefix_*``` where prefix is the index prefix defined in the environment
variables.

Finally run 
```
python manage.py search-index _all
```
on the container to recreate the index.