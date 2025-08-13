import os

import pytest
from sqlmodel import Session, SQLModel, create_engine

os.environ.setdefault("RX_SHIM_FORCE_STUB", "1")  # reflex 스텁 강제 (테스트 전용)
os.environ.setdefault("DATABASE_URL", "sqlite://")

@pytest.fixture(scope="function")   # ← session → function
def test_engine():
    # in-memory SQLite, 테스트마다 엔진 새로 생성
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    from kjh_nanophotonics_portfolio import models as _models  # noqa: F401
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture(autouse=True)
def _patch_engine(monkeypatch: pytest.MonkeyPatch, test_engine):
    import create_db
    from kjh_nanophotonics_portfolio.state import state as state_mod
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    monkeypatch.setattr(create_db, "engine", test_engine, raising=False)
    monkeypatch.setattr(state_mod, "engine", test_engine, raising=False)

@pytest.fixture
def db(test_engine):
    with Session(test_engine) as s:
        yield s