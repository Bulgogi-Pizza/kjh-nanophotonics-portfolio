import reflex as rx

from ..layout import main_layout
from ..state.state import State


@rx.page(route="/admin/add-media", title="Add Media")
def add_media_form() -> rx.Component:
    """새 미디어를 추가하는 폼 페이지."""
    return main_layout(
        rx.vstack(
            rx.heading("Add New Media", size="7"),
            rx.cond(
                State.form_media_error_message != "",
                rx.callout(
                    State.form_media_error_message,
                    icon="triangle_alert",
                    color_scheme="red",
                    role="alert",
                    width="100%",
                ),
            ),
            rx.form(
                rx.vstack(
                    rx.input(
                        placeholder="Title",
                        on_change=State.set_form_media_title,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Outlet (e.g., YTN 사이언스)",
                        on_change=State.set_form_media_outlet,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Publication Date (YYYY-MM)",
                        on_change=State.set_form_media_date,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Media URL",
                        on_change=State.set_form_media_url,
                        width="100%",
                    ),
                    rx.button("Add Media", type="submit", width="100%"),
                    spacing="4",
                ),
                on_submit=State.add_media,
                width="100%",
            ),
            width="100%",
            max_width="600px",
            margin="auto",
            padding_top="10%",
        )
    )