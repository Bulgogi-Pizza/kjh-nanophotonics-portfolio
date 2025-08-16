#!/bin/bash
set -e

echo "### STARTING ROLLING UPDATE USING DOCKER COMPOSE DEPLOY"

# 1. 새 버전의 Docker 이미지 빌드
docker compose build app

# 2. Docker Compose에 롤링 업데이트 명령
docker compose up -d --remove-orphans --no-build

# 3. 모든 업데이트가 완료된 후, 최종적으로 Nginx 설정 업데이트
echo "### ROLLING UPDATE FINISHED. SYNCING NGINX..."
sleep 10 # 컨테이너 이름이 완전히 안정화될 때까지 잠시 대기

# 현재 실행 중인 모든 app 컨테이너의 이름을 가져옴
RUNNING_CONTAINER_NAMES=$(docker inspect --format='{{.Name}}' $(docker compose ps -q app) | sed 's/^\///')

# 최종 upstream 목록 생성
UPSTREAM_FRONT_CONFIG=$(echo "$RUNNING_CONTAINER_NAMES" | awk '{print "server " $1 ":3000;"}')
UPSTREAM_BACK_CONFIG=$(echo "$RUNNING_CONTAINER_NAMES" | awk '{print "server " $1 ":8000;"}')

echo "upstream reflex_front { ${UPSTREAM_FRONT_CONFIG} }" > ./nginx/conf.d/upstream.conf
echo "upstream reflex_back { ${UPSTREAM_BACK_CONFIG} }" >> ./nginx/conf.d/upstream.conf

# Nginx 설정 리로드
docker compose exec nginx nginx -s reload

echo "### DEPLOYMENT COMPLETED SUCCESSFULLY"