from sqlmodel import SQLModel, create_engine

import rxconfig
from kjh_nanophotonics_portfolio.models import Publication  # noqa: F401

db_url = rxconfig.config.db_url
if db_url is None:
    raise ValueError("DB_URL is not configured.")

engine = create_engine(db_url)

def init_db() -> None:
  print("Creating Database tables...")
  SQLModel.metadata.create_all(engine)
  print("Table creation complete")

if __name__ == "__main__":
  init_db()