from pygame_helper.pygame_helper import debug
from pygame_helper.helper_graphics import draw_image, load_image, scale_image
from item.item import ItemInstance
from settings import GRAPHICS_PATH, GRAVITY_CONSTANT, BLOCK_SIZE, MOB_DAMAGE_COOLDOWN, SAFE_BLOCKS_NUM,PLAYER_DAMAGE_COOLDOWN
from dict.data import entities_data, items_ids
from random import  randint
from pygame.transform import flip
import pygame
from utility.pixel_calculator import width_calculator, height_calculator, medium_calculator


class MonsterEntity:
    def __init__(self, start_pos, type, add_drop,delete_entity,get_p_rect,damage_player,h=None,p_f=0):

        scale = medium_calculator(0.8)
        self.type = type
        self.body_left = scale_image(load_image(
            f"{GRAPHICS_PATH}entities/{type}/body.png", True), scale)
        self.body_right = flip(self.body_left,True,False)
        self.head_left = scale_image(load_image(
            f"{GRAPHICS_PATH}entities/{type}/head.png", True), scale)
        self.head_right = flip(self.head_left,True,False)
        self.ori_arm_img = scale_image(load_image(
            f"{GRAPHICS_PATH}entities/{type}/arm.png", True), scale)
        self.ori_leg_img = scale_image(load_image(
            f"{GRAPHICS_PATH}entities/{type}/leg.png", True), scale)
        self.left_arm = self.ori_arm_img
        self.right_arm = self.ori_arm_img
        self.left_leg = self.ori_leg_img
        self.right_leg = self.ori_leg_img
        self.head_img = self.head_left
        self.body_img = self.body_left
        self.rect = self.body_img.get_rect(center=start_pos)
        self.head_rect = self.head_img.get_rect(midbottom=self.rect.midtop)
        self.left_arm_r = self.left_arm.get_rect(midtop=self.rect.midtop)
        self.right_arm_r = self.right_arm.get_rect(midtop=self.rect.midtop)
        self.left_leg_r = self.left_leg.get_rect(midtop=self.rect.midbottom)
        self.right_arm_r = self.right_arm.get_rect(midtop=self.rect.midbottom)

        self.inf_height = self.left_leg.get_height()

        self.x_speed = entities_data[self.type]["speed"]
        self.gravity = 0

        self.is_standing = False
        self.is_moving = False
        self.first_time_land = False
        self.pixel_fell = p_f
        self.direction = -1
        self.can_jump = True
        self.jump_speed = medium_calculator(10,True)

        self.get_p_rect = get_p_rect
        self.damage_player = damage_player
        self.last_hit = 0

        self.max_health = entities_data[self.type]["health"]
        if h: self.health = h
        else: self.health = self.max_health

        self.width = self.body_img.get_width()
        self.height = self.body_img.get_height()
        self.r_offset = self.body_img.get_width()/4

        self.add_drop = add_drop
        self.delete_entity = delete_entity

        self.can_move_a = True
        self.can_move_d = True
        self.can_attack = True

        self.drops = [{"id":items_ids["meat"],"type":"items","chances":100,"quantity":1,"more":[50,1]}]

        self.damage_hoverlay = scale_image(load_image(f"{GRAPHICS_PATH}gui/damage/mob.png",True),None,self.width+10,self.height+self.inf_height+10)
        self.damage_hoverlay.set_alpha(160)
        self.damage_rect = self.damage_hoverlay.get_rect(center=self.rect.center)
        self.is_damaging = False
        self.start_an = 0

        self.last_check = 0
        self.check_cooldown = 0.85*1000

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

    def die(self,do_drop=True):
        if do_drop:
            if self.drops:
                for d in self.drops:
                    if d["chances"] != 0:
                        pos = (self.rect.centerx+randint(-self.body_left.get_width()//2,self.body_left.get_width()//2),self.rect.centery)
                        if randint(0,100) <= d["chances"]:
                            self.add_drop(pos,ItemInstance(d["id"],d["type"],True),d["quantity"])
                            if d["more"][0] != 0:
                                if randint(0,100) <= d["more"][0]:
                                    self.add_drop(pos,ItemInstance(d["id"],d["type"],True),d["more"][1])

        self.delete_entity(self)

    def flip_image(self):
        if self.direction == -1:
            self.body_img = self.body_left
            self.head_img = self.head_left
        else:
            self.body_img = self.body_right
            self.head_img = self.head_right

    def fall(self,dt):
        self.gravity += GRAVITY_CONSTANT
        self.rect.y += self.gravity*dt

    def obstacles_collisions(self, obstacles):
        not_collided = 0
        near_blocks = 0
        not_call_r = 0
        not_call_l = 0

        if self.gravity != 0:
            if self.is_standing != False:
                self.is_standing = False
        if obstacles:
            for obstacle in obstacles:
                if obstacle[2]:
                    obs = obstacle[0]
                    r = self.rect.inflate(0, self.inf_height*2)
                    inf_y = r.inflate(-self.width+self.o_1, 2)
                    inf_x = r.inflate(2,-self.height/3)
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
                                            self.can_jump = True
                                            if self.first_time_land:
                                                self.first_time_land = False
                                                blocks_fell = (
                                                    (self.pixel_fell)/BLOCK_SIZE)-SAFE_BLOCKS_NUM
                                                if int(blocks_fell) > 0:
                                                    self.damage(int(blocks_fell))
                                                self.pixel_fell = 0
                            elif self.gravity < 0:
                                if r.top < obs.bottom and r.top > obs.centery+15:
                                    self.rect.top = obs.bottom+self.inf_height
                                    self.is_standing = False
                                    self.gravity = 0
                            if self.direction == 1:
                                if 0 < (obs.left+self.o_3)-(self.rect.right-self.o_3) < BLOCK_SIZE//2:
                                    if self.rect.right > obs.left:
                                        self.rect.right = obs.left
                                        self.can_move_d = False
                                        self.can_attack = False
                                        if self.can_jump:
                                            self.jump()
                                        if r.bottom < obs.centery:
                                            self.rect.bottom = obs.top-self.inf_height-3
                            elif self.direction == -1:
                                if 0 < (self.rect.left+self.o_3)-(obs.right-self.o_3) < BLOCK_SIZE//2:
                                    if self.rect.left < obs.right:
                                        self.rect.left = obs.right
                                        self.can_move_a = False
                                        self.can_attack = False
                                        if self.can_jump:
                                            self.jump()
                                        if r.bottom < obs.centery:
                                            self.rect.bottom = obs.top-self.inf_height-3
                                        
                        else:
                            if not inf_y.colliderect(obs):
                                not_collided += 1
                            if not inf_x.colliderect(obs):
                                if self.direction == 1:
                                    not_call_r += 1
                                elif self.direction == -1:
                                    not_call_l += 1
                            else:
                                if self.can_jump:
                                    self.jump()

        if not_collided == near_blocks:
            self.is_standing = False
            self.first_time_land = True
        if not_call_l == near_blocks:
            self.can_move_a = True
            if not_call_l == not_call_r:
                self.can_attack = True
        if not_call_r == near_blocks:
            self.can_move_d = True

    def move(self,dt):
        if self.direction != 0:
            if self.direction == 1:
                if self.can_move_d:
                    self.rect.x += self.x_speed*self.direction*dt
                    self.is_moving = True
                    self.can_attack = True
                else:
                    if self.is_moving:
                        self.is_moving = False
            elif self.direction == -1:
                if self.can_move_a:
                    self.rect.x += self.x_speed*self.direction*dt
                    self.is_moving = True
                    self.can_attack = True
                else:
                    if self.is_moving:
                        self.is_moving = False
                        self.can_attack = True
        else:
            if self.is_moving:
                self.is_moving = False
                self.can_attack = True

    def jump(self):
        self.gravity -= self.jump_speed
        self.can_jump = False

    def draw_overlay(self):
        self.damage_rect.center = self.rect.center
        if pygame.time.get_ticks()-self.start_an >= MOB_DAMAGE_COOLDOWN:
            self.is_damaging = False
        draw_image(self.damage_hoverlay,self.damage_rect)

    def draw_body(self):
        draw_image(self.body_img, self.rect)

    def update(self, obstacles, dt):
        self.obstacles_collisions(obstacles)
        if not self.is_standing:
            self.fall(dt)
        self.move(dt)
        if pygame.time.get_ticks()-self.last_check >= self.check_cooldown:
            self.target_player()
            self.last_check = pygame.time.get_ticks()

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
        if self.can_attack:
            if abs(self.rect.centerx-self.get_p_rect().centerx) <= entities_data[self.type]["attack_range"]*BLOCK_SIZE:
                if abs(self.rect.centery-self.get_p_rect().centery) <= entities_data[self.type]["attack_range"]*BLOCK_SIZE:
                    if pygame.time.get_ticks()-self.last_hit >= entities_data[self.type]["attack_cooldown"]:
                        self.last_hit = pygame.time.get_ticks()
                        self.damage_player(entities_data[self.type]["attack_damage"])

    def draw(self):
        """override"""

    def walk_animation(self,dt):
        """override"""