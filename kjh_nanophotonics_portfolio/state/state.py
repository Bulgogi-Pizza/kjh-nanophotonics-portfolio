import reflex as rx
from datetime import date, datetime
from ..models import Publication  # 상위 폴더의 models.py에서 Publication 가져오기

class State(rx.State):
  publications: list[Publication] = []
  form_title: str
  form_authors: str
  form_journal: str
  form_publication_date: str
  form_doi: str
  form_abstract: str
  form_error_message: str = ""

  def get_all_publications(self):
    with rx.session() as session:
      self.publications = session.query(Publication).order_by(
        Publication.publication_date.desc()).all()

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
      )
      session.add(new_publication)
      session.commit()

    self.get_all_publications()