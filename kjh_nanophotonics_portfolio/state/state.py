import reflex as rx
from ..models import Publication  # 상위 폴더의 models.py에서 Publication 가져오기


class State(rx.State):
  """The app state."""

  publications: list[Publication] = []
  form_title: str
  form_authors: str
  form_journal: str
  form_year: str
  form_doi: str
  form_abstract: str

  def get_all_publications(self):
    with rx.session() as session:
      self.publications = session.query(Publication).order_by(
        Publication.year.desc()).all()

  def add_publication(self):
    with rx.session() as session:
      new_publication = Publication(
          title=self.form_title,
          authors=self.form_authors,
          journal=self.form_journal,
          year=int(self.form_year) if self.form_year.isdigit() else 2025,
          doi=self.form_doi,
          abstract=self.form_abstract,
      )
      session.add(new_publication)
      session.commit()

    self.get_all_publications()