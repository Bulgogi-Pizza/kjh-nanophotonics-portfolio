from datetime import datetime
from typing import List, Optional, Tuple

import reflex as rx
from sqlalchemy import desc
from sqlmodel import Session, select

import rxconfig
from ..models import Publication, ResearchArea


class State(rx.State):
    """Reflex 상태: 폼 값/목록 상태 + 이벤트 핸들러."""

    # ---- 폼 상태 ----
    form_title: str = ""
    form_authors: str = ""
    form_journal: str = ""
    form_publication_date: str = ""  # "YYYY-MM"
    form_selected_research_area_id: str = ""  # 셀렉트 박스(빈 문자열 가능)
    form_doi: str = ""
    form_abstract: str = ""
    form_research_area_name: str = ""  # 연구 분야 추가용
    form_error_message: str = ""

    # ---- 페이지 상태 ----
    publications: List[Publication] = []
    research_areas: List[ResearchArea] = []

    # =========================
    # 기본 세터 (mypy가 속성 확인 가능)
    # =========================
    def set_form_title(self, v: str) -> None:
        self.form_title = v

    def set_form_authors(self, v: str) -> None:
        self.form_authors = v

    def set_form_journal(self, v: str) -> None:
        self.form_journal = v

    def set_form_publication_date(self, v: str) -> None:
        self.form_publication_date = v

    def set_form_selected_research_area_id(self, v: str) -> None:
        self.form_selected_research_area_id = v

    def set_form_doi(self, v: str) -> None:
        self.form_doi = v

    def set_form_abstract(self, v: str) -> None:
        self.form_abstract = v

    # =========================
    # 유틸
    # =========================
    def _refresh_publications(self) -> None:
        """현재 선택된 연구 분야 기준으로 출판물 목록을 갱신."""
        with Session(rxconfig.config.engine) as session:
            q = select(Publication)
            if self.form_selected_research_area_id:
                selected_id = int(self.form_selected_research_area_id)
                q = q.where(Publication.research_area_id == selected_id)

            q = q.order_by(desc(Publication.publication_date))
            self.publications = session.exec(q).all()

    # =========================
    # 페이지 로드
    # =========================
    async def load_publications_page(self) -> None:
        """연구 분야/출판물 목록 초기 로드."""
        with Session(rxconfig.config.engine) as session:
            self.research_areas = session.exec(select(ResearchArea)).all()
        self._refresh_publications()

    @rx.var
    def research_area_options(self) -> List[Tuple[str, str]]:
        """드롭다운에 사용할 (이름, ID) 튜플 리스트."""
        return [(area.name, str(area.id)) for area in self.research_areas]

    # =========================
    # 목록 필터링 이벤트
    # =========================
    def get_all_publications(self) -> None:
        """모든 출판물 보기(필터 해제)."""
        self.form_selected_research_area_id = ""
        self._refresh_publications()

    def filter_publications_by_area(self, area_id: int) -> None:
        """특정 연구 분야로 필터링."""
        self.form_selected_research_area_id = str(area_id)
        self._refresh_publications()

    # =========================
    # 출판물 추가
    # =========================
    def add_publication(self, form_data: Optional[dict] = None) -> None:
        """새 출판물 등록(on_submit 콜백 호환)."""
        self.form_error_message = ""

        try:
            pub_date = datetime.strptime(self.form_publication_date, "%Y-%m").date()
        except ValueError:
            self.form_error_message = "날짜 형식이 올바르지 않습니다 (YYYY-MM 형식으로 입력해주세요)."
            return

        with Session(rxconfig.config.engine) as session:
            new_publication = Publication(
                title=self.form_title,
                authors=self.form_authors,
                journal=self.form_journal,
                publication_date=pub_date,
                doi=self.form_doi,
                abstract=self.form_abstract,
                research_area_id=(
                    int(self.form_selected_research_area_id)
                    if self.form_selected_research_area_id
                    else None
                ),
            )
            session.add(new_publication)
            session.commit()

        self.get_all_publications()

    # =========================
    # 연구 분야 목록/추가
    # =========================
    def get_all_research_areas(self) -> None:
        with Session(rxconfig.config.engine) as session:
            self.research_areas = session.exec(select(ResearchArea)).all()

    def add_research_area(self, form_data: Optional[dict] = None) -> None:
        name = self.form_research_area_name.strip()
        if not name:
            return
        with Session(rxconfig.config.engine) as session:
            session.add(ResearchArea(name=name))
            session.commit()
        self.get_all_research_areas()