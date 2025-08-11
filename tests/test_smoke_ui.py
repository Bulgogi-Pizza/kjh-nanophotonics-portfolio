import pytest

# Reflex 임포트가 환경/버전 충돌로 실패하면 전체 테스트 모듈 스킵
try:
    import reflex as rx  # noqa: F401

    from kjh_nanophotonics_portfolio.components.navbar import navbar
    from kjh_nanophotonics_portfolio.layout import main_layout
    from kjh_nanophotonics_portfolio.pages.publications import publications
except Exception as e:  # pragma: no cover
    pytest.skip(f"Skip UI smoke tests: Reflex import failed ({e})", allow_module_level=True)


def test_navbar_and_layout():
    comp = navbar()
    assert comp is not None
    wrapped = main_layout(rx.box("x"))
    assert wrapped is not None


def test_publications_page_builds():
    comp = publications()
    assert comp is not None