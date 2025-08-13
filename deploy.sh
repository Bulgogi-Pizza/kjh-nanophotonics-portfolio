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

docker compose build app_${NEXT_COLOR}
docker compose up -d app_${NEXT_COLOR}

echo "### WAITING FOR app_${NEXT_COLOR} to be health..."
sleep 10
# 임시로 10초 기다리는 방편, 추후에는 healthy API 호출하여 200 OK 응답 확인하기

echo "### SWITCHING NGINX to $NEXT_COLOR"
UPSTREAM_CONFIG="set \$upstream app_${NEXT_COLOR}:3000;"
echo "$UPSTREAM_CONFIG" | docker compose exec -T nginx sh -c 'cat > /etc/nginx/conf.d/upstream.conf'
docker compose exec nginx nginx -s reload

if [ ! -z "$RUNNING_CONTAINER" ]; then
    echo "### STOPPING old container: $RUNNING_CONTAINER"
    docker compose stop $RUNNING_CONTAINER
    docker compose rm -f $RUNNING_CONTAINER
else
    echo "### NO old container to stop."
fi

echo "### DEPLOYMENT COMPLETED: $NEXT_COLOR is now live."
