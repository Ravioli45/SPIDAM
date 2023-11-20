import pyglet
from pyglet.gui.widgets import PushButton
from pyglet.shapes import BorderedRectangle
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pathlib
from tkinter.filedialog import askopenfilename

# TODO import functions from controller once it is implemented
# from controller import ...

# telling pyglet where the assets folder is
assets = pathlib.Path(__file__).parents[1] / "assets"
pyglet.resource.path = [str(assets)]
pyglet.resource.reindex()

load_file_image = pyglet.resource.image("load_file_image.png")

def figure_to_image(fig):
    canvas = FigureCanvasAgg(fig)
    data, (width, height) = canvas.print_to_buffer()
    image = pyglet.image.ImageData(width, height, "RGBA", data, -4*width)
    return image

class AppWindow(pyglet.window.Window):
    """
    The main window for the application

    Contains all relevant ui elements and functions for the view
    """
    def __init__(self):
        super().__init__(1200, 675, caption="Audio Analyzer")

        self.figures: list = []
        self.images: list = []

        self.gui_batch = pyglet.graphics.Batch()
        self.gui_frame = pyglet.gui.Frame(self)

        self.load_file_button = PushButton(0, 575, pressed=load_file_image, depressed=load_file_image, batch=self.gui_batch)
        self.load_file_button.set_handler('on_press', self.on_load_file_press)

        # TODO replace white rectangles with actual gui elements
        self.placeholder1 = BorderedRectangle(300, 575, 900, 100, 10, border_color=(0, 0, 0, 255), batch=self.gui_batch)
        self.placeholder2 = BorderedRectangle(0, 0, 1200, 50, 10, border_color=(0, 0, 0, 255), batch=self.gui_batch)

        self.gui_frame.add_widget(self.load_file_button)

    def on_load_file_press(self):
        """
        Called when ever the load file button is pressed

        Will pass path of selected file to the controller, otherwise does nothing
        """
        chosen_file = askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.ogg")], title="Select File")

        if chosen_file != "":
            # TODO give file path to controller
            # 
            # self.figures = some_controller_function_that_doesnt_exist_yet(chosen_file)
            # self.images = list(map(figure_to_image, self.figures))
            pass

    def on_draw(self):
        """
        Overwrites on_draw method in pyglet.window.Window

        Defines a draw loop for the window
        """
        self.clear()
        self.gui_batch.draw()

