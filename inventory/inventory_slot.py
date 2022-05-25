from pygame_helper.helper_graphics import draw_image, get_window_surface
import pygame
from settings import MAX_DUR_WIDTH, DUR_HEIGHT, DUR_BG_COLOR, ITEM_SIZE, SLOT_OFFSET
from dict.data import tools_data

from utility.pixel_calculator import height_calculator

quantity_font = pygame.font.Font("assets/fonts/regular.ttf",height_calculator(16,True))

class InventorySlot:
    def __init__(self):

        self.empty = True
        self.item = None
        self.quantity = 0
        self.selected = False

        self.quantity_img = quantity_font.render(str(self.quantity),True,"black")

        self.durability_bg_rect = pygame.Rect(0,0,MAX_DUR_WIDTH,DUR_HEIGHT)
        self.durability_rect = pygame.Rect(0,0,MAX_DUR_WIDTH,DUR_HEIGHT)
        self.color = "green"
        self.last_check = 0

    def draw_item(self,x,y,offset):
        if not self.empty:
            draw_image(self.item.image,(x+offset//2+2,y+offset//2+2))
            if self.item.is_stackable:
                pygame.draw.rect(get_window_surface(),"white",pygame.Rect(x+offset-offset/2,y+offset-offset/2,self.quantity_img.get_width()+offset/2,self.quantity_img.get_height()),0,3)
                draw_image(self.quantity_img,(x+offset-offset/4,y+offset-offset/2))
            else:
                if self.item.type == "tools":
                    self.durability_bg_rect.topleft = (x+SLOT_OFFSET//2,y+ITEM_SIZE+SLOT_OFFSET//2)
                    self.durability_rect.topleft = (x+SLOT_OFFSET//2,y+ITEM_SIZE+SLOT_OFFSET//2)
                    self.durability_rect.width = (MAX_DUR_WIDTH*self.item.durability)/tools_data[self.item.id][self.item.level]["durability"]
                    pygame.draw.rect(pygame.display.get_surface(),DUR_BG_COLOR,self.durability_bg_rect)
                    pygame.draw.rect(pygame.display.get_surface(),self.color,self.durability_rect)
                    if pygame.time.get_ticks()-self.last_check >= 3000:
                        max_dur = tools_data[self.item.id][self.item.level]["durability"]
                        if self.item.durability <= max_dur/5:
                            self.color = "red"
                        elif self.item.durability <= max_dur-(max_dur/5)*3:
                            self.color = "orange"
                        elif self.item.durability <= max_dur-(max_dur/5)*2:
                            self.color = "yellow"
                        elif self.item.durability <= max_dur-max_dur/5:
                            self.color = "greenyellow"
                        else:
                            self.color = "green"
                        self.last_check = pygame.time.get_ticks()

    def refresh_quantity_img(self):
        self.quantity_img = quantity_font.render(str(self.quantity),True,"black")

    def refresh_durability(self):
        pass

    def __copy__(self):
        copy = InventorySlot()
        copy.empty = False
        copy.quantity = self.quantity
        copy.item = self.item
        return copy