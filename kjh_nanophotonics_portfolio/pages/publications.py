import reflex as rx

from ..layout import main_layout
from ..models import Publication
from ..state.state import State


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
                    # 날짜 포맷팅은 문자열로 안전하게 표기
                    rx.text(str(pub.publication_date)),
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
                    on_click=State.get_all_publications,  # 함수 호출 X, 참조만
                    size="2",
                ),
                rx.foreach(
                    State.research_areas,
                    lambda area: rx.button(
                        area.name,
                        # 클릭 시 선택한 분야로 필터링하는 이벤트 호출
                        on_click=lambda area_id=area.id: State.filter_publications_by_area(
                            int(area_id)
                        ),
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