import reflex as rx

from ..layout import main_layout
from ..state.cv_state import CVState as State

@rx.page(route="/cv", title="CV", on_load=State.load_cv_page)
def cv_page() -> rx.Component:
    """DB에 저장된 마크다운 CV를 보여주는 페이지."""
    return main_layout(
        rx.box(
            rx.markdown(State.cv_content),
            width="100%",
            padding_top="5%",
        )
    )