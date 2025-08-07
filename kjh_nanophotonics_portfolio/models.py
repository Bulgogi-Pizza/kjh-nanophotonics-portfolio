from typing import Optional
from datetime import date
from sqlmodel import Field, SQLModel

class Publication(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  title: str = Field(index=True)
  authors: str # 저자 목룍 (예: "Joohoon Kim, John Doe, Hane Smith")
  journal: str # 학회 또는 저널 이름
  publication_date: date

  # 선택적 필드들
  volume: Optional[str] = None
  issue: Optional[str] = None
  pages: Optional[str] = None
  doi: Optional[str] = None
  abstract: Optional[str] = None
  image_url: Optional[str] = None  # 대표 이미지 URL
  pdf_url: Optional[str] = None  # PDF 파일 링크 URL

  # 연구 분야 (나중에 별도 테이블로 분리할 수 있음)
  research_area: Optional[str] = Field(default=None, index=True)