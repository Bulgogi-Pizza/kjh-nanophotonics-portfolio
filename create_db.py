import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from kjh_nanophotonics_portfolio import models

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not configured.") # pragma: no cover
engine = create_engine(DATABASE_URL)

def init_db() -> None:
  print("Creating Database tables...")
  SQLModel.metadata.create_all(engine)
  print("Table creation complete")

if __name__ == "__main__":
    init_db()