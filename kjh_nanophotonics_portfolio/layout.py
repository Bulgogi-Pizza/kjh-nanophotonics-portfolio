import reflex as rx

from kjh_nanophotonics_portfolio.components.navbar import navbar


def main_layout(child: rx.Component) -> rx.Component:
  """
  모든 페이지에 적용될 기본 레이아웃.
  네비게이션 바와 메인 컨텐츠 영역을 포함.
  """
  return rx.box(
      navbar(),
      rx.container(
          child,
          padding_top="6em",
          max_width="960px",
      ),
  )