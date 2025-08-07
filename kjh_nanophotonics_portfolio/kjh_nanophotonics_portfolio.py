import reflex as rx
from kjh_nanophotonics_portfolio.layout import main_layout


class State(rx.State):
    """The app state."""
    pass

@rx.page(route="/", title="Home | Joohoon Kim POrtfolio")
def index() -> rx.Component:
    # Welcome Page (Index)
    return main_layout(
        rx.vstack(
            rx.heading("Welcome to Joohoon Kim's Portfolio", size="8"),
            rx.text(
                """
                my name is joohoon kim
                I research for nanophotonics
                """
            ),
            align="center",
            spacing="7",
            font_size="2em",
            padding_top="10%",
        )
    )

app = rx.App()
