import json
import pygame
from item.item import ItemInstance
from settings import ITEM_SIZE, SLOT_COLOR, SLOT_OFFSET, WIDTH,HEIGHT, INV_BG_COLOR, STACK_SIZE, BLOCK_SIZE
from pygame_helper.helper_graphics import draw_image, get_window_surface
from inventory.inventory_slot import InventorySlot
from random import randint,choice

class Inventory:
    def __init__(self,add_drop,get_p_data ):

        self.slots = {}
        self.slot_rects = {}

        self.rows = 4
        self.columns = 9
        
        self.y_offset = 0
        self.y_pos_special = -300

        self.slot_image = pygame.Surface((ITEM_SIZE+SLOT_OFFSET,ITEM_SIZE+SLOT_OFFSET))
        self.slot_image.fill((30,30,30))
        self.slot_image.set_alpha(100)

        self.bg_tint = pygame.Surface((WIDTH,HEIGHT))
        self.bg_tint.set_alpha(100)

        self.inv_offset = 30
        self.inv_sizes = ((self.columns)*(ITEM_SIZE+SLOT_OFFSET)+(SLOT_OFFSET*self.columns)+self.inv_offset-SLOT_OFFSET,(self.rows)*(ITEM_SIZE+SLOT_OFFSET)+(SLOT_OFFSET*self.rows)+self.inv_offset-SLOT_OFFSET)
        self.offset = [(WIDTH//2)-self.inv_sizes[0]//2,(HEIGHT//2)-self.inv_sizes[1]//2]
        self.inv_rect = pygame.Rect(self.offset[0]-self.inv_offset/2,self.offset[1]-self.inv_offset/2,self.inv_sizes[0]+4,self.inv_sizes[1]+4)

        self.can_click = True
        self.first_time_pressed = True
        self.selected_slot = []
        self.was_clicking = False

        self.add_drop = add_drop
        self.get_p_data = get_p_data

        self.init_slots()
        self.load_rects()

    def move_inventory(self,dir):
        self.y_offset += self.y_pos_special*dir
        self.load_rects()
        self.inv_rect.y += self.y_offset*dir

    def save_data(self,id):
        try:
            with open("data/worlds_data/"+id+"/inventory_data.json","w") as i_file:
                data = {}
                for s in self.slots.keys():
                    slot = self.slots[s]
                    if slot.empty:
                        data[s] = {"empty":slot.empty,"item":False,"quantity":slot.quantity,"sel":slot.selected,}
                    else:
                        data[s] = {"empty":slot.empty,"item":{"id":slot.item.id,"type":slot.item.type,"is_stackable":slot.item.is_stackable,"level":slot.item.level,"durability":slot.item.durability},"quantity":slot.quantity,"sel":slot.selected}
                json.dump(data,i_file)

        except:
            pass

    def load_data(self,id):
        #try:
            with open("data/worlds_data/"+id+"/inventory_data.json","r") as i_file:
                data = json.load(i_file)
                for s in data.keys():
                    slot = data[s]
                    if slot["empty"]:
                        self.slots[s].empty = True
                        self.slots[s].item = None
                        self.slots[s].quantity = slot["quantity"]
                    else:
                        self.slots[s].empty = False
                        self.slots[s].item = ItemInstance(slot["item"]["id"],slot["item"]["type"],slot["item"]["is_stackable"],slot["item"]["level"],slot["item"]["durability"])
                        self.slots[s].quantity = slot["quantity"]
                    self.slots[s].selected = slot["sel"]
                    self.slots[s].refresh_quantity_img()
        #except:
            #self.save_data(id)

    def get_first_line(self):
        slots = {}
        for x in range(self.columns):
            slots[str(x)+";0"] = self.slots[str(x)+";0"]
        return slots

    def load_rects(self):
        for y in range(self.rows):
            for x in range(self.columns):
                x_t= (ITEM_SIZE+SLOT_OFFSET)*x+self.offset[0]
                y_t= (ITEM_SIZE+SLOT_OFFSET)*y+self.offset[1]+self.y_offset
                rect = pygame.Rect(x_t+SLOT_OFFSET*x,y_t+SLOT_OFFSET*y,ITEM_SIZE+SLOT_OFFSET+4,ITEM_SIZE+SLOT_OFFSET+4)
                pos = str(x)+";"+str(y)
                self.slot_rects[pos] = rect

    def init_slots(self):
        for y in range(self.rows):
            for x in range(self.columns):
                self.slots[str(x)+";"+str(y)] = InventorySlot()

    def add_item(self,pos,item,quantity=1):
        if not self.slots[pos].empty:
            if item.is_stackable == True:
                if self.slots[pos].item.type == item.type:
                    if self.slots[pos].item.id == item.id:
                        if self.slots[pos].quantity < STACK_SIZE:
                            self.slots[pos].quantity += quantity
                            if self.slots[pos].quantity > STACK_SIZE:
                                self.add_item(self.get_free_pos_by_id(item.id,item.type),item,self.slots[pos].quantity-STACK_SIZE)
                                self.slots[pos].quantity = STACK_SIZE
                            self.slots[pos].refresh_quantity_img()
                            return True
        elif self.slots[pos].empty == True:
            self.slots[pos].item = item
            self.slots[pos].empty = False
            self.slots[pos].quantity = quantity
            self.slots[pos].refresh_quantity_img()
            return True
        else:
            return False

    def get_empty_slot_pos(self):
        for y in range(self.rows):
            for x in range(self.columns):
                if self.slots[str(x)+";"+str(y)].empty == True:
                    return str(x)+";"+str(y)
        return False

    def get_free_pos_by_id(self,id,type):
        free_pos = []
        for y in range(self.rows):
            for x in range(self.columns):
                if self.slots[str(x)+";"+str(y)].empty== False:
                    if self.slots[str(x)+";"+str(y)].item.type == type:
                        if self.slots[str(x)+";"+str(y)].item.id== id:
                            if self.slots[str(x)+";"+str(y)].item.is_stackable== True:
                                if self.slots[str(x)+";"+str(y)].quantity < STACK_SIZE:
                                    return str(x)+";"+str(y)
                elif self.slots[str(x)+";"+str(y)].empty == True:
                    free_pos.append(str(x)+";"+str(y))
        if free_pos:
            return free_pos[0]
        return False

    def render_slots(self):
        draw_image(self.bg_tint,(0,0))
        #pygame.draw.rect(get_window_surface(),"black",self.inv_rect,4,10)
        #pygame.draw.rect(get_window_surface(),INV_BG_COLOR,pygame.Rect(self.offset[0]-self.inv_offset/2+2,self.offset[1]-self.inv_offset/2+2,self.inv_sizes[0],self.inv_sizes[1]),0,10)

        for y in range(self.rows):
            for x in range(self.columns):
                x_t= (ITEM_SIZE+SLOT_OFFSET)*x+self.offset[0]
                y_t= (ITEM_SIZE+SLOT_OFFSET)*y+self.offset[1]+self.y_offset
                #pygame.draw.rect(get_window_surface(),"black",self.slot_rects[str(x)+";"+str(y)],2,5)
                draw_image(self.slot_image,(x_t+SLOT_OFFSET*x+2,y_t+SLOT_OFFSET*y+2))
                pygame.draw.rect(get_window_surface(),(200,200,200),self.slot_rects[str(x)+";"+str(y)],3,5)
                self.slots[str(x)+";"+str(y)].draw_item(x_t+SLOT_OFFSET*x,y_t+SLOT_OFFSET*y,SLOT_OFFSET)

    def get_collided_slot(self,posi):
        pos = None
        for rect_pos in self.slot_rects.keys():
            r = self.slot_rects[rect_pos]
            if r.collidepoint(posi[0],posi[1]):
                pos = rect_pos
        return pos

    def get_selected_slot(self,posi):
        pos = self.get_collided_slot(posi)

        if pos != None:
            slot = self.slots[pos]
            if slot.empty == False:
                self.selected_slot = [slot.__copy__(),pos]
                return True
            else:
                return False
        else:
            return False

    def place_selected_slot(self,posi):
        pos = self.get_collided_slot(posi)
        do_search = False
        do_swap = False

        if pos != None:
            if self.slots[pos].empty == True:
                self.slots[pos].empty = False
                self.slots[pos].item = self.selected_slot[0].item
                self.slots[pos].quantity = self.selected_slot[0].quantity
                self.slots[pos].refresh_quantity_img()
            elif self.slots[pos].item.is_stackable:
                if self.slots[pos].item.type == self.selected_slot[0].item.type:
                    if self.slots[pos].item.id == self.selected_slot[0].item.id:
                        if self.slots[pos].quantity < STACK_SIZE:
                            self.add_item(pos,self.selected_slot[0].item,self.selected_slot[0].quantity)
                        else: do_swap=True
                    else: do_swap = True
                else:
                    do_swap = True
            else:
                do_swap = True
        else:
            do_search = True
        
        if do_swap:
            poss = self.selected_slot[1]
            if self.slots[poss].empty == True:
                self.slots[poss].empty = False
                self.slots[poss].item = self.slots[pos].item
                self.slots[poss].quantity = self.slots[pos].quantity
                self.slots[pos].empty = False
                self.slots[pos].item = self.selected_slot[0].item
                self.slots[pos].quantity = self.selected_slot[0].quantity
                self.slots[pos].refresh_quantity_img()
                self.slots[poss].refresh_quantity_img()
            else:
                do_search = True
            
        if do_search:
            poss = self.selected_slot[1]
            if self.slots[poss].empty == True:
                self.slots[poss].empty = False
                self.slots[poss].item = self.selected_slot[0].item
                self.slots[poss].quantity = self.selected_slot[0].quantity
            else:
                pos = (self.get_p_data()[0][0] + BLOCK_SIZE*self.get_p_data()[1],self.get_p_data()[0][1])
                self.add_drop(pos,self.selected_slot[0].item,self.selected_slot[0].quantity)
        
    def input(self,mouse):
        pos = pygame.mouse.get_pos()

        if ((mouse[0]) and (not mouse[2])) or self.was_clicking:
            if (self.can_click):
                if self.inv_rect.collidepoint(pos[0],pos[1]) or self.first_time_pressed == False:
                    if self.first_time_pressed:
                        if self.get_selected_slot(pos) == True:
                            self.first_time_pressed = False
                            self.slots[self.selected_slot[1]].empty = True
                            self.slots[self.selected_slot[1]].quantity = 0
                            self.slots[self.selected_slot[1]].item = None
                            self.selected_slot[0].refresh_quantity_img()
                        else:
                            self.can_click = False
                            self.first_time_pressed = True
                            self.selected_slot = []
                    else:
                        draw_image(self.selected_slot[0].item.image,(pos[0]-ITEM_SIZE//2,pos[1]-ITEM_SIZE//2))
                        if self.selected_slot[0].item.is_stackable:
                            pygame.draw.rect(get_window_surface(),"white",pygame.Rect(pos[0]-ITEM_SIZE//2-2,pos[1]-ITEM_SIZE//2-2,self.selected_slot[0].quantity_img.get_width()+4,self.selected_slot[0].quantity_img.get_height()),0,3)
                            draw_image(self.selected_slot[0].quantity_img,(pos[0]-ITEM_SIZE//2,pos[1]-ITEM_SIZE//2-2))
                else:
                    self.can_click = False
            if self.was_clicking == False:
                self.was_clicking = True

        if (not mouse[0]):
            if self.first_time_pressed == False:
                if self.inv_rect.collidepoint(pos[0],pos[1]):
                    self.place_selected_slot(pos)
                else:
                    pos = (self.get_p_data()[0][0] + BLOCK_SIZE*self.get_p_data()[1],self.get_p_data()[0][1])
                    self.add_drop(pos,self.selected_slot[0].item,self.selected_slot[0].quantity)
                self.first_time_pressed = True
                self.selected_slot = []
            self.can_click = True
            self.was_clicking = False

    def drop_all(self):
        for y in range(self.rows):
            for x in range(self.columns):
                slot = self.slots[str(x)+";"+str(y)]
                if not slot.empty:
                    pos = (self.get_p_data()[0][0] +randint(-BLOCK_SIZE/2,BLOCK_SIZE/2)*choice([-1,1]),self.get_p_data()[0][1])
                    self.add_drop(pos,slot.item,slot.quantity)

    def clear(self):
        for y in range(self.rows):
            for x in range(self.columns):
                slot = self.slots[str(x)+";"+str(y)]
                if not slot.empty:
                    slot.empty = True
                    slot.item = None
                    slot.quantity = 1
                    slot.selected = False

    def update(self,mouse):
        self.input(mouse)

