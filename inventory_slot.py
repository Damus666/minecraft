from pygame_helper.helper_graphics import draw_image, get_window_surface
import pygame

quantity_font = pygame.font.Font("assets/fonts/regular.ttf",16)

class InventorySlot:
    def __init__(self):

        self.empty = True
        self.item = None
        self.quantity = 0
        self.selected = False

        self.quantity_img = quantity_font.render(str(self.quantity),False,"black")

    def draw_item(self,x,y,offset):
        if not self.empty:
            draw_image(self.item.image,(x+offset//2+2,y+offset//2+2))
            if self.item.is_stackable:
                pygame.draw.rect(get_window_surface(),"white",pygame.Rect(x+offset-offset/2,y+offset-offset/2,self.quantity_img.get_width()+offset/2,self.quantity_img.get_height()),0,3)
                draw_image(self.quantity_img,(x+offset-offset/4,y+offset-offset/2))

    def refresh_quantity_img(self):
        self.quantity_img = quantity_font.render(str(self.quantity),False,"black")

    def refresh_durability(self):
        pass

    def __copy__(self):
        copy = InventorySlot()
        copy.empty = False
        copy.quantity = self.quantity
        copy.item = self.item
        return copy