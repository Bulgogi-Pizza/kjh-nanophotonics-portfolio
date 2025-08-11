from datetime import datetime
from typing import List, Optional, Tuple

import reflex as rx
from sqlalchemy import desc
from sqlmodel import Session, select

import rxconfig

from ..models import Publication, ResearchArea


class State(rx.State):
  """Reflex 상태. 폼 값과 목록 상태를 들고 있으며, 이벤트 핸들러를 제공합니다."""

  # ---- 폼 상태 (타입 명시) ----
  form_title: str = ""
  form_authors: str = ""
  form_journal: str = ""
  form_publication_date: str = ""  # "YYYY-MM"
  form_selected_research_area_id: str = ""  # 셀렉트 박스 값 (빈 문자열일 수 있음)
  form_doi: str = ""
  form_abstract: str = ""

  # ---- 페이지 상태 ----
  publications: List[Publication] = []
  research_areas: List[ResearchArea] = []

  # ---- 이벤트 세터 (mypy가 attr 확인 가능하도록 명시) ----
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

  # ---- 페이지 로드시 데이터 로드 ----
  async def load_publications_page(self) -> None:
    """연구 분야/출판물 목록을 불러옵니다."""
    with Session(rxconfig.config.engine) as session:  # 엔진 주입 방식에 맞게 조정
      # 연구 분야 먼저
      self.research_areas = session.exec(select(ResearchArea)).all()

      # 출판물 쿼리: where로 조건 추가하고, 정렬은 sqlalchemy.desc 사용
      q = select(Publication)

      # 선택된 연구 분야가 있으면 where에 '식'을 전달 (bool이 아닌 Column Element)
      if self.form_selected_research_area_id:
        selected_id = int(self.form_selected_research_area_id)
        q = q.where(Publication.research_area_id == selected_id)

      q = q.order_by(desc(Publication.date))  # ✅ mypy 친화적

      self.publications = session.exec(q).all()

  @rx.var
  def research_area_options(self) -> List[Tuple[str, str]]:
    """드롭다운에 사용할 (이름, ID) 튜플 리스트를 반환합니다."""
    return [(area.name, str(area.id)) for area in self.research_areas]

  def get_all_publications(self, area_id: Optional[int] = None):
    with rx.session() as session:
      query = session.query(Publication).order_by(
        Publication.publication_date.desc())
      if area_id:
        query = query.filter(Publication.research_area_id == area_id)
      self.publications = query.all()

  def add_publication(self):
    self.form_error_message = ""

    try:
      pub_date = datetime.strptime(self.form_publication_date, "%Y-%m").date()
    except ValueError:
      self.form_error_message = "날짜 형식이 올바르지 않습니다 (YYYY-MM 형식으로 입력해주세요)."
      return

    with rx.session() as session:
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

  def get_all_research_areas(self):
    with rx.session() as session:
      self.research_areas = session.query(ResearchArea).all()

  def add_research_area(self):
    with rx.session() as session:
      new_area = ResearchArea(name=self.form_research_area_name)
      session.add(new_area)
      session.commit()
    self.get_all_research_areas()