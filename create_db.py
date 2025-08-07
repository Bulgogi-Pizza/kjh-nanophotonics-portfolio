from sqlmodel import SQLModel, create_engine
from kjh_nanophotonics_portfolio.models import Publication
import rxconfig

engine = create_engine(rxconfig.config.db_url)

def create_db_and_tables():
  print("Creating Database tables...")
  SQLModel.metadata.create_all(engine)
  print("Table creation complete")

if __name__ == "__main__":
  create_db_and_tables()