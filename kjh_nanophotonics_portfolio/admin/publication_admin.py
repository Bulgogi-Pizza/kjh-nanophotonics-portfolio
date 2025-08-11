import reflex as rx

from ..layout import main_layout
from ..state.state import State


@rx.page(route="/admin/add-publication", title="Add Publication")
def add_publication_form() -> rx.Component:
    """새 논문을 추가하는 폼 페이지"""
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
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Authors (e.g., A, B, C)",
                        on_change=State.set_form_authors,
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Journal / Conference",
                        on_change=State.set_form_journal,
                        width="100%"
                    ),
                    rx.input(
                        placeholder="Publication Date (YYYY-MM)",
                        on_change=State.set_form_publication_date,
                        width="100%"
                    ),
                    rx.select.root(
                        rx.select.trigger(
                            placeholder="Select Research Area"
                        ),
                        rx.select.content(
                            rx.foreach(
                                State.research_area_options,
                                lambda option: rx.select.item(
                                    option[0],
                                    value=option[1]
                                )
                            )
                        ),
                        on_change=State.set_form_selected_research_area_id,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="DOI (e.g., 10.1000/xyz)",
                        on_change=State.set_form_doi,
                        width="100%"
                    ),
                    rx.text_area(
                        placeholder="Abstract",
                        on_change=State.set_form_abstract,
                        width="100%"
                    ),
                    rx.button(
                        "Add Publication",
                        type="submit",
                        width="100%"
                    ),
                    spacing="4",
                ),
                on_submit=State.add_publication,
                width="100%",
            ),
            width="100%",
            max_width="600px",
            margin="auto",
            padding_top="10%"
        )
    )