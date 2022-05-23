from pygame_helper.pygame_helper import debug
import pygame
from dict.data import items_data, smeltables_types
from pygame_helper.helper_graphics import draw_image, get_window_surface
from item.item import ItemInstance
from utility.pixel_calculator import height_calculator, medium_calculator, width_calculator
from settings import FURNACE_SLOT_SIZE, ITEM_SIZE, BG_COLOR_COMPLETE,BG_COLOR,OUTLINE_COLOR,COMPLETE_OUTLINE_COLOR, STACK_SIZE, WIDTH,BLOCK_SIZE
from random import randint,choice

class FurnacesManager:
    def __init__(self,update_block_frame,top, add_item,free_pos_id,get_furnace_open, add_drop,get_scroll):
        
        self.furnaces = {}
        self.selected_id = 0
        self.font = pygame.font.Font("assets/fonts/regular.ttf",medium_calculator(20,True))

        self.top = top
        self.top_offset = height_calculator(120)
        self.can_click = True

        self.buggy_thing = medium_calculator(4)
        self.big_s_img = pygame.Surface((FURNACE_SLOT_SIZE,FURNACE_SLOT_SIZE))
        self.slot_img = pygame.Surface((FURNACE_SLOT_SIZE-self.buggy_thing,FURNACE_SLOT_SIZE-self.buggy_thing))
        self.slot_img.fill(BG_COLOR)
        self.slot_img.set_alpha(100)
        self.slot_img_complete = self.slot_img.copy()
        self.slot_img_complete.fill(BG_COLOR_COMPLETE)
        self.slot_img_complete.set_alpha(100)
        self.slot_offset = (FURNACE_SLOT_SIZE-ITEM_SIZE)/2
        self.little_offset = self.slot_offset/3
        self.intra_offset = width_calculator(15)

        self.r_width = medium_calculator(4,True)
        self.r_radius = medium_calculator(5,True)

        self.smelt_item_rect = self.big_s_img.get_rect(center = (WIDTH//2-FURNACE_SLOT_SIZE*2,self.top+self.top_offset+FURNACE_SLOT_SIZE/2))
        self.fuel_item_rect = self.big_s_img.get_rect(center = (WIDTH//2-FURNACE_SLOT_SIZE+self.intra_offset,self.top+self.top_offset+FURNACE_SLOT_SIZE/2))
        self.result_item_rect = self.big_s_img.get_rect(center = (WIDTH//2+FURNACE_SLOT_SIZE+self.intra_offset,self.top+self.top_offset+FURNACE_SLOT_SIZE/2))

        self.update_block_frame = update_block_frame
        self.add_item = add_item
        self.free_pos_id = free_pos_id
        self.get_furnace_open = get_furnace_open
        self.add_drop = add_drop
        self.get_scroll = get_scroll

    def place_items_in_furnace(self,pos,selected_slot):
        if self.get_furnace_open:
            item = selected_slot[0].item
            if self.smelt_item_rect.collidepoint(pos[0],pos[1]):
                if item.type == "items":
                    if items_data[item.id]["type"] in smeltables_types:
                        if self.furnaces[self.selected_id]["smelt_item"]["item"].id == item.id or self.furnaces[self.selected_id]["smelt_item"]["quantity"] == 0:
                            self.furnaces[self.selected_id]["smelt_item"]["item"] = item
                            self.furnaces[self.selected_id]["smelt_item"]["quantity"] += selected_slot[0].quantity
                            if self.furnaces[self.selected_id]["smelt_item"]["quantity"] > STACK_SIZE:
                                self.add_item(self.free_pos_id(item.id,item.type),item,self.furnaces[self.selected_id]["smelt_item"]["quantity"]-STACK_SIZE)
                            self.furnaces[self.selected_id]["is_active"]=True
                            self.update_block_frame(self.selected_id,1)
                            self.furnaces[self.selected_id]["smelt_item"]["quantity_img"] = self.font.render(str(self.furnaces[self.selected_id]["smelt_item"]["quantity"]),True,"white")
                            self.furnaces[self.selected_id]["fuel_item"]["quantity_img"] = self.font.render(str(self.furnaces[self.selected_id]["fuel_item"]["quantity"]),True,"white")
                            return True    

            if self.fuel_item_rect.collidepoint(pos[0],pos[1]):
                if item.type == "items":
                    if items_data[item.id]["type"] =="fuel":
                        if self.furnaces[self.selected_id]["fuel_item"]["item"].id == item.id or self.furnaces[self.selected_id]["fuel_item"]["quantity"] == 0:
                            self.furnaces[self.selected_id]["fuel_item"]["item"] = item
                            self.furnaces[self.selected_id]["fuel_item"]["quantity"] += selected_slot[0].quantity
                            if self.furnaces[self.selected_id]["fuel_item"]["quantity"] > STACK_SIZE:
                                self.add_item(self.free_pos_id(item.id,item.type),item,self.furnaces[self.selected_id]["fuel_item"]["quantity"]-STACK_SIZE)
                            self.furnaces[self.selected_id]["is_active"]=True
                            self.update_block_frame(self.selected_id,1)
                            self.furnaces[self.selected_id]["smelt_item"]["quantity_img"] = self.font.render(str(self.furnaces[self.selected_id]["smelt_item"]["quantity"]),True,"white")
                            self.furnaces[self.selected_id]["fuel_item"]["quantity_img"] = self.font.render(str(self.furnaces[self.selected_id]["fuel_item"]["quantity"]),True,"white")
                            return True   


            return False

    def update_furnaces(self):
        for id in self.furnaces.keys():
            furnace = self.furnaces[id]

            if furnace["is_active"]:
                if furnace["smelt_item"]["quantity"] == 0:
                    furnace["smelt_item"]["quantity_img"] = self.font.render(str(furnace["smelt_item"]["quantity"]),True,"white")
                    furnace["fuel_item"]["quantity_img"] = self.font.render(str(furnace["fuel_item"]["quantity"]),True,"white")
                    furnace["is_active"] = False
                    self.update_block_frame(id,0)
                elif furnace["fuel_item"]["quantity"] == 0:
                    furnace["fuel_item"]["quantity_img"] = self.font.render(str(furnace["fuel_item"]["quantity"]),True,"white")
                    furnace["smelt_item"]["quantity_img"] = self.font.render(str(furnace["smelt_item"]["quantity"]),True,"white")
                    furnace["is_active"] = False
                    self.update_block_frame(id,0)
                else:
                    if pygame.time.get_ticks() - furnace["last_smelt"] >= items_data[furnace["smelt_item"]["item"].id]["smelt_cooldown"]:
                        furnace["result_item"]["item"] = ItemInstance(items_data[furnace["smelt_item"]["item"].id]["result"],"items",True)
                        furnace["result_item"]["quantity"] += 1
                        furnace["smelt_points"] -= 1
                        furnace["smelt_item"]["quantity"]-=1
                        furnace["last_smelt"] = pygame.time.get_ticks()
                        furnace["smelt_item"]["quantity_img"] = self.font.render(str(furnace["smelt_item"]["quantity"]),True,"white")
                        furnace["result_item"]["quantity_img"] = self.font.render(str(furnace["result_item"]["quantity"]),True,"white")
                        if furnace["smelt_points"] <= 0:
                            furnace["fuel_item"]["quantity"] -= 1
                            furnace["smelt_points"] += items_data[furnace["fuel_item"]["item"].id]["fuel_points"]
                            furnace["fuel_item"]["quantity_img"] = self.font.render(str(furnace["fuel_item"]["quantity"]),True,"white")
                self.furnaces[id] = furnace

    def open_furnace(self,id):
        if not id in self.furnaces.keys():
            self.furnaces[id] = {"smelt_item":{"quantity":0,"item":ItemInstance(0,"items",True),"quantity_img":self.font.render("0",True,"white")},"fuel_item":{"quantity":0,"item":ItemInstance(6,"items",True),"quantity_img":self.font.render("0",True,"white")},"result_item":{"quantity":0,"item":ItemInstance(0,"items",True),"quantity_img":self.font.render("0",True,"white")},"smelt_points":0,"last_smelt":0,"is_active":False}
        self.selected_id = id        

    def passive_update(self):
        self.update_furnaces()

    def active_update(self,mouse):
        if mouse[0] and self.can_click:
            self.can_click = False
            pos = pygame.mouse.get_pos()
            self.slots_clicks(pos)

        if not mouse[0]:
            self.can_click = True

    def slots_clicks(self,pos):
        if self.smelt_item_rect.collidepoint(pos[0],pos[1]):
            if self.furnaces[self.selected_id]["smelt_item"]["quantity"] != 0:
                self.add_item(self.free_pos_id(self.furnaces[self.selected_id]["smelt_item"]["item"].id,self.furnaces[self.selected_id]["smelt_item"]["item"].type),self.furnaces[self.selected_id]["smelt_item"]["item"],self.furnaces[self.selected_id]["smelt_item"]["quantity"])
                self.furnaces[self.selected_id]["smelt_item"]["quantity"] = 0

        if self.fuel_item_rect.collidepoint(pos[0],pos[1]):
            if self.furnaces[self.selected_id]["fuel_item"]["quantity"] != 0:
                self.add_item(self.free_pos_id(self.furnaces[self.selected_id]["fuel_item"]["item"].id,self.furnaces[self.selected_id]["fuel_item"]["item"].type),self.furnaces[self.selected_id]["fuel_item"]["item"],self.furnaces[self.selected_id]["fuel_item"]["quantity"])
                self.furnaces[self.selected_id]["fuel_item"]["quantity"] = 0

        if self.result_item_rect.collidepoint(pos[0],pos[1]):
            if self.furnaces[self.selected_id]["result_item"]["quantity"] != 0:
                self.add_item(self.free_pos_id(self.furnaces[self.selected_id]["result_item"]["item"].id,self.furnaces[self.selected_id]["result_item"]["item"].type),self.furnaces[self.selected_id]["result_item"]["item"],self.furnaces[self.selected_id]["result_item"]["quantity"])
                self.furnaces[self.selected_id]["result_item"]["quantity"] = 0

    def delete_furnace(self,block):
        pos = (block["pos"][0]*BLOCK_SIZE-self.get_scroll().x+BLOCK_SIZE/2+randint(0,BLOCK_SIZE//4)*choice([1,-1]),block["pos"][1]*BLOCK_SIZE-self.get_scroll().y+BLOCK_SIZE/2)
        if self.furnaces[block["unique"]]["smelt_item"]["quantity"] != 0:
            pos = (block["pos"][0]*BLOCK_SIZE-self.get_scroll().x+BLOCK_SIZE/2+randint(0,BLOCK_SIZE//4)*choice([1,-1]),block["pos"][1]*BLOCK_SIZE-self.get_scroll().y+BLOCK_SIZE/2)
            self.add_drop(pos,self.furnaces[block["unique"]]["smelt_item"]["item"],self.furnaces[block["unique"]]["smelt_item"]["quantity"])

        if self.furnaces[block["unique"]]["fuel_item"]["quantity"] != 0:
            pos = (block["pos"][0]*BLOCK_SIZE-self.get_scroll().x+BLOCK_SIZE/2+randint(0,BLOCK_SIZE//4)*choice([1,-1]),block["pos"][1]*BLOCK_SIZE-self.get_scroll().y+BLOCK_SIZE/2)
            self.add_drop(pos,self.furnaces[block["unique"]]["fuel_item"]["item"],self.furnaces[block["unique"]]["fuel_item"]["quantity"])

        if self.furnaces[block["unique"]]["result_item"]["quantity"] != 0:
            pos = (block["pos"][0]*BLOCK_SIZE-self.get_scroll().x+BLOCK_SIZE/2+randint(0,BLOCK_SIZE//4)*choice([1,-1]),block["pos"][1]*BLOCK_SIZE-self.get_scroll().y+BLOCK_SIZE/2)
            self.add_drop(pos,self.furnaces[block["unique"]]["result_item"]["item"],self.furnaces[block["unique"]]["result_item"]["quantity"])

        self.furnaces.pop(block["unique"],None)

    def draw(self):
        if self.furnaces[self.selected_id]["smelt_item"]["quantity"]!=0:
            draw_image(self.slot_img_complete,(self.smelt_item_rect.topleft[0]+self.buggy_thing/2,self.smelt_item_rect.topleft[1]+self.buggy_thing/2))
            pygame.draw.rect(get_window_surface(),COMPLETE_OUTLINE_COLOR,self.smelt_item_rect,self.r_width,self.r_radius)
            draw_image(self.furnaces[self.selected_id]["smelt_item"]["item"].image,(self.smelt_item_rect.topleft[0]+self.slot_offset,self.smelt_item_rect.topleft[1]+self.slot_offset))
            draw_image(self.furnaces[self.selected_id]["smelt_item"]["quantity_img"],(self.smelt_item_rect.topleft[0]+self.little_offset,self.smelt_item_rect.topleft[1]+self.little_offset))
        else:
            draw_image(self.slot_img,(self.smelt_item_rect.topleft[0]+self.buggy_thing/2,self.smelt_item_rect.topleft[1]+self.buggy_thing/2))
            pygame.draw.rect(get_window_surface(),OUTLINE_COLOR,self.smelt_item_rect,self.r_width,self.r_radius) 
        
        if self.furnaces[self.selected_id]["fuel_item"]["quantity"]!=0:
            draw_image(self.slot_img_complete,(self.fuel_item_rect.topleft[0]+self.buggy_thing/2,self.fuel_item_rect.topleft[1]+self.buggy_thing/2))
            pygame.draw.rect(get_window_surface(),COMPLETE_OUTLINE_COLOR,self.fuel_item_rect,self.r_width,self.r_radius)
            draw_image(self.furnaces[self.selected_id]["fuel_item"]["item"].image,(self.fuel_item_rect.topleft[0]+self.slot_offset,self.fuel_item_rect.topleft[1]+self.slot_offset))
            draw_image(self.furnaces[self.selected_id]["fuel_item"]["quantity_img"],(self.fuel_item_rect.topleft[0]+self.little_offset,self.fuel_item_rect.topleft[1]+self.little_offset))
        else:
            draw_image(self.slot_img,(self.fuel_item_rect.topleft[0]+self.buggy_thing/2,self.fuel_item_rect.topleft[1]+self.buggy_thing/2))
            pygame.draw.rect(get_window_surface(),OUTLINE_COLOR,self.fuel_item_rect,self.r_width,self.r_radius)

        if self.furnaces[self.selected_id]["result_item"]["quantity"]!=0:
            draw_image(self.slot_img_complete,(self.result_item_rect.topleft[0]+self.buggy_thing/2,self.result_item_rect.topleft[1]+self.buggy_thing/2))
            pygame.draw.rect(get_window_surface(),COMPLETE_OUTLINE_COLOR,self.result_item_rect,self.r_width,self.r_radius)
            draw_image(self.furnaces[self.selected_id]["result_item"]["item"].image,(self.result_item_rect.topleft[0]+self.slot_offset,self.result_item_rect.topleft[1]+self.slot_offset))
            draw_image(self.furnaces[self.selected_id]["result_item"]["quantity_img"],(self.result_item_rect.topleft[0]+self.little_offset,self.result_item_rect.topleft[1]+self.little_offset))
        else:
            draw_image(self.slot_img,(self.result_item_rect.topleft[0]+self.buggy_thing/2,self.result_item_rect.topleft[1]+self.buggy_thing/2))
            pygame.draw.rect(get_window_surface(),OUTLINE_COLOR,self.result_item_rect,self.r_width,self.r_radius)