import os

import reflex as rx
from dotenv import load_dotenv

load_dotenv()

class KjhPortfolioConfig(rx.Config):
  pass

config = rx.Config(
    app_name="kjh_nanophotonics_portfolio",
    db_url=os.getenv("DATABASE_URL"),
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)