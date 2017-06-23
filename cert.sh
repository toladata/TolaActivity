#!bin/bash

service nginx stop
certbot certonly --standalone  --email dborchers001@gmail.com -d activity-dev.toladata.io
service nginx start
