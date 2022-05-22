import pygame
from pygame_helper.helper_graphics import draw_image, load_image, scale_image
from item.item import ItemInstance
from settings import GRAPHICS_PATH, GRAVITY_CONSTANT, BLOCK_SIZE, MOB_DAMAGE_COOLDOWN, SAFE_BLOCKS_NUM, ENTITY_DIR_COOLDOWN
from dict.data import entities_data, items_ids
from random import choice, randint
from pygame.transform import flip
from utility.pixel_calculator import width_calculator, height_calculator, medium_calculator


class AnimalEntity:
    def __init__(self, start_pos, type, add_drop,delete_entity,h=None,p_f=0):

        scale = medium_calculator(0.8)
        self.type = type
        self.ori_body_image_l = scale_image(load_image(
            f"{GRAPHICS_PATH}entities/{type}/body.png", True), scale)
        self.ori_body_image_r = flip(self.ori_body_image_l,True,False)
        self.body_img = self.ori_body_image_l
        self.rect = self.body_img.get_rect(center=start_pos)

        self.inf_height = 0
        self.inf_width = 0

        self.x_speed = entities_data[self.type]["speed"]
        self.gravity = 0

        self.is_standing = False
        self.is_moving = False
        self.first_time_land = False
        self.pixel_fell = p_f
        self.direction = -1

        self.max_health = entities_data[self.type]["health"]
        if h: self.health = h
        else: self.health = self.max_health

        self.last_change = 0

        self.width = self.body_img.get_width()
        self.height = self.body_img.get_height()

        self.add_drop = add_drop
        self.delete_entity = delete_entity

        self.drops = [{"id":items_ids["meat"],"type":"items","chances":100,"quantity":1,"more":[20,1]}]

        self.damage_hoverlay = scale_image(load_image(f"{GRAPHICS_PATH}gui/damage/mob.png",True),None,self.width+10+self.inf_width,self.height+10)
        self.damage_hoverlay.set_alpha(160)
        self.damage_rect = self.damage_hoverlay.get_rect(center=self.rect.center)
        self.is_damaging = False
        self.start_an = 0

        self.o_1 = medium_calculator(10)
        self.o_2 = medium_calculator(5)
        self.o_3 = medium_calculator(15)

    def damage(self, damage):
        self.health -= damage
        self.is_damaging = True
        self.start_an = pygame.time.get_ticks()
        if self.health <= 0:
            self.health = 0
            self.die()

    def draw_overlay(self):
        self.damage_rect.center = self.rect.center
        if pygame.time.get_ticks()-self.start_an >= MOB_DAMAGE_COOLDOWN:
            self.is_damaging = False
        draw_image(self.damage_hoverlay,self.damage_rect)

    def die(self):
        if self.drops:
            for d in self.drops:
                if d["chances"] != 0:
                    pos = (self.rect.centerx+randint(-self.ori_body_image_l.get_width()//2,self.ori_body_image_l.get_width()//2),self.rect.centery)
                    if randint(0,100) <= d["chances"]:
                        self.add_drop(pos,ItemInstance(d["id"],d["type"],True),d["quantity"])
                        if d["more"][0] != 0:
                            if randint(0,100) <= d["more"][0]:
                                self.add_drop(pos,ItemInstance(d["id"],d["type"],True),d["more"][1])

        self.delete_entity(self)

    def flip_image(self):
        if self.direction == -1:
            self.body_img = self.ori_body_image_l
        else:
            self.body_img = self.ori_body_image_r

    def fall(self,dt):
        self.gravity += GRAVITY_CONSTANT
        self.rect.y += self.gravity*dt

    def obstacles_collisions(self, obstacles):
        not_collided = 0
        near_blocks = 0

        if self.gravity != 0:
            if self.is_standing != False:
                self.is_standing = False
        if obstacles:
            for obstacle in obstacles:
                if obstacle[2]:
                    obs = obstacle[0]
                    r = self.rect.inflate(self.inf_width*2, self.inf_height*2)
                    inf_y = r.inflate(-self.width+self.o_1, 2)
                    if abs(obs.x-self.rect.x) <= BLOCK_SIZE*3 and abs(obs.y-self.rect.y) <= BLOCK_SIZE*3:
                        near_blocks += 1
                        if r.colliderect(obs):
                            if self.gravity >= 0:
                                if r.bottom > obs.top:
                                    if (r.bottom < obs.centery) or (self.rect.left > obs.left and self.rect.right < obs.right):
                                        if self.rect.left < obs.right - self.o_2 or self.rect.right > obs.left + self.o_2:
                                            self.rect.bottom = obs.top-self.inf_height
                                            self.is_standing = True
                                            self.gravity = 0
                                            if self.first_time_land:
                                                self.first_time_land = False
                                                blocks_fell = (
                                                    (self.pixel_fell)/BLOCK_SIZE)-SAFE_BLOCKS_NUM
                                                if int(blocks_fell) > 0:
                                                    self.damage(int(blocks_fell))
                                                self.pixel_fell = 0
                            if self.direction == 1:
                                if 0 < (obs.left+self.o_3)-(self.rect.right-self.o_3) < BLOCK_SIZE//2:
                                    if self.rect.right > obs.left:
                                        self.rect.right = obs.left
                                        self.direction = choice([0, -1])
                                        self.flip_image()
                            elif self.direction == -1:
                                if 0 < (self.rect.left+self.o_3)-(obs.right-self.o_3) < BLOCK_SIZE//2:
                                    if self.rect.left < obs.right:
                                        self.rect.left = obs.right
                                        self.direction = choice([0, 1])
                                        self.flip_image()
                        else:
                            if not inf_y.colliderect(obs):
                                not_collided += 1

        if not_collided == near_blocks:
            self.is_standing = False
            self.first_time_land = True

    def change_dir(self):
        if pygame.time.get_ticks()-self.last_change >= ENTITY_DIR_COOLDOWN:
            self.last_change = pygame.time.get_ticks()
            dir = choice([-1, 0, 1])
            flip = False
            if dir != 0:
                if dir != self.direction:
                    flip = True
            self.direction = dir
            if flip:
                self.flip_image()

    def move(self,dt):
        if self.direction != 0:
            self.rect.x += self.x_speed*self.direction*dt
            if not self.is_moving:
                self.is_moving = True
        else:
            if self.is_moving:
                self.is_moving = False

    def draw_body(self):
        draw_image(self.body_img, self.rect)

    def update(self, obstacles, dt):
        self.obstacles_collisions(obstacles)
        self.change_dir()
        self.move(dt)
        if not self.is_standing:
            self.fall(dt)

    def draw(self):
        """override"""

    def walk_animation(self,dt):
        """override"""
