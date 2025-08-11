# ─────────────────────────────────────────────────────────────
# Stage 1) Python builder: Reflex export로 산출물 생성
# ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS reflex-builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl unzip ca-certificates build-essential git \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt reflex

# 빌드 시 DB 접근 안 하도록 더미로
ENV DB_URL=sqlite://

COPY . /src

# Reflex export 실행
RUN reflex export

# 산출물 구조가 버전에 따라 다름 → out/ 또는 *frontend*.zip 자동 탐지
# 디버깅을 위해 목록도 찍어 둠
RUN set -eux; \
  echo "==== .web tree ===="; \
  find /src/.web -maxdepth 3 -type f -o -type d -print; \
  # 1) out 디렉터리
  if [ -d "/src/.web/out" ]; then \
    echo "Found /src/.web/out"; \
    cp -r /src/.web/out /src/_export_out; \
  else \
    # 2) frontend zip (이름이 앱명-frontend.zip 등일 수 있음)
    zipfile="$(find /src/.web -maxdepth 3 -type f -iname '*frontend*.zip' -print -quit || true)"; \
    if [ -n "$zipfile" ]; then \
      echo "Found frontend zip: $zipfile"; \
      mkdir -p /src/_frontend && unzip -q "$zipfile" -d /src/_frontend; \
      echo "==== unzipped frontend tree ===="; \
      find /src/_frontend -maxdepth 3 -type f -o -type d -print; \
    else \
      echo "ERROR: Could not find out/ or *frontend*.zip under .web"; \
      exit 1; \
    fi; \
  fi

# ─────────────────────────────────────────────────────────────
# Stage 2) Runtime: 정적(out) 또는 Next 런타임 중 자동 선택
# ─────────────────────────────────────────────────────────────
FROM node:20-slim AS web-runtime
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1
WORKDIR /web

# 두 경우 모두 복사 (있는 것만 존재함)
COPY --from=reflex-builder /src/_export_out /web/out
COPY --from=reflex-builder /src/_frontend   /web/app

# 정적 서빙용
RUN npm i -g serve@14

# Next 런타임 필요한 경우 의존성 설치 (package.json 있으면)
RUN set -eux; \
  if [ -f /web/app/package.json ]; then \
    cd /web/app; \
    # package-lock이 없을 수 있으므로 ci 실패 시 install fallback
    (npm ci --omit=dev --no-audit --no-fund || npm install --omit=dev --no-audit --no-fund); \
  fi

USER node
EXPOSE 3000

# 우선순위: 1) 정적 out → serve, 2) Next 앱 → next start
CMD ["/bin/sh", "-lc", "if [ -d /web/out ]; then exec serve -s out -l 3000; elif [ -f /web/app/package.json ]; then cd /web/app && exec npx next start -p 3000; else echo 'No frontend artifacts found (out/ or app/).'; sleep infinity; fi"]