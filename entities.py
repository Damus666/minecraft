import pygame
from animal_entity import AnimalEntity
from monster_entity import MonsterEntity
from pygame.transform import rotate
from pygame_helper.helper_graphics import draw_image
from settings import BLOCK_SIZE
from data import entities_data, items_ids

class ZombieEntity(MonsterEntity):
    def __init__(self, start_pos, type, add_drop, delete_entity,get_p_rect,damage_player, h=None, p_f=0):
        super().__init__(start_pos, type, add_drop, delete_entity, h, p_f)

        self.leg_direction = pygame.Vector2((0,0))
        self.right_angle = 0
        self.left_angle = 0
        self.go_right = 1
        self.go_left = -1
        self.v = 3
        self.get_p_rect = get_p_rect
        self.damage_player = damage_player
        self.last_hit = 0
        self.arm_offset = self.body_img.get_height()//7
        self.drops = [{"id":items_ids["brown_fungus"],"type":"items","chances":100,"quantity":1,"more":[20,1]},{"id":items_ids["white_fungus"],"type":"items","chances":50,"quantity":1,"more":[10,1]}]

    def flip_image(self):
        super().flip_image()
        if self.direction == 1:
            self.left_arm = rotate(self.ori_arm_img,90)
            self.right_arm = rotate(self.ori_arm_img,90)
        else:
            self.left_arm = rotate(self.ori_arm_img,-90)
            self.right_arm = rotate(self.ori_arm_img,-90)

    def walk_animation(self):
        if self.is_moving:
            
            if self.right_angle > 0:
                self.leg_direction.x = 1
            else:
                self.leg_direction.x = -1
            self.leg_direction.y = self.leg_direction.x *-1

            if self.go_right == 1:
                if self.right_angle > 45:
                    self.go_right = -1
            elif self.go_right == -1:
                if self.right_angle < -45:
                    self.go_right = 1

            self.go_left = self.go_right *-1
            
            self.left_leg = rotate(self.ori_leg_img,self.left_angle)
            self.right_leg = rotate(self.ori_leg_img,self.right_angle)

            self.right_angle += self.v*self.go_right
            self.left_angle += self.v*self.go_left

    def draw(self):

        self.head_rect.midbottom = self.rect.midtop
        match self.direction:
            case 1:
                self.right_arm_r = self.right_arm.get_rect(topleft=(self.rect.left,self.rect.top+self.arm_offset))
                self.left_arm_r = self.left_arm.get_rect(topleft=self.rect.midtop)
            case -1:
                self.right_arm_r = self.right_arm.get_rect(topright=self.rect.midtop)
                self.left_arm_r = self.left_arm.get_rect(topright=(self.rect.right,self.rect.top+self.arm_offset))
            case 0:
                self.right_arm_r = self.right_arm.get_rect(midtop=self.rect.midtop)
                self.left_arm_r = self.left_arm.get_rect(midtop=self.rect.midtop)

        match self.leg_direction.x:
            case 1:
                self.right_leg_r = self.right_leg.get_rect(topleft=(self.rect.centerx-self.r_offset,self.rect.bottom))
            case -1:
                self.right_leg_r = self.right_leg.get_rect(topright=(self.rect.centerx+self.r_offset,self.rect.bottom))
            case 0:
                self.right_leg_r = self.right_leg.get_rect(midtop=self.rect.midbottom)
        match self.leg_direction.y:
            case 1:
                self.left_leg_r = self.left_leg.get_rect(topleft=(self.rect.centerx-self.r_offset,self.rect.bottom))
            case -1:
                self.left_leg_r = self.left_leg.get_rect(topright=(self.rect.centerx+self.r_offset,self.rect.bottom))
            case 0:
                self.left_leg_r = self.left_leg.get_rect(midtop=self.rect.midbottom)

        if self.direction == 1:
            draw_image(self.left_arm,self.left_arm_r)
            draw_image(self.left_leg,self.left_leg_r)
        else:
            draw_image(self.right_arm,self.right_arm_r)
            draw_image(self.right_leg,self.right_leg_r)
        draw_image(self.head_img,self.head_rect)
        self.draw_body()
        if self.direction ==1:
            draw_image(self.right_arm,self.right_arm_r)
            draw_image(self.right_leg,self.right_leg_r)
        else:
            draw_image(self.left_arm,self.left_arm_r)
            draw_image(self.left_leg,self.left_leg_r)

    def target_player(self):
        if abs(self.rect.centery-self.get_p_rect().centery) <= entities_data[self.type]["target_range"]*BLOCK_SIZE:
            if abs(self.rect.centerx-self.get_p_rect().centerx) <= entities_data[self.type]["target_range"]*BLOCK_SIZE:
                if self.rect.centerx-self.get_p_rect().centerx > 0 and abs(self.rect.centerx-self.get_p_rect().centerx) > 20:
                    if self.direction != -1:
                        self.direction = -1
                        self.flip_image()
                    self.attack_player()
                elif self.rect.centerx-self.get_p_rect().centerx < 0 and abs(self.rect.centerx-self.get_p_rect().centerx) > 20:
                    if self.direction != 1:
                        self.direction = 1
                        self.flip_image()
                    self.attack_player()
                else:
                    if self.direction != 0:
                        self.direction = 0
                    self.attack_player()
            else:
                if self.direction != 0:
                    self.direction = 0
        else:
            if self.direction != 0:
                self.direction = 0

    def attack_player(self):
        if abs(self.rect.centerx-self.get_p_rect().centerx) <= entities_data[self.type]["attack_range"]*BLOCK_SIZE:
            if pygame.time.get_ticks()-self.last_hit >= entities_data[self.type]["attack_cooldown"]:
                self.last_hit = pygame.time.get_ticks()
                self.damage_player(entities_data[self.type]["attack_damage"])

    def update(self, obstacles):
        super().update(obstacles)
        self.target_player()

class PorcupineEntity(AnimalEntity):
    def __init__(self,start_pos,type,add_drop,delete_entity,h=None,p_f=0):
        AnimalEntity.__init__(self,start_pos,type,add_drop,delete_entity,h,p_f)

    def draw(self):
        self.draw_body()