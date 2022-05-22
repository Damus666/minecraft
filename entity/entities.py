import pygame
from entity.animal_entity import AnimalEntity
from entity.monster_entity import MonsterEntity
from pygame.transform import rotate
from pygame_helper.helper_graphics import draw_image
from settings import BLOCK_SIZE
from dict.data import entities_data, items_ids

class SkeletonEntity(MonsterEntity):
    def __init__(self, start_pos, type, add_drop, delete_entity,get_p_rect,damage_player, h=None, p_f=0):
        super().__init__(start_pos, type, add_drop, delete_entity,get_p_rect,damage_player, h, p_f)

        self.leg_direction = pygame.Vector2((0,0))
        self.arm_direction = pygame.Vector2((0,0))
        self.right_angle = 0
        self.left_angle = 0
        self.go_right = 1
        self.go_left = -1
        self.v = 3
        
        self.drops = [{"id":items_ids["bone"],"type":"items","chances":100,"quantity":1,"more":[50,1]}]

    def walk_animation(self,dt):
        if self.is_moving:
            
            if self.right_angle > 0:
                self.leg_direction.x = 1
                self.arm_direction.x = 1
            else:
                self.leg_direction.x = -1
                self.arm_direction.x = -1
            self.leg_direction.y = self.leg_direction.x *-1
            self.arm_direction.y = self.arm_direction.x*-1

            if self.go_right == 1:
                if self.right_angle > 45:
                    self.go_right = -1
            elif self.go_right == -1:
                if self.right_angle < -45:
                    self.go_right = 1

            self.go_left = self.go_right *-1
            
            self.left_leg = rotate(self.ori_leg_img,self.left_angle)
            self.right_leg = rotate(self.ori_leg_img,self.right_angle)
            self.right_arm = rotate(self.ori_arm_img,self.right_angle)
            self.left_arm = rotate(self.ori_arm_img,self.left_angle)

            self.right_angle += self.v*self.go_right*dt
            self.left_angle += self.v*self.go_left*dt

    def draw(self):

        self.head_rect.midbottom = self.rect.midtop
        match self.arm_direction.x:
            case 1:
                self.right_arm_r = self.right_arm.get_rect(topleft=self.rect.midtop)
            case -1:
                self.right_arm_r = self.right_arm.get_rect(topright=self.rect.midtop)
            case 0:
                self.right_arm_r = self.right_arm.get_rect(midtop=self.rect.midtop)
        match self.arm_direction.y:
            case 1:
                self.left_arm_r = self.left_arm.get_rect(topleft=self.rect.midtop)
            case -1:
                self.left_arm_r = self.left_arm.get_rect(topright=self.rect.midtop)
            case 0:
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

        if self.is_damaging:
            self.draw_overlay()

class ZombieEntity(MonsterEntity):
    def __init__(self, start_pos, type, add_drop, delete_entity,get_p_rect,damage_player, h=None, p_f=0):
        super().__init__(start_pos, type, add_drop, delete_entity,get_p_rect,damage_player, h, p_f)

        self.leg_direction = pygame.Vector2((0,0))
        self.right_angle = 0
        self.left_angle = 0
        self.go_right = 1
        self.go_left = -1
        self.v = 3
        self.side = -1
        
        self.arm_offset = self.body_img.get_height()//7
        self.drops = [{"id":items_ids["brown_fungus"],"type":"items","chances":100,"quantity":1,"more":[20,1]},{"id":items_ids["white_fungus"],"type":"items","chances":50,"quantity":1,"more":[10,1]}]
        self.flip_image()

    def flip_image(self):
        super().flip_image()
        if self.direction == 1:
            self.left_arm = rotate(self.ori_arm_img,90)
            self.right_arm = rotate(self.ori_arm_img,90)
            self.side = 1
        else:
            self.left_arm = rotate(self.ori_arm_img,-90)
            self.right_arm = rotate(self.ori_arm_img,-90)
            self.side = -1

    def walk_animation(self,dt):
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

            self.right_angle += self.v*self.go_right*dt
            self.left_angle += self.v*self.go_left*dt

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
                if self.side == 1:
                    self.right_arm_r = self.right_arm.get_rect(topleft=(self.rect.left,self.rect.top+self.arm_offset))
                    self.left_arm_r = self.left_arm.get_rect(topleft=self.rect.midtop)
                elif self.side == -1:
                    self.right_arm_r = self.right_arm.get_rect(topright=self.rect.midtop)
                    self.left_arm_r = self.left_arm.get_rect(topright=(self.rect.right,self.rect.top+self.arm_offset))

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

        if self.is_damaging:
            self.draw_overlay()

class PorcupineEntity(AnimalEntity):
    def __init__(self,start_pos,type,add_drop,delete_entity,h=None,p_f=0):
        AnimalEntity.__init__(self,start_pos,type,add_drop,delete_entity,h,p_f)

    def draw(self):
        self.draw_body()
        if self.is_damaging:
            self.draw_overlay()