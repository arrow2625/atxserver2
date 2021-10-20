#!/bin/bash
docker-compose -p atx2 -f docker-compose.yml down
docker-compose -p atx2 -f docker-compose.yml build
docker-compose -p atx2 -f docker-compose.yml up -d
#docker-compose -p atx2 -f docker-compose.ym restart