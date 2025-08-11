import importlib


def test_init_db_runs(monkeypatch):
    monkeypatch.setenv("DB_URL", "sqlite://")   # 보호차원 이중 세팅
    create_db = importlib.import_module("create_db")
    importlib.reload(create_db)                 # 환경변수 반영 강제
    create_db.init_db()