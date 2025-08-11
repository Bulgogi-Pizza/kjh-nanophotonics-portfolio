import os
from typing import cast

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise ValueError("DB_URL is not configured.")
engine = create_engine(cast(str, DB_URL))

def init_db() -> None:
  print("Creating Database tables...")
  SQLModel.metadata.create_all(engine)
  print("Table creation complete")

if __name__ == "__main__":
  init_db()