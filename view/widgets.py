from pyglet.gui.widgets import PushButton
from typing import Literal

def triangle_area(x1, y1, x2, y2, x3, y3):
    area = abs((x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))/2)
    return area

class SliderButton(PushButton):
    """
    Custom widget used for making slider buttons
    """
    def __init__(self, x: int, y: int, pressed, depressed, hover=None, batch=None, group=None, dir: Literal['left', 'right'] = 'left'):
        super().__init__(x, y, pressed, depressed, hover, batch, group)

        if dir == "left":
            self._x1, self._y1 = self._x, self._y + (self._height/2)
            self._x2, self._y2 = self._x + self._width, self._y + self._height
            self._x3, self._y3 = self._x + self.width, self._y
        elif dir == "right":
            self._x1, self._y1 = self._x, self._y
            self._x2, self._y2 = self.x, self._y + self._height
            self._x3, self._y3 = self._x+self._width, self._y + (self._height/2)
        else:
            raise ValueError("Invalid button direction")
        
        self.button_area = triangle_area(self._x1, self._y1, self._x2, self._y2, self._x3, self._y3)

    def _check_hit(self, x, y) -> bool:
        a1 = triangle_area(x, y, self._x2, self._y2, self._x3, self._y3)
        a2 = triangle_area(self._x1, self._y1, x, y, self._x3, self._y3)
        a3 = triangle_area(self._x1, self._y1, self._x2, self._y2, x, y)
        return self.button_area == (a1+a2+a3)