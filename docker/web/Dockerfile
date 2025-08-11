# ─────────────────────────────────────────────────────────────
# Stage 1) Reflex export
# ─────────────────────────────────────────────────────────────
FROM python:3.11-slim AS reflex-builder
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /src

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl unzip ca-certificates build-essential git \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt reflex

# 빌드시 DB 접속 회피
ENV DB_URL=sqlite://
COPY . /src

RUN reflex export

# 산출물 자동 탐지: out/ → *frontend*.zip → build/client
RUN set -eux; \
  echo "==== .web tree (depth 5) ===="; \
  find /src/.web -maxdepth 5 -print; \
  if [ -d "/src/.web/out" ]; then \
    echo "[export] found: .web/out"; \
    cp -r /src/.web/out /src/_site; \
  else \
    zipfile="$(find /src/.web -maxdepth 5 -type f -iname '*frontend*.zip' -print -quit || true)"; \
    if [ -n "$zipfile" ]; then \
      echo "[export] found zip: $zipfile"; \
      mkdir -p /src/_site && unzip -q "$zipfile" -d /src/_site; \
    elif [ -d "/src/.web/build/client" ]; then \
      echo "[export] found: .web/build/client (Remix build)"; \
      mkdir -p /src/_site && cp -r /src/.web/build/client/* /src/_site/; \
      # public 정적자산이 따로 있으면 합치기(덮어쓰지 않음)
      if [ -d "/src/.web/public" ]; then cp -rn /src/.web/public/* /src/_site/ || true; fi; \
    else \
      echo "[export] no static site found; falling back to app runtime"; \
      cp -r /src/.web /src/_app; \
    fi; \
  fi

# ─────────────────────────────────────────────────────────────
# Stage 2) Runtime (정적 or 앱 런타임)
# ─────────────────────────────────────────────────────────────
FROM node:20-slim AS web-runtime
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1
WORKDIR /web

# 정적 사이트/앱 둘 다 복사
COPY --from=reflex-builder /src/_site /web/site
COPY --from=reflex-builder /src/_app  /web/app

RUN npm i -g serve@14

# 앱 런타임 필요한 경우 의존성(있을 때만)
RUN set -eux; \
  if [ -f /web/app/package.json ]; then \
    cd /web/app; \
    (npm ci --omit=dev --no-audit --no-fund || npm install --omit=dev --no-audit --no-fund); \
  fi

USER node
EXPOSE 3000
CMD ["/bin/sh","-lc", "\
  if [ -d /web/site ] && [ -f /web/site/index.html ]; then \
    echo '[run] serve static /web/site'; exec serve -s /web/site -l 3000; \
  elif [ -f /web/app/package.json ]; then \
    echo '[run] start app runtime'; cd /web/app && exec npx --yes remix vite dev --port 3000 --host 0.0.0.0 || exec npx next start -p 3000; \
  else \
    echo 'No frontend artifacts found'; sleep infinity; \
  fi"]