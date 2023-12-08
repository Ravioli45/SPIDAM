import pyglet
from pyglet.gui.widgets import PushButton
from pyglet.image import ImageData
from pyglet.shapes import BorderedRectangle
from pyglet.text import Label
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import pathlib
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
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

tall_rectangle = pyglet.resource.image("small_rectangle.png")
wide_rectangle = pyglet.resource.image("big_rectangle.png")

icon = pyglet.resource.image("speaker_icon.png")

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
        self.set_icon(icon)

        self.current_file = ""
        self.image_loaded: bool = False
        self.num_images: int = -1
        self.choosing_file: bool = False
        self.image_index: int = 0
        self.images: list[ImageData] = [ImageData(1, 1, "RGBA", "0000")]
        self.titles: list[str] = ["Waveform", 
                                  "Spectrogram",
                                  "Low Frequency",
                                  "Mid Frequency",
                                  "High Frequency",
                                  "Power Spectrum",
                                  ]
        self.rt_60s: list[float] = []

        self.gui_batch = pyglet.graphics.Batch()
        # frame for gui elements that are always present and never change
        self.static_gui_frame = pyglet.gui.Frame(self, cell_size=100)

        self.load_file_button = PushButton(0, 575, pressed=load_file_image, depressed=load_file_image, batch=self.gui_batch)
        self.load_file_button.set_handler('on_press', self._on_load_file_press)

        self.wide_rect = pyglet.sprite.Sprite(wide_rectangle, x=0, y=0, batch=self.gui_batch)
        self.tall_rect = pyglet.sprite.Sprite(tall_rectangle, x=300, y=575, batch=self.gui_batch)

        self.label_batch = pyglet.graphics.Batch()
        self.file_label = Label("File: ", "Calibri", font_size=25, color=(0, 0, 0, 255), x=15, y=12.5, width=100, height=20, batch=self.label_batch, dpi=100)
        self.time_label = Label("Time: ", "Calibri", font_size=25, color=(0, 0, 0, 255), x=600, y=12.5, width=100, height=20, batch=self.label_batch, dpi=100)
        self.rt60_label = Label("RT60: ", "Calibri", font_size=25, color=(0, 0, 0, 255), x=900, y=12.5, width=75, height=20, batch=self.label_batch, dpi=100)
        self.title_label = Label("", "Calibri", font_size=50, color=(0, 0, 0, 255), x=300, y=600, width=900, height=100, align='center', batch=self.label_batch, dpi=100)

        self.static_gui_frame.add_widget(self.load_file_button)

    def _on_load_file_press(self):
        """
        Called when ever the load file button is pressed

        Will pass path of selected file to the controller, otherwise does nothing
        """
        if not self.choosing_file:
            self.choosing_file = True
            chosen_file: str = askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")], title="Select File")
            self.choosing_file = False
            if chosen_file != "":
                chosen_path = pathlib.Path(chosen_file)
                self.current_file = chosen_path.name
                controller.loadFile(chosen_file)

    def on_draw(self):
        """
        Overwrites on_draw method in pyglet.window.Window

        Defines a draw loop for the window
        """
        self.clear()
        self.images[self.image_index].blit(0, 50)
        self.gui_batch.draw()
        self.label_batch.draw()

    def update_images(self, data: tuple[list[Figure], list[float], float] | None):
        # TODO improve update_images documentation
        """
        Called from model

        receives relevant information from the model and processes accordingly
        """
        if data is None:
            showerror("Error", "Unexpected error when opening file")
            return

        self.image_index = 0
        images = []
        for fig in data[0]:
            images.append(figure_to_image(fig))
        self.images = images
        self.num_images = len(images)

        self.rt_60s = data[1]

        self._update_time_label(data[2])
        self._update_rt60_label()
        self._update_title_label()
        self._update_file_label(self.current_file)

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
        self.image_index -= 1
        if self.image_index < 0:
            self.image_index = self.num_images - 1
        self._update_rt60_label()
        self._update_title_label()

    def _on_right_slider_press(self):
        """
        Switches the graph being displayed when the right slider button is pressed
        """
        self.image_index += 1
        if self.image_index >= self.num_images:
            self.image_index = 0
        self._update_rt60_label()
        self._update_title_label()

    def _update_time_label(self, time):
        self.time_label.text = f"Time: {time:0.2f}s"
    
    def _update_rt60_label(self):
        rt_index = self.image_index - 2
        if rt_index >= 0 and rt_index <= 2:
            self.rt60_label.text = f"RT60: {self.rt_60s[rt_index]:0.2e}s"
        else:
            self.rt60_label.text = "RT60: NA"

    def _update_title_label(self):
        self.title_label.text = self.titles[self.image_index]

    def _update_file_label(self, filename):
        self.file_label.text = f"File: {filename:.20}"
