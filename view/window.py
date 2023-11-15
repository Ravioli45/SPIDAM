import pyglet

class AppWindow(pyglet.window.Window):
    """
    The main window for the application
    """

    def __init__(self):
        super().__init__(1200, 675, caption="Audio Analyzer")

