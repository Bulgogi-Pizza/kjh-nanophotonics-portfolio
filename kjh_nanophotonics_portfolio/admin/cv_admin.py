import reflex as rx

from ..layout import main_layout
from ..state.cv_state import CVState as State

@rx.page(route="/admin/edit-cv", title="Edit CV", on_load=State.load_cv_editor)
def edit_cv_page() -> rx.Component:
    """CV 내용을 마크다운으로 수정하는 페이지."""
    return main_layout(
        rx.vstack(
            rx.heading("Edit CV", size="8"),
            rx.text("이곳에서 마크다운 문법을 사용하여 CV를 수정할 수 있습니다."),
            rx.text_area(
                value=State.cv_editor_content,
                on_change=State.set_cv_editor_content,
                height="60vh",
                width="100%",
                font_family="monospace",
            ),
            rx.button("Save CV", on_click=State.save_cv_content, margin_top="1em"),
            width="100%",
            padding_top="5%",
        )
    )