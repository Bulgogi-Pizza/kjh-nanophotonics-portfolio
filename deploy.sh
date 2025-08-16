#!/bin/bash
set -e

echo "### STARTING EXPORT-BASED ROLLING DEPLOYMENT"

# 1. 새 버전의 Docker 이미지 빌드 (이 과정에서 reflex export 실행)
docker compose build app

# 2. 임시 컨테이너를 이용해 프론트엔드 빌드 결과물(frontend.zip)을 호스트로 복사
echo "### EXTRACTING FRONTEND FILES..."
BUILD_CONTAINER_ID=$(docker create kjh-nanophotonics-portfolio-app)
docker cp $BUILD_CONTAINER_ID:/app/frontend.zip .
docker rm $BUILD_CONTAINER_ID

# 3. 기존 frontend 폴더를 삭제하고, 새로운 빌드 결과물 압축 해제
rm -rf ./frontend
unzip -o frontend.zip -d ./frontend # -o 옵션: 묻지 않고 덮어쓰기
rm frontend.zip

# 4. Docker Compose로 롤링 업데이트 실행
# 이 명령어 하나로 Docker가 deploy:update_config 전략에 따라
# 하나씩 컨테이너를 헬스체크하며 자동으로 업데이트합니다.
echo "### STARTING ROLLING UPDATE FOR APP CONTAINERS..."
docker compose up -d --remove-orphans --no-build app

# 5. Nginx가 새로운 컨테이너들을 인식하도록 upstream.conf 업데이트 및 리로드
echo "### SYNCING NGINX..."
# Docker 네트워크 DNS가 업데이트될 시간을 잠시 기다립니다.
sleep 5

# 현재 실행 중인 모든 app 컨테이너의 이름을 가져옴
RUNNING_CONTAINER_NAMES=$(docker inspect --format='{{.Name}}' $(docker compose ps -q app) | sed 's/^\///')

# 백엔드 upstream 목록 생성 (8000번 포트)
BACKEND_UPSTREAM=$(echo "$RUNNING_CONTAINER_NAMES" | awk '{print "server " $1 ":8000;"}')
echo "upstream reflex_back { ${BACKEND_UPSTREAM} }" > ./nginx/conf.d/upstream.conf

# Nginx 설정 리로드
docker compose exec nginx nginx -s reload

echo "### DEPLOYMENT COMPLETED SUCCESSFULLY"