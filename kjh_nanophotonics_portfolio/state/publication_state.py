from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional, cast

from sqlalchemy import extract
from sqlmodel import Session, select, desc

from create_db import engine
from .base_state import BaseState
from ..models import Publication
from ..utils.rx_shim import rx


class PublicationState(BaseState):
    """Publication 및 ResearchArea 관련 상태 및 이벤트 핸들러."""
    form_title: str = ""
    form_authors: str = ""
    form_journal: str = ""
    form_volume: str = ""
    form_pages: str = ""
    form_publication_date: str = ""
    form_contribution: str = ""
    form_selected_publication_year: Optional[int] = None
    form_selected_contribution: str = ""
    form_doi: str = ""
    form_abstract: str = ""
    form_error_message: str = ""
    publications: List[Publication] = []
    publication_years: List[int] = []
    contributions: List[str] = []

    def _refresh_publications(self) -> None:
        with Session(engine) as session:
            q = select(Publication)
            if self.form_selected_publication_year:
                q = q.where(
                    extract("year", Publication.publication_date)
                    == self.form_selected_publication_year
                )
            if self.form_selected_contribution:
                q = q.where(
                    Publication.contribution == self.form_selected_contribution)
            q = q.order_by(desc(cast(Any, Publication.publication_date)))
            self.publications = list(session.exec(q).all())

    async def load_publications_page(self) -> None:
        with Session(engine) as session:
            dates = session.exec(select(Publication.publication_date)).all()
            self.publication_years = list({d.year for d in dates})
            self.publication_years.sort(reverse=True)

    @rx.var
    def publications_count(self) -> int:
        return len(self.publications)

    @rx.var
    def publication_year_month_map(self) -> dict[int, str]:
        return {
            pub.id: f"{pub.publication_date.strftime('%Y-%m')}"
            for pub in self.publications if pub.id is not None
        }

    def get_all_publications(self) -> None:
        self.form_selected_publication_year = None
        self.form_selected_contribution = ""
        self._refresh_publications()

    def filter_all_publication_years(self) -> None:
        self.form_selected_publication_year = None
        self._refresh_publications()

    def filter_all_contributions(self) -> None:
        self.form_selected_contribution = ""
        self._refresh_publications()

    def filter_publications_by_year(self, year: Any) -> None:
        self.form_selected_publication_year = (
            int(year) if year not in ("", None) else None
        )
        self._refresh_publications()

    def filter_publications_by_contribution(self, contribution: Any) -> None:
        self.form_selected_contribution = str(contribution)
        self._refresh_publications()

    def add_publication(self, form_data: Optional[dict] = None) -> None:
        self.form_error_message = ""
        try:
            pub_date = datetime.strptime(self.form_publication_date,
                                         "%Y-%m").date()
        except ValueError:
            self.form_error_message = "날짜 형식이 올바르지 않습니다.\n예: YYYY-MM"
            return
        with Session(engine) as session:
            new_publication = Publication(
                title=self.form_title,
                authors=self.form_authors,
                contribution=self.form_contribution,
                journal=self.form_journal,
                volume=self.form_volume,
                pages=self.form_pages,
                publication_date=pub_date,
                doi=self.form_doi,
            )
            session.add(new_publication)
            session.commit()
        self.get_all_publications()
