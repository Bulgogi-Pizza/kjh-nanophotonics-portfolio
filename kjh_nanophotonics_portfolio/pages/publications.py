from typing import Callable, cast

import reflex as rx

from ..layout import main_layout
from ..models import Publication
from ..state.state import State


def _area_filter_handler(area_id: int) -> Callable[[], None]:
    """버튼 on_click에 넘길 제로-인자 콜백 생성기.

    Reflex 런타임이 State 인스턴스를 바인딩하지만, mypy는 이를 모름.
    호출 지점만 예외 처리해 정적 타입 검사를 통과시킨다.
    """
    handler = cast("Callable[[int], None]", State.filter_publications_by_area)
    return lambda: handler(area_id)

@rx.page(
    route="/publications",
    title="Publications",
    on_load=State.load_publications_page,  # 콜백 참조만 전달
)
def publications() -> rx.Component:
    """데이터베이스에서 가져온 논문 목록을 보여주는 페이지."""

    def publication_card(pub: Publication) -> rx.Component:
        return rx.box(
            rx.vstack(
                rx.heading(pub.title, size="5"),
                rx.text(pub.authors, font_style="italic"),
                rx.hstack(
                    rx.text(f"{pub.journal},"),
                    rx.text(str(pub.publication_date)),  # 문자열로 안전하게 표기
                    spacing="2",
                ),
                rx.link(
                    "DOI Link",
                    href=f"https://doi.org/{pub.doi}",
                    is_external=True,
                ),
                spacing="2",
                align_items="start",
            ),
            border="1px solid #ddd",
            padding="1em",
            border_radius="8px",
            width="100%",
        )

    return main_layout(
        rx.vstack(
            rx.heading("Publications", size="7", margin_bottom="1em"),
            rx.hstack(
                rx.button(
                    "All",
                    on_click=State.get_all_publications,  # 함수 참조만
                    size="2",
                ),
                rx.foreach(
                    State.research_areas,
                    lambda area: rx.button(
                        area.name,
                        on_click=_area_filter_handler(int(area.id)),
                        size="2",
                    ),
                ),
                spacing="3",
                margin_bottom="2em",
            ),
            rx.foreach(State.publications, publication_card),
            spacing="5",
            width="100%",
            padding_top="10%",
        )
    )