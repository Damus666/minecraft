import pygame
from settings import BLOCK_DAMAGE, PLAYER_HIT_RANGE
from dict.data import tools_data

class CombatSystem:
    def __init__(self,get_entites,get_selected, get_p_rect, c_s_i,get_player_last_attack,player_attack):

        self.can_click = True
        
        self.get_entities = get_entites
        self.get_selected = get_selected
        self.get_p_rect = get_p_rect
        self.change_selected_item = c_s_i
        self.get_p_last_a = get_player_last_attack
        self.player_attack = player_attack

    def find_entity(self):
        pos = pygame.mouse.get_pos()

        if self.get_entities():
            for e in self.get_entities():
                if e.rect.collidepoint(pos[0],pos[1]):
                    if abs(e.rect.centerx-self.get_p_rect().centerx) <= PLAYER_HIT_RANGE and abs(e.rect.centery-self.get_p_rect().centery) <= PLAYER_HIT_RANGE:
                        return e

        return False

    def damage_entity(self,e):
        if self.get_selected().empty == True:
            e.damage(BLOCK_DAMAGE)
        else:
            if self.get_selected().item.type in ["blocks","items"]:
                e.damage(BLOCK_DAMAGE)
            else:
                if pygame.time.get_ticks()-self.get_p_last_a()>= tools_data[self.get_selected().item.id][self.get_selected().item.level]["attack_cooldown"]:
                    damage = tools_data[self.get_selected().item.id][self.get_selected().item.level]["damage"]
                    e.damage(damage)
                    self.get_selected().item.durability -= 1
                    if self.get_selected().item.durability <= 0:
                        self.get_selected().empty = True
                        self.get_selected().item = None
                        self.change_selected_item(None)
                    else:
                        self.get_selected().refresh_durability()
                    self.player_attack()

    def input(self,mouse):

        if mouse[0] and not mouse[2]:
            if self.can_click:
                self.can_click = False
                e = self.find_entity()
                if e:
                    self.damage_entity(e)

        if not mouse[0]:
            self.can_click = True

    def update(self,mouse):
        self.input(mouse)