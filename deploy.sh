#!/bin/bash
set -e

echo "### STARTING ROLLING UPDATE DEPLOYMENT"

# 1. 새 버전의 Docker 이미지 빌드
docker compose build app

# 2. 현재 실행 중인 app 컨테이너들의 실제 이름 목록 가져오기 (수정된 부분)
RUNNING_CONTAINER_IDS=$(docker compose ps -q app)
RUNNING_CONTAINER_NAMES=""
if [ -n "$RUNNING_CONTAINER_IDS" ]; then
    RUNNING_CONTAINER_NAMES=$(docker inspect --format='{{.Name}}' $RUNNING_CONTAINER_IDS | sed 's/^\///')
fi

# 3. 각 컨테이너를 순회하며 하나씩 업데이트
for CONTAINER_NAME in $RUNNING_CONTAINER_NAMES; do
  echo "### UPDATING CONTAINER: $CONTAINER_NAME"

  # 3-1. Nginx 로드밸런싱 그룹에서 현재 컨테이너를 'down'으로 표시하여 트래픽 제외
  echo "### EXCLUDING $CONTAINER_NAME from load balancer..."
  # 현재 실행중인 모든 app 컨테이너 이름을 다시 가져와서 upstream 목록 생성
  ALL_APP_NAMES=$(docker inspect --format='{{.Name}}' $(docker compose ps -q app) | sed 's/^\///')
  UPSTREAM_CONFIG=$(echo "$ALL_APP_NAMES" | awk '{print "server " $1 ":3000 " ($1 == "'$CONTAINER_NAME'" ? "down" : "") ";"}')
  echo "upstream reflex_app { ${UPSTREAM_CONFIG} }" > ./nginx/conf.d/upstream.conf
  docker compose exec nginx nginx -s reload
  sleep 5

  # 3-2. 새 이미지로 컨테이너 재생성 (업데이트)
  echo "### RECREATING $CONTAINER_NAME with new image..."
  docker compose up -d --force-recreate --no-deps --no-build $CONTAINER_NAME

  # 3-3. 업데이트된 컨테이너가 healthy 상태가 될 때까지 헬스체크
  echo "### WAITING FOR $CONTAINER_NAME to be healthy..."
  timeout 120s bash -c \
    'until docker inspect --format="{{.State.Health.Status}}" '"$CONTAINER_NAME"' | grep -q "healthy"; do \
      sleep 5; \
    done'
  echo "### $CONTAINER_NAME is healthy!"

  # 3-4. Nginx 로드밸런싱 그룹에 컨테이너 다시 포함
  echo "### INCLUDING $CONTAINER_NAME back into load balancer..."
  ALL_APP_NAMES=$(docker inspect --format='{{.Name}}' $(docker compose ps -q app) | sed 's/^\///')
  UPSTREAM_CONFIG=$(echo "$ALL_APP_NAMES" | awk '{print "server " $1 ":3000;"}')
  echo "upstream reflex_app { ${UPSTREAM_CONFIG} }" > ./nginx/conf.d/upstream.conf
  docker compose exec nginx nginx -s reload
done

# 최초 실행 시 (실행 중인 컨테이너가 없을 때) 2개의 컨테이너를 띄움
if [ -z "$RUNNING_CONTAINER_NAMES" ]; then
    echo "### NO RUNNING CONTAINERS FOUND. STARTING INITIAL DEPLOYMENT..."
    docker compose up -d --build --no-deps app

    # 헬스체크
    echo "### WAITING FOR INITIAL CONTAINERS to be healthy..."
    timeout 120s bash -c \
        'until [ $(docker compose ps -q app | xargs -r docker inspect --format="{{.State.Health.Status}}" | grep -c "healthy") -eq 2 ]; do \
            sleep 5; \
        done'
    echo "### INITIAL CONTAINERS are healthy!"

    # Nginx 설정
    ALL_APP_NAMES=$(docker inspect --format='{{.Name}}' $(docker compose ps -q app) | sed 's/^\///')
    UPSTREAM_CONFIG=$(echo "$ALL_APP_NAMES" | awk '{print "server " $1 ":3000;"}')
    echo "upstream reflex_app { ${UPSTREAM_CONFIG} }" > ./nginx/conf.d/upstream.conf
    docker compose exec nginx nginx -s reload
fi


echo "### ROLLING UPDATE DEPLOYMENT COMPLETED"