# ─────────────────────────────────────────────────────────────
# Stage 1) Python builder: Reflex가 Next(.web) 생성
# ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS reflex-builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /src

# bun 설치 중 압축 해제에 필요: unzip (+ curl/ca-certificates도 함께)
# 일부 파이썬 패키지 빌드를 대비해 build-essential, git 설치 (빌더에만)
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl unzip ca-certificates build-essential git \
 && rm -rf /var/lib/apt/lists/*

# 의존성 설치 (reflex가 requirements.txt에 없다면 함께 설치)
COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt reflex

ENV DB_URL=sqlite://

# 앱 소스 복사
COPY . /src

# Reflex가 Next 기반 정적/SSR 프로젝트를 .web에 생성
# (bun 설치는 reflex가 자동 수행; unzip 필수)
RUN reflex export

# ─────────────────────────────────────────────────────────────
# Stage 2) Node builder: .web을 Next 프로덕션 빌드
# ─────────────────────────────────────────────────────────────
FROM node:20-slim AS next-builder
WORKDIR /app

# Reflex가 생성한 .web 복사
COPY --from=reflex-builder /src/.web /app

# Next 의존성 설치 및 빌드
# export 산출물에는 package.json / package-lock.json이 포함됨
RUN npm ci && npm run build

# ─────────────────────────────────────────────────────────────
# Stage 3) Runtime: Next 서버만 실행 (프런트엔드 전용)
# ─────────────────────────────────────────────────────────────
FROM node:20-slim AS web-runtime
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1
WORKDIR /web

# 런타임에 필요한 산출물/메타만 복사
COPY --from=next-builder /app/.next /web/.next
COPY --from=next-builder /app/public /web/public
COPY --from=next-builder /app/package.json /web/package.json
COPY --from=next-builder /app/package-lock.json /web/package-lock.json

# prod 의존성만 설치 (dev 제외)
RUN npm ci --omit=dev

# 보안: 비루트 실행 (node 이미지에 기본 존재하는 계정)
RUN chown -R node:node /web
USER node

EXPOSE 3000
# Next 기본 start 스크립트(-p 3000). Caddy가 3000으로 프록시
CMD ["npm", "run", "start", "--", "-p", "3000"]