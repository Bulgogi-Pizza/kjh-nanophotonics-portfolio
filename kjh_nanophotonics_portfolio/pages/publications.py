from typing import Callable

import reflex as rx

from ..layout import main_layout
from ..models import Publication
from ..state.publication_state import PublicationState as State


def _year_filter_handler(year: int) -> Callable[[], None]:
    handler = State.filter_publications_by_year
    return lambda: handler(year)


def _contribution_filter_handler(contribution: str) -> Callable[[], None]:
    handler = State.filter_publications_by_contribution
    return lambda: handler(contribution)


@rx.page(
    route="/publications",
    title="Publications",
    on_load=State.load_publications_page,
)
def publications() -> rx.Component:
    """데이터베이스에서 가져온 논문 목록을 보여주는 페이지."""

    def publication_card(pub: Publication, index: int) -> rx.Component:
        return rx.box(
            rx.hstack(
                rx.text(
                    f"{State.publications_count - index}",
                    size="5",
                    width="40px",
                    text_align="center",
                ),
                rx.vstack(
                    rx.heading(pub.title, size="4"),
                    rx.text(pub.authors, font_style="italic",
                            color_scheme="gray"),
                    rx.hstack(
                        rx.text(pub.journal, font_style="italic",
                                font_weight="bold"),
                        rx.text(
                            f", {State.publication_year_month_map[pub.id]}"
                        ),
                        rx.cond(
                            pub.volume,
                            rx.hstack(
                                rx.text(","),
                                rx.text(pub.volume, font_weight="bold"),
                                spacing="2",
                            ),
                        ),
                        rx.cond(
                            pub.pages,
                            rx.text(f", pp. {pub.pages}"),
                        ),
                        spacing="2",
                        align_items="center",
                    ),
                    rx.link(
                        "DOI Link",
                        href=f"https://doi.org/{pub.doi}",
                        is_external=True,
                        size="2",
                    ),
                    spacing="2",
                    align_items="start",
                ),
                spacing="4",
                align_items="center",
            ),
            border="1px solid #ddd",
            padding="1.5em",
            border_radius="8px",
            width="100%",
        )

    return main_layout(
        rx.vstack(
            rx.heading("Publications", size="7", margin_bottom="1em"),
            rx.hstack(
                rx.button(
                    "All",
                    on_click=State.filter_all_contributions,  # 함수 참조만
                    size="2",
                ),
                rx.foreach(
                    State.contributions,
                    lambda contribution: rx.button(
                        contribution,
                        on_click=_contribution_filter_handler(contribution),
                        size="2",
                    ),
                ),
                spacing="3",
                margin_bottom="2em",
            ),
            rx.hstack(
                rx.button(
                    "All",
                    on_click=State.filter_all_publication_years(),
                    size="2",
                ),
                rx.foreach(
                    State.publication_years,
                    lambda year: rx.button(
                        year,
                        on_click=_year_filter_handler(year),
                        size="2",
                    ),
                ),
                spacing="3",
                margin_bottom="2em",
            ),
            rx.foreach(
                State.publications,
                lambda pub, index: publication_card(pub, index)
            ),
            spacing="5",
            width="100%",
            padding_top="10%",
        )
    )
