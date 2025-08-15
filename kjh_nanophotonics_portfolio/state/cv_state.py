from __future__ import annotations
from sqlmodel import Session
from create_db import engine
from ..models import CVContent
from .base_state import BaseState, rx


class CVState(BaseState):
  """CV 관련 상태 및 이벤트 핸들러."""
  cv_content: str = ""
  cv_editor_content: str = ""

  def _get_or_create_cv(self, session: Session) -> CVContent:
    cv = session.get(CVContent, 1)
    if not cv:
      cv = CVContent(id=1, content="# CV\n\n이곳에 내용을 입력하세요.")
      session.add(cv)
      session.commit()
      session.refresh(cv)
    return cv

  def load_cv_page(self):
    with Session(engine) as session:
      self.cv_content = self._get_or_create_cv(session).content

  def load_cv_editor(self):
    with Session(engine) as session:
      self.cv_editor_content = self._get_or_create_cv(session).content

  def save_cv_content(self):
    with Session(engine) as session:
      cv_to_update = self._get_or_create_cv(session)
      cv_to_update.content = self.cv_editor_content
      session.add(cv_to_update)
      session.commit()
    self.cv_content = self.cv_editor_content
    return rx.toast.success("CV 내용이 저장되었습니다!")