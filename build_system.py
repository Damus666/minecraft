import pygame
from settings import PLAYER_BUILD_RANGE

class BuildSystem:
    def __init__(self,get_free_pos_rects, get_selected, add_block, get_current_unique,update_current_unique,decrease_slot,get_rect, get_p_pos):
        
        self.can_click = True
        self.block = None

        self.get_free_pos_rects = get_free_pos_rects
        self.get_selected = get_selected
        self.add_block = add_block
        self.get_current_unique = get_current_unique
        self.update_current_unique = update_current_unique
        self.decrease_slot = decrease_slot
        self.get_p_rect = get_rect
        self.get_p_pos = get_p_pos

    def get_free_pos_rect(self,pos):
        block = None

        for b in self.get_free_pos_rects():
            rect = b[0]
            if rect.collidepoint(pos[0],pos[1]):
                if not rect.colliderect(self.get_p_rect()):
                    if abs(rect.x-self.get_p_pos().x) <= PLAYER_BUILD_RANGE and abs(rect.y-self.get_p_pos().y) <= PLAYER_BUILD_RANGE:
                
                        block = b

        if block:
            self.block = block
            return True
        else:
            return False

    def input(self,mouse):
        pos = pygame.mouse.get_pos()
        
        if mouse[2] and not mouse[0]:
            if self.can_click:
                self.can_click = False
                if self.get_free_pos_rect(pos):
                    if self.get_selected().empty == False:
                        if self.get_selected().item.id < 60:
                            self.update_current_unique()
                            item = self.get_selected().item
                            self.add_block({"pos":self.block[1],"id":item.id,"collider":True,"frame":0,"unique":self.get_current_unique()})
                            self.decrease_slot()
                            self.block = None

        if not mouse[2]:
            self.can_click = True
            self.block = None

    def update(self,mouse):
        self.input(mouse)