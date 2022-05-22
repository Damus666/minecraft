from pygame_helper.helper_graphics import draw_image, scale_image, load_image
from utility.pixel_calculator import medium_calculator, width_calculator, height_calculator
import pygame
from settings import WIDTH,DAY_DURATION,NIGHT_DURATION,GRAPHICS_PATH,HEIGHT, TRANSITION_DUR

class DayNightCycle:
    def __init__(self,kill_monsters,spawn_monsters):

        self.bg_img_0 = scale_image(load_image("assets/graphics/world_bg/0.png"),medium_calculator(1))
        self.bg_img_1 = scale_image(load_image("assets/graphics/world_bg/1.png"),medium_calculator(1))
        self.bg_img_2 = scale_image(load_image("assets/graphics/world_bg/2.png"),medium_calculator(1))
        self.bg_sizes = self.bg_img_0.get_width(), self.bg_img_0.get_height()

        self.sun_img = scale_image(load_image(f"{GRAPHICS_PATH}other/sun.png"),width_calculator(0.8))
        self.moon_img = scale_image(load_image(f"{GRAPHICS_PATH}other/moon.png"),width_calculator(0.8))
        self.celestial_height = height_calculator(200)
        self.celestial_default_left = -width_calculator(100)
        self.sun_x_pos = self.celestial_default_left
        self.moon_x_pos = self.celestial_default_left
        self.is_day = True
        self.sun_speed = WIDTH/DAY_DURATION
        self.moon_speed = WIDTH/NIGHT_DURATION
        self.night_tint = pygame.Surface((WIDTH,HEIGHT))
        self.night_tint.fill("blue")
        self.night_tint.set_alpha(0)
        self.max_night_alpha = 150
        self.alpha_multiplier = 1
        self.last_milli = 0
        self.alpha = 0
        self.is_in_transition = False
        self.transition_speed = self.max_night_alpha/TRANSITION_DUR

        self.range_x = int(WIDTH/self.bg_sizes[0])+1
        self.range_y = (int(HEIGHT/self.bg_sizes[1])+1)-2

        self.kill_monsters = kill_monsters
        self.spawn_monsters = spawn_monsters

    def draw_day_night(self):
        if self.night_tint.get_alpha() > 0:
            draw_image(self.night_tint,(0,0))

        if self.is_day:
            draw_image(self.sun_img,(self.sun_x_pos,self.celestial_height))
        else:
            draw_image(self.moon_img,(self.moon_x_pos,self.celestial_height))

    def transition(self):
        self.alpha += self.alpha_multiplier*self.transition_speed*(pygame.time.get_ticks()-self.last_milli)
        if self.alpha <= 0:
            self.alpha = 0
            self.is_in_transition = False
            self.kill_monsters()
        if self.alpha >= self.max_night_alpha:
            self.alpha = self.max_night_alpha
            self.is_in_transition = False
            self.spawn_monsters()
        self.night_tint.set_alpha(self.alpha)

    def update_day_night(self,dt):
        if self.is_in_transition:
            self.transition()

        if self.is_day:
            self.sun_x_pos+= self.sun_speed*dt*(pygame.time.get_ticks()-self.last_milli)
            if self.sun_x_pos > WIDTH+50:
                self.is_day = False
                self.sun_x_pos = self.celestial_default_left
                self.alpha_multiplier = 1
                self.is_in_transition = True
        else:
            self.moon_x_pos += self.moon_speed*dt*(pygame.time.get_ticks()-self.last_milli)
            if self.moon_x_pos > WIDTH+50:
                self.is_day = True
                self.moon_x_pos = self.celestial_default_left
                self.alpha_multiplier = -1
                self.is_in_transition = True

        self.last_milli = pygame.time.get_ticks()

    def draw_bg(self):
        for i in range(self.range_x):
            draw_image(self.bg_img_2,(i*self.bg_sizes[0],0-self.bg_sizes[1]/2.5))
            draw_image(self.bg_img_1,(i*self.bg_sizes[0],self.bg_sizes[1]-self.bg_sizes[1]/2.5-1))
            draw_image(self.bg_img_0,(i*self.bg_sizes[0],self.bg_sizes[1]*2-self.bg_sizes[1]/2.5-2))
            if self.range_y > 0:
                for o in range(self.range_y):
                    draw_image(self.bg_img_0,(i*self.bg_sizes[0],self.bg_sizes[1]*(o+2)-self.bg_sizes[1]/2.5-2))