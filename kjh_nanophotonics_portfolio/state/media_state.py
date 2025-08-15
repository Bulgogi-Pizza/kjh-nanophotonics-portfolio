from __future__ import annotations
from typing import Any, List, Optional, cast
from datetime import datetime
from sqlmodel import Session, select, desc
from create_db import engine
from ..models import Media
from .base_state import BaseState, rx


class MediaState(BaseState):
  """Media 관련 상태 및 이벤트 핸들러."""
  form_media_title: str = ""
  form_media_outlet: str = ""
  form_media_date: str = ""
  form_media_url: str = ""
  form_media_error_message: str = ""
  media_items: List[Media] = []

  def load_media_page(self):
    with Session(engine) as session:
      q = select(Media).order_by(desc(cast(Any, Media.publication_date)))
      self.media_items = list(session.exec(q).all())

  def add_media(self, form_data: Optional[dict] = None):
    self.form_media_error_message = ""
    try:
      pub_date = datetime.strptime(self.form_media_date, "%Y-%m").date()
    except (ValueError, TypeError):
      self.form_media_error_message = "날짜 형식이 올바르지 않습니다 (YYYY-MM)."
      return
    if not self.form_media_url.strip():
      self.form_media_error_message = "미디어 링크(URL)는 필수 항목입니다."
      return
    with Session(engine) as session:
      new_media_item = Media(
          title=self.form_media_title, outlet=self.form_media_outlet,
          publication_date=pub_date, url=self.form_media_url
      )
      session.add(new_media_item)
      session.commit()
    self.load_media_page()