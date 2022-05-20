from settings import ITEM_SIZE, SLOT_COLOR, WIDTH,HEIGHT, SLOT_OFFSET_H
from pygame_helper.helper_graphics import draw_image, get_window_surface
from inventory.inventory_slot import InventorySlot
import pygame

class Hotbar:
    def __init__(self,columns, get_first_line, change_s_item):

        self.slots = {}
        self.slot_rects = {}

        self.rows = 1
        self.columns = columns
        self.offset = [(WIDTH//2)-((self.columns*(ITEM_SIZE+SLOT_OFFSET_H)+(SLOT_OFFSET_H*self.columns)))//2,HEIGHT-100]
        self.s_off = 10
        self.selection_index = 0
        self.max_select = 9

        self.slot_image = pygame.Surface((ITEM_SIZE+SLOT_OFFSET_H,ITEM_SIZE+SLOT_OFFSET_H))
        self.slot_image_s = pygame.Surface((ITEM_SIZE+SLOT_OFFSET_H+self.s_off/2,ITEM_SIZE+SLOT_OFFSET_H+self.s_off/2))
        self.slot_image.fill((30,30,30))
        self.slot_image.set_alpha(100)
        self.slot_image_s.fill((100,100,100))
        self.slot_image_s.set_alpha(100)

        self.lenght = self.columns*((ITEM_SIZE+SLOT_OFFSET_H))+(ITEM_SIZE+SLOT_OFFSET_H)*2

        self.init_slots()
        self.load_rects()

        self.selected_slot = []
        self.get_first_line = get_first_line
        self.slots = get_first_line()
        self.can_press = True
        self.can_click = True
        self.change_selected_item = change_s_item

        self.slots[str(round(self.columns/2-0.1))+";0"].selected = True
        self.selection_index = round(self.columns/2-0.1)

    def get_selected(self):
        for x in range(self.columns):
            if self.slots[str(x)+";0"].selected == True:
                return self.slots[str(x)+";0"]

    def get_s_pos(self):
        for x in range(self.columns):
            if self.slots[str(x)+";0"].selected == True:
                return str(x)+";0"

    def load_rects(self):
        for y in range(self.rows):
            for x in range(self.columns):
                x_t= (ITEM_SIZE+SLOT_OFFSET_H)*x+self.offset[0]
                y_t= (ITEM_SIZE+SLOT_OFFSET_H)*y+self.offset[1]
                rect = pygame.Rect(x_t+SLOT_OFFSET_H*x,y_t+SLOT_OFFSET_H*y,ITEM_SIZE+SLOT_OFFSET_H+4,ITEM_SIZE+SLOT_OFFSET_H+4)
                pos = str(x)+";"+str(y)
                self.slot_rects[pos] = rect

    def init_slots(self):
        for y in range(self.rows):
            for x in range(self.columns):
                self.slots[str(x)+";"+str(y)] = InventorySlot()

    def render_slots(self):

        for y in range(self.rows):
            for x in range(self.columns):
                x_t= (ITEM_SIZE+SLOT_OFFSET_H)*x+self.offset[0]
                y_t= (ITEM_SIZE+SLOT_OFFSET_H)*y+self.offset[1]
                if self.slots[str(x)+";"+str(y)].selected == False:
                    draw_image(self.slot_image,(x_t+SLOT_OFFSET_H*x+2,y_t+SLOT_OFFSET_H*y+2))
                    pygame.draw.rect(get_window_surface(),(155,155,155),self.slot_rects[str(x)+";"+str(y)],3,5)
                else:
                    draw_image(self.slot_image_s,(x_t+SLOT_OFFSET_H*x-self.s_off/2+5,y_t+SLOT_OFFSET_H*y-self.s_off/2+5))
                    pygame.draw.rect(get_window_surface(),(255,255,255),pygame.Rect(x_t+SLOT_OFFSET_H*x-self.s_off/2,y_t+SLOT_OFFSET_H*y-self.s_off/2,ITEM_SIZE+SLOT_OFFSET_H+self.s_off,ITEM_SIZE+SLOT_OFFSET_H+self.s_off),5,5)
                self.slots[str(x)+";"+str(y)].draw_item(x_t+SLOT_OFFSET_H*x,y_t+SLOT_OFFSET_H*y,SLOT_OFFSET_H)

    def refresh(self):
        self.slots = self.get_first_line()

    def input(self):
        keys = pygame.key.get_pressed()
        changed = False

        if keys[pygame.K_1] and self.can_press:
            self.selection_index = 1-1
            changed = True
            self.can_press = False
        elif keys[pygame.K_2] and self.can_press:
            self.selection_index = 2-1
            changed = True
            self.can_press = False
        elif keys[pygame.K_3] and self.can_press:
            self.selection_index = 3-1
            changed = True
            self.can_press = False
        elif keys[pygame.K_4] and self.can_press:
            self.selection_index = 4-1
            changed = True
            self.can_press = False
        elif keys[pygame.K_5] and self.can_press:
            self.selection_index = 5-1
            changed = True
            self.can_press = False
        elif keys[pygame.K_6] and self.can_press:
            self.selection_index = 6-1
            changed = True
            self.can_press = False
        elif keys[pygame.K_7] and self.can_press:
            self.selection_index = 7-1
            changed = True
            self.can_press = False
        elif keys[pygame.K_8] and self.can_press:
            self.selection_index = 8-1
            changed = True
            self.can_press = False
        elif keys[pygame.K_9] and self.can_press:
            self.selection_index = 9-1
            changed = True
            self.can_press = False

        if (not keys[pygame.K_1]) and (not keys[pygame.K_2]) and (not keys[pygame.K_3]) and (not keys[pygame.K_4]) and (not keys[pygame.K_5]) and (not keys[pygame.K_6]) and (not keys[pygame.K_7]) and (not keys[pygame.K_8]) and (not keys[pygame.K_9]):
            self.can_press = True

        if changed:
            self.change_selection()

    def scroll_mousewheel(self,value):
        if abs(value) <= self.columns-1: 
            if value > 0:
                self.selection_index += value
                if self.selection_index > self.columns -1:
                    self.selection_index -= self.columns
            elif value < 0:
                self.selection_index += value
                if self.selection_index < 0:
                    self.selection_index += self.columns
            self.change_selection()

    def select_slot(self,posi):
        pos = self.get_collided_slot(posi)

        if pos:
            self.selection_index = int(pos[0])
            self.change_selection()

    def decrease_slot(self):
        slot = self.slots[self.get_s_pos()]
        if slot.quantity > 1:
            slot.quantity -= 1
            slot.refresh_quantity_img()
        else:
            slot.empty = True
            slot.item = None
            slot.quantity = 1
            slot.refresh_quantity_img()
            self.change_selected_item(None)
        
    def change_selection(self):
        for x in range(self.columns):
            if x == self.selection_index:
                self.slots[str(x)+";0"].selected = True
                if self.slots[str(x)+";0"].empty == True:
                    self.change_selected_item(None)
                else:
                    self.change_selected_item(self.slots[str(x)+";0"].item.__copy__())
            else:
                self.slots[str(x)+";0"].selected = False

    def get_collided_slot(self,posi):
        pos = None
        for rect_pos in self.slot_rects.keys():
            r = self.slot_rects[rect_pos]
            if r.collidepoint(posi[0],posi[1]):
                pos = rect_pos
        return pos

    def mouse_input(self,mouse):

        if mouse[0] and self.can_click:
            pos = pygame.mouse.get_pos()
            self.can_click = False
            self.select_slot(pos)

        if not mouse[0]:
            self.can_click = True

    def update(self,mouse):
        self.input()
        self.mouse_input(mouse)