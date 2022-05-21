import pygame
from dict.crafting_recipes import recipes
from crafting.crafting_card import RecipeCard
from item.item import ItemInstance
from settings import  CRAFTING_CARD_WIDTH
from utility.custom_button import CustomButton

class CraftingSystem:
    def __init__(self,left_pos,width,inv_bottom,get_inventory_slots,add_item,get_free_pos,remove_item):
        
        self.left = left_pos- CRAFTING_CARD_WIDTH-25
        self.width = width+CRAFTING_CARD_WIDTH*2+50
        self.top = inv_bottom+110

        self.get_inv_slots = get_inventory_slots
        self.add_item = add_item
        self.get_free_pos = get_free_pos
        self.remove_item = remove_item

        self.offset = 20
        self.can_click = True

        self.button_size = 50
        self.blocks_button = CustomButton((0,0),(self.left+self.width/2,self.top-60),"assets/graphics/gui/buttons/blocks.png",None,None,None,"white",self.button_size,self.button_size,True)
        self.items_button = CustomButton((0,0),(self.left+self.width/2-self.button_size-10,self.top-60),"assets/graphics/gui/buttons/items.png",None,None,None,"white",self.button_size,self.button_size,True)
        self.tools_button = CustomButton((0,0),(self.left+self.width/2+self.button_size+10,self.top-60),"assets/graphics/gui/buttons/tools.png",None,None,None,"white",self.button_size,self.button_size,True)

        self.sections = ["blocks","items","tools"]
        self.selected_section = 1

        self.cards = {"blocks":[],"items":[],"tools":[]}
        self.rects = {"blocks":[],"items":[],"tools":[]}

        self.load_cards()

    def refresh_correct_items(self):
        items_player_has = {}
        slots = self.get_inv_slots()
        for slot in slots.values():
            if slot.empty == False:
                string = str(slot.item.type)+";"+str(slot.item.id)
                if items_player_has.get(string):
                    items_player_has[string] += slot.quantity
                else:
                    items_player_has[string] = slot.quantity
        for section in self.sections:
            for card in self.cards[section]:
                card.refresh_correct_items(items_player_has)

    def load_cards(self):
        for section in self.sections:
            for index,recipe in enumerate(recipes[section].keys()):
                if section in ["blocks","items"]:
                    self.cards[section].append(RecipeCard(section,recipe,recipes[section][recipe]["recipe"],recipes[section][recipe]["amount"]))
                else:
                    for level in recipes[section][recipe].keys():
                        self.cards[section].append(RecipeCard(section,recipe,recipes[section][recipe][level],1,level))

    def update(self, mouse):
        if mouse[0] and self.can_click:
            self.can_click = False
            pos = pygame.mouse.get_pos()
            for card in self.cards[self.sections[self.selected_section]]:
                if card.rect.collidepoint(pos[0],pos[1]):
                    if card.has_needed:
                        self.add_item(self.get_free_pos(card.final_item_id,card.type),ItemInstance(card.final_item_id,card.type,True if card.type in ["blocks","items"] else False,card.level),card.amount)
                        for recipe in card.recipes_data:
                            self.remove_item(recipe["type"],recipe["id"],recipe["need"])
            self.refresh_correct_items()

        if not mouse[0]:
            self.can_click = True

    def draw(self):
        if self.blocks_button.draw():
            self.selected_section = 0
        if self.items_button.draw():
            self.selected_section = 1
        if self.tools_button.draw():
            self.selected_section = 2
        row = 0
        index = 0
        for card in self.cards[self.sections[self.selected_section]]:
            card.draw((self.left+self.offset*index+card.width*index,self.top+self.offset*row+card.height*row))
            index += 1
            if self.left+self.offset*index+card.width*index+card.width > self.left+self.width:
                row += 1
                index = 0