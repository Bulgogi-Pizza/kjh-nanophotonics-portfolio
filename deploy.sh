#!/bin/bash
set -e

echo "### STARTING FRONTEND & BACKEND DEPLOYMENT"

# 1. 새 버전의 프론트엔드 및 백엔드 이미지 빌드
docker compose build frontend backend

# 2. 프론트엔드 컨테이너 업데이트 (단순 재시작으로 충분)
echo "### UPDATING FRONTEND..."
docker compose up -d --no-deps --force-recreate --no-build frontend

# 3. 백엔드 컨테이너 롤링 업데이트 실행
echo "### STARTING ROLLING UPDATE FOR BACKEND..."
docker compose up -d --remove-orphans --no-build backend

# 4. Nginx가 새로운 백엔드 컨테이너들을 인식하도록 upstream.conf 업데이트 및 리로드
echo "### SYNCING NGINX with new backend containers..."
sleep 5

RUNNING_CONTAINER_NAMES=$(docker inspect --format='{{.Name}}' $(docker compose ps -q backend) | sed 's/^\///')
BACKEND_UPSTREAM=$(echo "$RUNNING_CONTAINER_NAMES" | awk '{print "server " $1 ":8000;"}')
echo "upstream reflex_backend { ${BACKEND_UPSTREAM} }" > ./nginx/conf.d/upstream.conf

docker compose exec frontend nginx -s reload

echo "### DEPLOYMENT COMPLETED SUCCESSFULLY"