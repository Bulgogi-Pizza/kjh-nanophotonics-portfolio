# ─────────────────────────────────────────────────────────────
# Stage 1) Python builder: Reflex가 Next 프로젝트(.web)를 생성
# ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS reflex-builder
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /src

# 시스템 빌드 도구 (일부 패키지 컴파일 대비; 용량 최소화를 위해 builder에만 설치)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git \
    && rm -rf /var/lib/apt/lists/*

# 의존성 설치 (reflex 포함)
COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt reflex

# 앱 소스 복사
COPY . /src

# Reflex가 Next 기반 정적/SSR 프로젝트를 .web 폴더에 생성
# --no-watch: CI/도커 빌드 환경에서 감시 비활성
# 환경에 따라 export 옵션이 다를 수 있으니, 필요 시 rxconfig.py에 맞춰 조정
RUN reflex export --no-watch

# ─────────────────────────────────────────────────────────────
# Stage 2) Node builder: .web 프로젝트를 Next 프로덕션 빌드
# ─────────────────────────────────────────────────────────────
FROM node:20-slim AS next-builder
WORKDIR /app

# Reflex가 생성한 .web을 복사
COPY --from=reflex-builder /src/.web /app

# Next 의존성 설치 및 빌드
# package-lock.json 이 생성되어 있으므로 npm ci 사용
RUN npm ci && npm run build

# ─────────────────────────────────────────────────────────────
# Stage 3) Runtime: Next 서버만 실행 (프런트엔드 전용)
# ─────────────────────────────────────────────────────────────
FROM node:20-slim AS web-runtime
ENV NODE_ENV=production
WORKDIR /web

# 런타임에 필요한 파일만 복사 (용량 최소화)
COPY --from=next-builder /app/.next /web/.next
COPY --from=next-builder /app/public /web/public
COPY --from=next-builder /app/package.json /web/package.json
# prod 의존성만 설치 (dev 제외)
RUN npm ci --omit=dev

EXPOSE 3000
# Next 기본 start 스크립트(-p 3000). Caddy/Nginx가 3000으로 프록시
CMD ["npm", "run", "start", "--", "-p", "3000"]