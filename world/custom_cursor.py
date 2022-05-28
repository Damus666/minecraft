from pygame_helper.pygame_helper import scale_image,load_image,draw_image
from utility.pixel_calculator import medium_calculator

class CustomCursor:
    def __init__(self):

        self.img = scale_image(load_image("assets/graphics/gui/cursor.png",True),medium_calculator(0.07))
        self.w = self.img.get_width()/2
        self.h = self.img.get_height()/2

    def draw(self,pos):

        draw_image(self.img,(pos[0]-self.w,pos[1]-self.h))