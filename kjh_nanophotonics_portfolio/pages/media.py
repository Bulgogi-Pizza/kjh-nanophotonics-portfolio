import reflex as rx

from ..layout import main_layout
from ..models import Media
from ..state.state import State


@rx.page(route="/media", title="Media", on_load=State.load_media_page)
def media() -> rx.Component:
    """데이터베이스에서 가져온 미디어 목록을 보여주는 페이지."""

    def media_card(item: Media) -> rx.Component:
        return rx.link(
            rx.card(
                rx.vstack(
                    rx.heading(item.title, size="5"),
                    rx.hstack(
                        rx.text(f"{item.outlet} |"),
                        rx.text(
                            item.publication_date,
                            format_time="YYYY. MM."  # frontend에서 날짜 형식 지정
                        ),
                        spacing="2",
                        color_scheme="gray",
                    ),

                    spacing="2",
                    align_items="start",
                    width="100%",
                )
            ),
            href=item.url,
            is_external=True,
            width="100%",
        )

    return main_layout(
        rx.vstack(
            rx.heading("Media", size="8", margin_bottom="1em"),
            rx.cond(
                State.media_items,
                rx.vstack(
                    rx.foreach(State.media_items, media_card),
                    spacing="4",
                    width="100%",
                ),
                rx.text("아직 등록된 미디어 활동이 없습니다."),
            ),
            width="100%",
            padding_top="5%",
        )
    )