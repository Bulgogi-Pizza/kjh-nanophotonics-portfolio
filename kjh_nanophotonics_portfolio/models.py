from datetime import date
from typing import Optional

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class Publication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    authors: str
    journal: str
    publication_date: date
    contribution: str
    volume: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None


class Media(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    outlet: str
    publication_date: date
    url: str
    image_url: Optional[str] = None


class CVContent(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True)
    content: str = Field(default="", sa_column=Column(Text))
