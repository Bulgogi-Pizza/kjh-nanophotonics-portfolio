import reflex as rx

from ..layout import main_layout
from ..state.publication_state import PublicationState as State


@rx.page(route="/admin/add-publication", title="Add Publication")
def add_publication_form() -> rx.Component:
    """새 논문을 추가하는 폼 페이지."""
    return main_layout(
        rx.vstack(
            rx.heading("Add New Publication", size="7"),
            rx.cond(
                State.form_error_message != "",
                rx.callout(
                    State.form_error_message,
                    icon="alert_triangle",
                    color_scheme="red",
                    role="alert",
                    width="100%",
                ),
            ),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Title",
                        on_change=State.set_form_title,
                        width="100%",
                    ),
                    rx.hstack(
                        rx.input(
                            placeholder="Authors (e.g., A, B, C)",
                            on_change=State.set_form_authors,
                            width="60%",
                        ),
                        rx.select(
                            items=["First author", "Co-author",
                                   "Corresponding author"],
                            placeholder="Contribution",
                            on_change=State.set_form_contribution,
                            width="40%",
                            position="popper",
                        ),
                        width="100%",
                    ),
                    rx.hstack(
                        rx.input(
                            placeholder="Journal / Conference",
                            on_change=State.set_form_journal,
                            width="60%",
                        ),
                        rx.input(
                            placeholder="Volume",
                            on_change=State.set_form_volume,
                            width="20%",
                        ),
                        rx.input(
                            placeholder="Page",
                            on_change=State.set_form_pages,
                            width="20%",
                        ),
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Publication Date (YYYY-MM)",
                        on_change=State.set_form_publication_date,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="DOI (e.g., 10.1000/xyz)",
                        on_change=State.set_form_doi,
                        width="100%",
                    ),
                    rx.button(
                        "Add Publication",
                        type="submit",
                        width="100%",
                    ),
                    spacing="4",
                ),
                on_submit=State.add_publication,  # State에 구현 필요
                width="100%",
            ),
            width="100%",
            max_width="600px",
            margin="auto",
            padding_top="10%",
        )
    )
