import reflex as rx
from datetime import date, datetime
from typing import Optional
from ..models import Publication, ResearchArea

class State(rx.State):
  publications: list[Publication] = []
  form_title: str
  form_authors: str
  form_journal: str
  form_publication_date: str
  form_doi: str
  form_abstract: str
  form_error_message: str = ""

  research_areas: list[ResearchArea] = []
  form_research_area_name: str
  form_selected_research_area_id: str  # 드롭다운에서 선택된 ID

  def get_all_publications(self, area_id: Optional[int] = None):
    with rx.session() as session:
      query = session.query(Publication).order_by(
        Publication.publication_date.desc())
      if area_id:
        query = query.filter(Publication.research_area_id == area_id)
      self.publications = query.all()

  def load_publications_page(self):
    self.get_all_research_areas()
    self.get_all_publications()

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
          research_area_id=int(self.form_selected_research_area_id) if self.form_selected_research_area_id else None
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