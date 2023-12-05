import pyglet
from pyglet.gui.widgets import PushButton
from pyglet.image import ImageData
from pyglet.shapes import BorderedRectangle
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import pathlib
from tkinter.filedialog import askopenfilename
import controller
from .widgets import SliderButton

# telling pyglet where the assets folder is
assets = pathlib.Path(__file__).parents[1] / "assets"
pyglet.resource.path = [str(assets)]
pyglet.resource.reindex()

load_file_image = pyglet.resource.image("load_file_image.png")
left_slider_button = pyglet.resource.image("blue_slider.png")
left_slider_hover = pyglet.resource.image("blue_slider_hover.png")

right_slider_button = pyglet.resource.image("blue_slider.png", flip_x=True)
right_slider_button.anchor_x = 0
right_slider_hover = pyglet.resource.image("blue_slider_hover.png", flip_x=True)
right_slider_hover.anchor_x = 0

def figure_to_image(fig: Figure) -> ImageData:
    canvas = FigureCanvasAgg(fig)
    data, (width, height) = canvas.print_to_buffer()
    image = ImageData(width, height, "RGBA", data, -4*width)
    return image

class AppWindow(pyglet.window.Window):
    """
    The main window for the application

    Contains all relevant ui elements and functions for the view
    """
    def __init__(self):
        super().__init__(1200, 675, caption="Audio Analyzer")

        self.image_loaded: bool = False
        self.image_index: int = 0
        self.images: list[ImageData] = [ImageData(1, 1, "RGBA", "0000")]

        self.gui_batch = pyglet.graphics.Batch()
        self.static_gui_frame = pyglet.gui.Frame(self, cell_size=100)

        self.load_file_button = PushButton(0, 575, pressed=load_file_image, depressed=load_file_image, batch=self.gui_batch)
        self.load_file_button.set_handler('on_press', self._on_load_file_press)

        # TODO replace white rectangles with actual gui elements
        self.placeholder1 = BorderedRectangle(300, 575, 900, 100, 3, border_color=(0, 0, 0, 255), batch=self.gui_batch)
        self.placeholder2 = BorderedRectangle(0, 0, 1200, 50, 3, border_color=(0, 0, 0, 255), batch=self.gui_batch)

        self.static_gui_frame.add_widget(self.load_file_button)

    def _on_load_file_press(self):
        """
        Called when ever the load file button is pressed

        Will pass path of selected file to the controller, otherwise does nothing
        """
        chosen_file: str = askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")], title="Select File")

        if chosen_file != "":
            controller.loadFile(chosen_file)

    def on_draw(self):
        """
        Overwrites on_draw method in pyglet.window.Window

        Defines a draw loop for the window
        """
        self.clear()
        self.images[self.image_index].blit(0, 50)
        self.gui_batch.draw()

    def update_images(self, data):
        # TODO improve update_images documentation
        """
        Called from model

        receives relevant information from the model and processes accordingly
        """
        self.images[0] = figure_to_image(data)

        if not self.image_loaded:
            self._create_sliders()
            self.image_loaded = True
            

    def _create_sliders(self):
        """
        Creates slider buttons that will be used to switch between graphs
        """
        self.left_slider = SliderButton(10, 275, 
                                            pressed=left_slider_hover, 
                                            depressed=left_slider_button, 
                                            hover=left_slider_hover,
                                            batch=self.gui_batch,
                                            dir='left' 
                                    )
        self.right_slider = SliderButton(1115, 275, 
                                            pressed=right_slider_hover, 
                                            depressed=right_slider_button, 
                                            hover=right_slider_hover,
                                            batch=self.gui_batch, 
                                            dir='right'
                                        )
        self.slider_frame = pyglet.gui.Frame(self, cell_size=1200)
        self.left_slider.set_handler('on_press', self._on_left_slider_press)
        self.right_slider.set_handler('on_press', self._on_right_slider_press)
        self.slider_frame.add_widget(self.left_slider)
        self.slider_frame.add_widget(self.right_slider)

    def _on_left_slider_press(self):
        """
        Switches the graph being displayed when the left slider button is pressed
        """
        pass
    def _on_right_slider_press(self):
        """
        Switches the graph being displayed when the right slider button is pressed
        """
        pass