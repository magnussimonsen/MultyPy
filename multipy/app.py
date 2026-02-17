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
        ("a", "about", "About"), # Note: 'a' bindings might conflict if typing in normal mode, handled by context usually or focus
    ]

    def on_mount(self) -> None:
        self.push_screen(MenuView())

    def action_about(self) -> None:
        # Global binding for about - checks if we are already there?
        # For simplicity, we can just push it if not present, but 
        # MenuView handles it explicitly.
        # Let's let the views handle navigation to keep stacks clean.
        pass

if __name__ == "__main__":
    app = MultiPyApp()
    app.run()
