#!/bin/bash

# EXPORTS ENV VARS DEV
MACHINE_IP=$(docker-machine ip)
echo "Docker Machine: $MACHINE_IP"
export ENV=development
export DB_HOST=$MACHINE_IP
docker-compose up -d
docker container restart ubiwhere-api-development