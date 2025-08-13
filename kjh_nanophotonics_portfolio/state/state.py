from datetime import datetime
from typing import Any, List, Optional, Tuple, cast

from sqlalchemy import desc
from sqlmodel import Session, select

from create_db import engine

from ..models import Publication, ResearchArea, Media
from ..utils.rx_shim import rx


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

    # Media 관련 폼/페이지 상태
    form_media_title: str = ""
    form_media_outlet: str = ""
    form_media_date: str = ""  # "YYYY-MM"
    form_media_url: str = ""
    form_media_error_message: str = ""
    media_items: List[Media] = []

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
        with Session(engine) as session:
            q = select(Publication)
            if self.form_selected_research_area_id:
                selected_id = int(self.form_selected_research_area_id)
                q = q.where(Publication.research_area_id == selected_id)

            col = cast(Any, Publication.publication_date)
            q = q.order_by(desc(col))
            self.publications = list(session.exec(q).all())

    # =========================
    # 페이지 로드
    # =========================
    async def load_publications_page(self) -> None:
        """연구 분야/출판물 목록 초기 로드."""
        with Session(engine) as session:
            self.research_areas = list(session.exec(select(ResearchArea)).all())
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

    def filter_publications_by_area(self, area_id: Any) -> None:
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
            self.form_error_message = (
                "날짜 형식이 올바르지 않습니다.\n"
                "예: YYYY-MM"
            )
            return

        with Session(engine) as session:
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
        with Session(engine) as session:
            self.research_areas = list(session.exec(select(ResearchArea)).all())

    def add_research_area(self, form_data: Optional[dict] = None) -> None:
        name = self.form_research_area_name.strip()
        if not name:
            return
        with Session(engine) as session:
            session.add(ResearchArea(name=name))
            session.commit()
        self.get_all_research_areas()

    # Media 관련 이벤트 핸들러
    def load_media_page(self):
        """Media 페이지 로드 시 모든 미디어 항목을 가져옴."""
        with Session(engine) as session:
            col = cast(Any, Media.publication_date)
            q = select(Media).order_by(desc(col))
            self.media_items = list(session.exec(q).all())

    def add_media(self, form_data: Optional[dict] = None):
        """새 미디어 항목 등록."""
        self.form_media_error_message = ""

        # 날짜 형식 검증
        try:
            pub_date = datetime.strptime(self.form_media_date,
                                         "%Y-%m").date()
        except (ValueError, TypeError):
            self.form_media_error_message = "날짜 형식이 올바르지 않습니다 (YYYY-MM)."
            return

        # URL 비어있는지 확인
        if not self.form_media_url.strip():
            self.form_media_error_message = "미디어 링크(URL)는 필수 항목입니다."
            return

        with Session(engine) as session:
            new_media_item = Media(
                title=self.form_media_title,
                outlet=self.form_media_outlet,
                publication_date=pub_date,
                url=self.form_media_url,
            )
            session.add(new_media_item)
            session.commit()

        # 성공 시, 목록 새로고침
        self.load_media_page()