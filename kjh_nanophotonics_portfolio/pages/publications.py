import reflex as rx
from ..layout import main_layout
from ..state.state import State
from ..models import Publication

@rx.page(route="/publications", title="Publications", on_load=State.get_all_publications)
def publications() -> rx.Component:
    """데이터베이스에서 가져온 논문 목록을 보여주는 페이지"""
    def publication_card(pub: Publication):
        return rx.box(
            rx.vstack(
                rx.heading(pub.title, size="5"),
                rx.text(pub.authors, font_style="italic"),
                rx.text(f"{pub.journal}, {pub.year}"),
                rx.link("DOI Link", href=f"https://doi.org/{pub.doi}", is_external=True),
                spacing="2",
                align_items="start",
            ),
            border="1px solid #ddd", padding="1em", border_radius="8px", width="100%",
        )

    return main_layout(
        rx.vstack(
            rx.heading("Publications", size="7", margin_bottom="1em"),
            rx.foreach(State.publications, publication_card),
            spacing="5",
            width="100%",
        )
    )