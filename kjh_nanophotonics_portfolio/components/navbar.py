import reflex as rx
from pygments.styles.dracula import background


def navbar() -> rx.Component:
  menu_items = [
    ("Home", "/"),
    ("Research", "/research"),
    ("About Me", "/about"),
    ("Publications", "/publications"),
    ("Media", "/media"),
    ("Gallery", "/gallery"),
    ("Notice", "/notice"),
    ("Contact", "/contact"),
  ]

  return rx.box(
      rx.hstack(
          rx.heading("Joohoon Kim Portfolio", size="6"),
          rx.spacer(),
          rx.hstack(
              *[
                rx.link(
                    name,
                    href=url,
                    padding="1em",
                    _hover={"background_color": "#f0f0f0", "border_radius": "5px"},
                )
                for name, url in menu_items
              ],
              spacing="4",
          ),
          rx.spacer(),
          rx.color_mode.button(),
      ),
      position="fixed",
      top="0px",
      left="0px",
      right="0px",
      z_index="1000",
      padding="1em",
      backdrop_filter="blur(10px)",
      background_color="rgba(255, 255, 255, 0.8)",
      border_bottom="1px solid #f0f0f0",
      _dark={
        "backgroud_color": "rgba(18, 18, 18, 0.8)",
        "border_bottom": "1px solid #333",
      },
  )