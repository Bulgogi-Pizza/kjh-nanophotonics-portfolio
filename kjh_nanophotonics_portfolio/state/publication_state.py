from __future__ import annotations
from typing import Any, List, Optional, Tuple, cast
from datetime import datetime
from sqlmodel import Session, select, desc
from create_db import engine
from ..models import Publication, ResearchArea
from .base_state import BaseState, rx

class PublicationState(BaseState):
    """Publication 및 ResearchArea 관련 상태 및 이벤트 핸들러."""
    form_title: str = ""
    form_authors: str = ""
    form_journal: str = ""
    form_publication_date: str = ""
    form_selected_research_area_id: str = ""
    form_doi: str = ""
    form_abstract: str = ""
    form_research_area_name: str = ""
    form_error_message: str = ""
    publications: List[Publication] = []
    research_areas: List[ResearchArea] = []

    def _refresh_publications(self) -> None:
        with Session(engine) as session:
            q = select(Publication)
            if self.form_selected_research_area_id:
                q = q.where(Publication.research_area_id == int(self.form_selected_research_area_id))
            q = q.order_by(desc(cast(Any, Publication.publication_date)))
            self.publications = list(session.exec(q).all())

    async def load_publications_page(self) -> None:
        with Session(engine) as session:
            self.research_areas = list(session.exec(select(ResearchArea)).all())
        self._refresh_publications()

    @rx.var
    def research_area_options(self) -> List[Tuple[str, str]]:
        return [(area.name, str(area.id)) for area in self.research_areas]

    def get_all_publications(self) -> None:
        self.form_selected_research_area_id = ""
        self._refresh_publications()

    def filter_publications_by_area(self, area_id: Any) -> None:
        self.form_selected_research_area_id = str(area_id)
        self._refresh_publications()

    def add_publication(self, form_data: Optional[dict] = None) -> None:
        self.form_error_message = ""
        try:
            pub_date = datetime.strptime(self.form_publication_date, "%Y-%m").date()
        except ValueError:
            self.form_error_message = "날짜 형식이 올바르지 않습니다.\n예: YYYY-MM"
            return
        with Session(engine) as session:
            new_publication = Publication(
                title=self.form_title, authors=self.form_authors, journal=self.form_journal,
                publication_date=pub_date, doi=self.form_doi, abstract=self.form_abstract,
                research_area_id=int(self.form_selected_research_area_id) if self.form_selected_research_area_id else None
            )
            session.add(new_publication)
            session.commit()
        self.get_all_publications()

    def get_all_research_areas(self) -> None:
        with Session(engine) as session:
            self.research_areas = list(session.exec(select(ResearchArea)).all())

    def add_research_area(self, form_data: Optional[dict] = None) -> None:
        name = self.form_research_area_name.strip()
        if not name: return
        with Session(engine) as session:
            session.add(ResearchArea(name=name))
            session.commit()
        self.get_all_research_areas()