import reflex as rx

from ..layout import main_layout


@rx.page(route="/", title="Home | My Portfolio")
def index() -> rx.Component:
    """메인 홈페이지"""
    return main_layout(
        rx.vstack(
            rx.heading("안녕하세요, 제 포트폴리오에 오신 것을 환영합니다.", size="8"),
            rx.text(
                "이곳은 저의 연구 여정과 성과를 공유하는 공간입니다. "
                "Python과 Reflex를 사용하여 직접 만들었습니다."
            ),
            align="center", spacing="7", font_size="2em", padding_top="10%",
        )
    )