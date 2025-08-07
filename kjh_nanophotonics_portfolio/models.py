from typing import Optional, List
from datetime import date
from sqlmodel import Field, SQLModel, Relationship


class ResearchArea(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  name: str = Field(unique=True, index=True)

  # Publication과의 관계 설정 (역방향)
  publications: List["Publication"] = Relationship(
    back_populates="research_area")


class Publication(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  title: str = Field(index=True)
  authors: str
  journal: str
  publication_date: date

  # 선택적 필드들
  volume: Optional[str] = None
  issue: Optional[str] = None
  pages: Optional[str] = None
  doi: Optional[str] = None
  abstract: Optional[str] = None
  image_url: Optional[str] = None  # 대표 이미지 URL
  pdf_url: Optional[str] = None  # PDF 파일 링크 URL

  research_area_id: Optional[int] = Field(default=None,
                                          foreign_key="researcharea.id")

  # 연구 분야 (나중에 별도 테이블로 분리할 수 있음)
  research_area: Optional[ResearchArea] = Relationship(
    back_populates="publications")
