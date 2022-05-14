import pygame
from settings import MAX_HEALTH, MAX_HUNGER, GRAPHICS_PATH, HEALTH_REGEN_COOLDOWN,ITEM_SIZE,SLOT_OFFSET_H, HUNGER_DECREASE_COOLDOWN
from pygame_helper.helper_graphics import draw_image,scale_image,load_image

class Statistics:
    def __init__(self,top_hotbar_y,left_hotbar_x,hotbar_lenght,trigger_death):

        self.bottom_y = top_hotbar_y
        self.left_x = left_hotbar_x
        self.offset = 3
        self.lenght = hotbar_lenght

        self.max_health = MAX_HEALTH
        self.player_health = 20

        self.max_hunger = MAX_HUNGER
        self.player_hunger = self.max_hunger

        self.item_size = ((hotbar_lenght-SLOT_OFFSET_H*1.5-ITEM_SIZE*1.5)//2)/(self.max_health//2)

        self.half_heart_img = scale_image(load_image(f"{GRAPHICS_PATH}gui/half_heart.png",True),None,self.item_size,self.item_size)
        self.full_heart_img = scale_image(load_image(f"{GRAPHICS_PATH}gui/full_heart.png",True),None,self.item_size,self.item_size)
        self.empty_heart_img = scale_image(load_image(f"{GRAPHICS_PATH}gui/empty_heart.png",True),None,self.item_size,self.item_size)

        self.half_hunger_img = scale_image(load_image(f"{GRAPHICS_PATH}gui/half_hunger.png",True),None,self.item_size,self.item_size)
        self.full_hunger_img = scale_image(load_image(f"{GRAPHICS_PATH}gui/full_hunger.png",True),None,self.item_size,self.item_size)
        self.empty_hunger_img = scale_image(load_image(f"{GRAPHICS_PATH}gui/empty_hunger.png",True),None,self.item_size,self.item_size)

        self.last_regen = 0
        self.regen_cooldown = HEALTH_REGEN_COOLDOWN

        self.last_decrease = 0
        self.decrease_cooldown = HUNGER_DECREASE_COOLDOWN

        self.trigger_death = trigger_death

    def get_hunger(self):
        return self.player_hunger

    def cooldowns(self):
        if self.player_hunger == self.max_hunger:
            if self.player_health < self.max_health:
                if pygame.time.get_ticks()-self.last_regen >= self.regen_cooldown:
                    self.last_regen = pygame.time.get_ticks()
                    self.player_health += 1

        if self.player_hunger > 0:
            if pygame.time.get_ticks()-self.last_decrease >= self.decrease_cooldown:
                self.last_decrease = pygame.time.get_ticks()
                self.player_hunger -= 1
        else:
            if self.player_health > 0:
                if pygame.time.get_ticks()-self.last_decrease >= self.decrease_cooldown:
                    self.last_decrease = pygame.time.get_ticks()
                    self.damage_player(1)

    def update(self):
        self.cooldowns()

    def reset(self):
        self.player_health = self.max_health
        self.player_hunger = self.max_hunger
        self.last_decrease = 0
        self.last_regen = 0

    def damage_player(self,damage):
        self.player_health -= int(damage)
        if self.player_health <= 0:
            self.player_health = 0
            self.trigger_death()

    def draw(self):

        for i in range(self.max_health//2):
            draw_image(self.empty_heart_img,(self.left_x+i*self.item_size+i*self.offset,self.bottom_y-self.offset*2.5-self.item_size))
        for o in range(self.player_health//2):
            draw_image(self.full_heart_img,(self.left_x+o*self.item_size+o*self.offset,self.bottom_y-self.offset*2.5-self.item_size))
        if self.player_health%2 != 0:
            draw_image(self.half_heart_img,(self.left_x+(self.player_health//2)*self.item_size+(self.player_health//2)*self.offset,self.bottom_y-self.offset*2.5-self.item_size))

        for i in range(self.max_hunger//2):
            draw_image(self.empty_hunger_img,(self.left_x+self.lenght+SLOT_OFFSET_H-i*self.item_size-i*self.offset-self.offset*2,self.bottom_y-self.offset*2.5-self.item_size))
        for o in range(self.player_hunger//2):
            draw_image(self.full_hunger_img,(self.left_x+self.lenght+SLOT_OFFSET_H-o*self.item_size-o*self.offset-self.offset*2,self.bottom_y-self.offset*2.5-self.item_size))
        if self.player_hunger%2 != 0:
            draw_image(self.half_hunger_img,(self.left_x+self.lenght+SLOT_OFFSET_H-(self.player_hunger//2)*self.item_size-(self.player_hunger//2)*self.offset-self.offset*2,self.bottom_y-self.offset*2.5-self.item_size))