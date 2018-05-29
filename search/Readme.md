# Search

### Configuration

The following environment variables are required to run with search enabled.

* `ELASTICSEARCH_ENABLED` decides whether objects saved to the database will also be indexed in elasticsearch. The search will work without it but only with existing data. This can be used if a lot of data is imported that should not be immediately indexed in ES.
* `ELASTICSEARCH_URL` sets the URL for connecting with the ES cluster.
* `ELASTICSEARCH_INDEX_PREFIX` sets a prefix for each index. There will be many indices for our instances and its important that we don't mix them up. Each index in the background will be created and named automatically, but we can set the prefix to separate between the servers.

### Updating the index
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
