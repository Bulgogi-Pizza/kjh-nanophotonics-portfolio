# ─────────────────────────────────────────────────────────────
# Stage 1) Python builder: Reflex가 Next(.web) 생성
# ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS reflex-builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /src

# bun 설치용 unzip (+ curl/ca-certificates), 빌드 도구
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl unzip ca-certificates build-essential git \
 && rm -rf /var/lib/apt/lists/*

# 의존성 설치
COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt reflex

# 빌드 전용 임시 DB_URL (import 시 에러 방지)
ENV DB_URL=sqlite://

# 앱 소스 복사 후 Reflex export (Next 기반 .web 생성)
COPY . /src
RUN reflex export

# ─────────────────────────────────────────────────────────────
# Stage 2) Node builder: .web을 Next 프로덕션 빌드
# ─────────────────────────────────────────────────────────────
FROM node:20-slim AS next-builder
WORKDIR /app

COPY --from=reflex-builder /src/.web /app

# package-lock.json 유무에 따라 ci/install
# 빌드 후 Export(out/)까지 만든다
RUN if [ -f package-lock.json ]; then \
      npm ci --no-audit --no-fund; \
    else \
      npm install --no-audit --no-fund; \
    fi \
 && (npm run build || npx next build) \
 && (npm run export || npx next export)

# ─────────────────────────────────────────────────────────────
# Stage 3) Runtime: Next 서버만 실행 (프런트엔드 전용)
# ─────────────────────────────────────────────────────────────
FROM node:20-slim AS web-runtime
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1
WORKDIR /web

COPY --from=next-builder /app/out /web/out

# 아주 가벼운 정적 서버 사용
RUN npm i -g serve@14

USER node
EXPOSE 3000
CMD ["serve", "-s", "out", "-l", "3000"]