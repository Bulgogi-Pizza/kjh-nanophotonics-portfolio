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

# Reflex가 생성한 .web 복사
COPY --from=reflex-builder /src/.web /app

# 1) package.json에 build/start 스크립트가 없으면 주입
# 2) Next/React를 호환 가능한 버전으로 고정 (Next 14.x + React 18.x)
# 3) lock 파일이 있으면 npm ci, 없으면 npm install
# 4) 빌드 실행
RUN node -e "const fs=require('fs');const p=JSON.parse(fs.readFileSync('package.json','utf8'));p.scripts=p.scripts||{};if(!p.scripts.build)p.scripts.build='next build';if(!p.scripts.start)p.scripts.start='next start -p 3000';fs.writeFileSync('package.json',JSON.stringify(p,null,2));" \
 && npm pkg set "dependencies.next=14.2.10" "dependencies.react=18.3.1" "dependencies.react-dom=18.3.1" \
 && if [ -f package-lock.json ]; then npm ci --no-audit --no-fund; else npm install --no-audit --no-fund; fi \
 && npm run build

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

# 보안: 비루트 실행
RUN chown -R node:node /web
USER node

EXPOSE 3000
# Next 기본 start 스크립트(-p 3000). Caddy가 3000으로 프록시
CMD ["npm", "run", "start", "--", "-p", "3000"]