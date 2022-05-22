import pygame as pg
from pygame_helper.helper_graphics import draw_image

from utility.pixel_calculator import height_calculator, width_calculator

pg.font.init()
COLOR_INACTIVE = pg.Color(200,200,200,255)
COLOR_ACTIVE = pg.Color('white')

class InputBox:

    def __init__(self, x, y, w, h,change_name, text='New World', font=None,f_s=None):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.width = w
        self.change_name = change_name
        self.max = self.width/f_s
        self.o_1 = width_calculator(10)
        self.o_2 = height_calculator(7)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            self.txt_surface = self.font.render(self.text, True, self.color)
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.change_name()
                else:
                    if not len(self.text) > self.max:
                        self.text += event.unicode
                        self.change_name()
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self):
        # Blit the text.
        draw_image(self.txt_surface, (self.rect.x+self.o_1, self.rect.y+self.o_2))
        # Blit the rect.
        #pg.draw.rect(screen, self.color, self.rect, 5)

    def get_text(self):
        return self.text