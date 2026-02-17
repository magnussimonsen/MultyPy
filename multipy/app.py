from textual.app import App
from multipy.views.menu_view import MenuView

class MultiPyApp(App):
    CSS = """
    Screen {
        background: $surface-darken-1;
    }
    """
    TITLE = "MultiPy"
    BINDINGS = [
        ("q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        self.push_screen(MenuView())

if __name__ == "__main__":
    app = MultiPyApp()
    app.run()
