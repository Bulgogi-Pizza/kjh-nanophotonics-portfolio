# ─────────────────────────────────────────────────────────────
# Stage 1) Python builder: Reflex export로 정적 산출물 생성
# ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS reflex-builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /src

# bun 설치 시 필요한 unzip 등 유틸
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl unzip ca-certificates build-essential git \
 && rm -rf /var/lib/apt/lists/*

# 의존성 + reflex
COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt reflex

# (빌드 시 DB 접근 안 하도록) 최소한의 DB_URL
ENV DB_URL=sqlite://

# 앱 복사 & export
COPY . /src
RUN reflex export

# Reflex 버전에 따라 산출물 위치가 다를 수 있어 대비:
# 1) /src/.web/out 디렉터리가 있으면 그대로 사용
# 2) frontend.zip 이면 풀어 사용
RUN set -eux; \
  if [ -d "/src/.web/out" ]; then \
    cp -r /src/.web/out /src/_export_out; \
  elif [ -f "/src/.web/frontend.zip" ]; then \
    mkdir -p /src/_export_out && unzip -q /src/.web/frontend.zip -d /src/_export_out; \
  elif [ -f "/src/.web/frontend/frontend.zip" ]; then \
    mkdir -p /src/_export_out && unzip -q /src/.web/frontend/frontend.zip -d /src/_export_out; \
  else \
    echo "ERROR: Frontend export not found"; \
    find /src/.web -maxdepth 3 -ls; \
    exit 1; \
  fi

# ─────────────────────────────────────────────────────────────
# Stage 2) Runtime: 정적 산출물만 초경량 서버로 서빙(3000)
# ─────────────────────────────────────────────────────────────
FROM node:20-slim AS web-runtime
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1
WORKDIR /web

COPY --from=reflex-builder /src/_export_out /web/out

# 정적 서버
RUN npm i -g serve@14

USER node
EXPOSE 3000
CMD ["serve", "-s", "out", "-l", "3000"]