FROM python:3.11-slim AS api
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 REFLEX_ENV=prod
WORKDIR /app

# 빌드 도구는 최소화; 필요한 경우에만 설치
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# 의존성 설치 (reflex 포함)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt reflex

# 앱 소스 복사
COPY . /app

EXPOSE 8000
# Reflex CLI로 백엔드만 실행 (버전에 따라 옵션이 다를 수 있어 아래 두 줄 중 하나 사용)
# 1) 최신 CLI가 지원한다면:
CMD ["reflex", "run", "--env", "prod", "--backend-only"]
# 2) 일부 버전은 python -m 형태가 더 안정적일 수 있음:
# CMD ["python", "-m", "reflex", "run", "--env", "prod", "--backend-only"]