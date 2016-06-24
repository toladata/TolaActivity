#!/bin/bash

### It dockerizes automatically ###
cd /home/TolaActivity
git stash
git pull origin docker
#docker-compose up mysqldb
#sleep 5
docker-compose up

