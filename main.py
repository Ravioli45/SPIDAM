from model import get_window_instance
from view import AppWindow

import pyglet

if __name__ == "__main__":
    window = AppWindow()
    get_window_instance(window)
    pyglet.app.run()
