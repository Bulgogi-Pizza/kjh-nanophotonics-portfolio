#!/bin/bash
set -e

echo "### STARTING ROLLING UPDATE DEPLOYMENT"

# 1. 새 버전의 Docker 이미지 빌드
docker compose build app

# 2. 현재 실행 중인 app 컨테이너들의 ID 목록 가져오기
RUNNING_CONTAINERS=$(docker compose ps -q app)

# 3. 각 컨테이너를 순회하며 하나씩 업데이트
for CONTAINER_ID in $RUNNING_CONTAINERS; do
  CONTAINER_NAME=$(docker inspect --format='{{.Name}}' $CONTAINER_ID | sed 's/^\///')
  echo "### UPDATING CONTAINER: $CONTAINER_NAME"

  # 3-1. Nginx 로드밸런싱 그룹에서 현재 컨테이너를 'down'으로 표시하여 트래픽 제외
  echo "### EXCLUDING $CONTAINER_NAME from load balancer..."
  UPSTREAM_CONFIG=$(docker compose ps -q app | awk '{print "server " $1 ":3000 " ($1 == "'$CONTAINER_ID'" ? "down" : "") ";"}')
  echo "upstream reflex_app { ${UPSTREAM_CONFIG} }" > ./nginx/conf.d/upstream.conf
  docker compose exec nginx nginx -s reload
  sleep 5 # 트래픽이 완전히 빠질 때까지 잠시 대기

  # 3-2. 새 이미지로 컨테이너 재생성 (업데이트)
  echo "### RECREATING $CONTAINER_NAME with new image..."
  docker compose up -d --no-deps --force-recreate --no-build $CONTAINER_NAME

  # 3-3. 업데이트된 컨테이너가 healthy 상태가 될 때까지 헬스체크
  echo "### WAITING FOR $CONTAINER_NAME to be healthy..."
  timeout 120s bash -c \
    'until docker inspect --format="{{.State.Health.Status}}" '"$CONTAINER_NAME"' | grep -q "healthy"; do \
      sleep 5; \
    done'
  echo "### $CONTAINER_NAME is healthy!"

  # 3-4. Nginx 로드밸런싱 그룹에 컨테이너 다시 포함
  echo "### INCLUDING $CONTAINER_NAME back into load balancer..."
  UPSTREAM_CONFIG=$(docker compose ps -q app | awk '{print "server " $1 ":3000;"}')
  echo "upstream reflex_app { ${UPSTREAM_CONFIG} }" > ./nginx/conf.d/upstream.conf
  docker compose exec nginx nginx -s reload
done

echo "### ROLLING UPDATE DEPLOYMENT COMPLETED"