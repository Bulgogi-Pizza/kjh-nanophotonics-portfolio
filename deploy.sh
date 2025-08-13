#!/bin/bash

set -e

RUNNING_CONTAINER=$(docker ps --filter "name=app_" --format "{{.Names}}")

if [ "$RUNNING_CONTAINER" == "app_blue" ]; then
  CURRENT_COLOR="blue"
  NEXT_COLOR="green"
else
  CURRENT_COLOR="green"
  NEXT_COLOR="blue"
fi

echo "### CURRENTLY RUNNING: $CURRENT_COLOR"
echo "### STARTING DEPLOYMENT FOR: $NEXT_COLOR"

echo "### PREPARING NGINX for $NEXT_COLOR"
UPSTREAM_CONFIG="set \$upstream app_${NEXT_COLOR}:3000"
echo "$UPSTREAM_CONFIG" > ./nginx/conf.d/upstream.conf

echo "### BUILDING AND STARTING app_${NEXT_COLOR}..."
docker compose up --build -d app_${NEXT_COLOR} nginx certbot

echo "### WAITING FOR app_${NEXT_COLOR} to be healthy..."
sleep 15


if [ ! -z "$RUNNING_CONTAINER" ]; then
    echo "### STOPPING old container: $RUNNING_CONTAINER"
    docker compose stop $RUNNING_CONTAINER
    docker compose rm -f $RUNNING_CONTAINER
else
    echo "### NO old container to stop."
fi

echo "### DEPLOYMENT COMPLETED: $NEXT_COLOR is now live."
