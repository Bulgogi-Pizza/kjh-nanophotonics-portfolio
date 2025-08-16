import os
import sys

from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
from sqlmodel import SQLModel, create_engine

# models.py를 임포트해야 SQLModel이 테이블들을 인식할 수 있습니다.
from kjh_nanophotonics_portfolio import models  # pragma: import

models
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not configured.")

engine = create_engine(DATABASE_URL)


def check_db_connection():
    """데이터베이스 연결을 확인하고, 실패 시 에러 메시지와 함께 종료합니다."""
    try:
        # engine.connect()를 실행하여 실제로 DB에 연결을 시도합니다.
        with engine.connect() as connection:
            print("✅ Database connection successful.")
    except OperationalError as e:
        print("❌ Database connection failed.")
        print(f"Error: {e}")
        print("\n[문제 해결 체크리스트]")
        print("1. `.env` 파일의 DATABASE_URL 주소, 사용자, 비밀번호, DB 이름이 정확한가요?")
        print("2. PostgreSQL Docker 컨테이너가 정상적으로 실행 중인가요? (`docker ps`로 확인)")
        print("3. 방화벽이 5432 포트 연결을 막고 있지는 않나요?")
        sys.exit(1)  # 에러 코드(1)와 함께 스크립트 종료


check_db_connection()


def init_db() -> None:
    """SQLModel 메타데이터를 기반으로 모든 테이블을 생성합니다."""
    print("Creating Database tables...")
    SQLModel.metadata.create_all(engine)
    print("Table creation complete.")


if __name__ == "__main__":
    check_db_connection()  # 테이블 생성 전에 연결부터 확인
    init_db()
