from datetime import date

import pytest
from sqlmodel import Session

from kjh_nanophotonics_portfolio.models import Publication, ResearchArea
from kjh_nanophotonics_portfolio.state.state import State


def _seed(db: Session):
    ra1 = ResearchArea(name="Nanophotonics")
    ra2 = ResearchArea(name="Metamaterials")
    db.add_all([ra1, ra2])
    db.commit()
    db.refresh(ra1)
    db.refresh(ra2)

    pub1 = Publication(
        title="Paper A",
        authors="A, B",
        journal="Optics Letters",
        publication_date=date(2024, 6, 1),
        doi="10.1111/a",
        abstract="A",
        research_area_id=ra1.id,
    )
    pub2 = Publication(
        title="Paper B",
        authors="C, D",
        journal="Nature Photonics",
        publication_date=date(2023, 12, 1),
        doi="10.1111/b",
        abstract="B",
        research_area_id=ra2.id,
    )
    db.add_all([pub1, pub2])
    db.commit()
    return ra1, ra2


@pytest.mark.anyio
async def test_load_and_filter(db: Session):
    ra1, ra2 = _seed(db)

    s = State()

    # 페이지 로드: 연구분야 + 출판물 적재
    await s.load_publications_page()
    assert len(s.research_areas) == 2
    assert len(s.publications) == 2

    # 필터링
    s.filter_publications_by_area(int(ra1.id))
    assert all(p.research_area_id == ra1.id for p in s.publications)

    # 전체보기
    s.get_all_publications()
    assert len(s.publications) == 2


def test_add_publication_ok_and_error(db: Session):
    _seed(db)
    s = State()

    # 에러 경로: 잘못된 날짜 형식
    s.set_form_publication_date("2024/06")
    s.add_publication()
    assert s.form_error_message != ""

    # 정상 경로
    s.set_form_title("New Paper")
    s.set_form_authors("E, F")
    s.set_form_journal("PRL")
    s.set_form_publication_date("2024-07")
    s.set_form_doi("10.2222/c")
    s.set_form_abstract("C")
    # 연구분야는 선택 안 해도 등록 가능(None 허용)
    s.add_publication()
    # 등록 후 전체 로드
    s.get_all_publications()
    assert any(p.title == "New Paper" for p in s.publications)


def test_research_area_crud(db: Session):
    s = State()
    s.form_research_area_name = "Plasmonics"
    s.add_research_area()
    s.get_all_research_areas()
    assert any(ra.name == "Plasmonics" for ra in s.research_areas)
    # 옵션 튜플 생성
    opts = s.research_area_options
    assert all(isinstance(name, str) and isinstance(val, str) for name, val in opts)

def test_add_research_area_empty_name(db):
    s = State()
    s.get_all_research_areas()
    before = len(s.research_areas)
    s.form_research_area_name = "   "  # 빈 이름 → 가드 분기
    s.add_research_area()
    s.get_all_research_areas()
    assert len(s.research_areas) == before

def test_set_selected_area_setter_covers():
    s = State()
    s.set_form_selected_research_area_id("123")
    assert s.form_selected_research_area_id == "123"