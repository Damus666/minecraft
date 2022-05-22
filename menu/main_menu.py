import json
import pygame
from settings import GRAPHICS_PATH, WIDTH, HEIGHT, BG_CHANGE_COOLDOWN
from pygame_helper.helper_classes import ImageButton
import pygame.font as pfont
from pygame_helper.helper_graphics import draw_image, load_image, scale_image
from random import randint
from utility.custom_button import CustomButton
from menu.menu_card import MenuCard
from utility.pixel_calculator import height_calculator, width_calculator, medium_calculator

class MainMenu:
    def __init__(self,screen, quit,play_world,delete_world,new_world):
        self.screen = screen
        self.quit = quit

        self.is_selecting_world = False
        self.empty_button_path = f"{GRAPHICS_PATH}gui/buttons/empty_button.png"
        self.size = medium_calculator(30,True)
        self.button_font = pfont.Font("assets/fonts/regular.ttf",self.size)
        self.button_scale = medium_calculator(2.5)
        self.bgs = []
        self.bg_num = 6
        self.bg_index = randint(0,self.bg_num-1)
        self.load_bgs()

        self.last_change = 0
        self.change_cool = BG_CHANGE_COOLDOWN

        self.title_img = scale_image(load_image(f"{GRAPHICS_PATH}gui/title.png",True),medium_calculator(2.5))
        self.title_rect = self.title_img.get_rect(center=(WIDTH//2,HEIGHT//2-height_calculator(250)))

        self.load_buttons()

        self.offset = height_calculator(30)
        self.middle_y = (self.new_world_button.rect.top+self.back_button.rect.bottom)//2
        self.middle_x = self.back_button.rect.midbottom[0]
        self.card_height = self.new_world_button.rect.top-self.back_button.rect.bottom-self.offset*2
        self.card_width = medium_calculator(550)

        self.cards = []
        self.world_index = 0

        self.left_arrow_button = ImageButton(0,0,None,f"{GRAPHICS_PATH}gui/left_arrow.png",scale=self.button_scale)
        self.right_arrow_button = ImageButton(WIDTH//2+self.card_width//2+self.offset,self.middle_y,None,f"{GRAPHICS_PATH}gui/right_arrow.png",scale=self.button_scale)
        self.left_arrow_button.rect.center = (WIDTH//2-self.card_width//2-self.offset,self.middle_y)
        self.right_arrow_button.rect.center = (WIDTH//2+self.card_width//2+self.offset,self.middle_y)

        self.new_world = new_world
        self.delete_world = delete_world
        self.play_world = play_world

        self.can_back = False
        self.load_cards()

    def save_cards(self):
        try:
            dict = {"cards":[{"id":card.world_id,"name":card.name}for card in self.cards]}
            with open("data/worlds/list.json","w") as l_file:
                json.dump(dict,l_file)
        except:pass

    def load_cards(self):
        try:
            with open("data/worlds/list.json","r") as l_file:
                dict = json.load(l_file)
                for card in dict["cards"]:
                    c = MenuCard(self.card_height,self.card_width,self.middle_x,self.middle_y,card["id"],self.button_font,self.size,self.button_scale,self.play_world,self.delete_world_f)
                    c.name = card["name"]
                    c.input.text = card["name"]
                    c.input.txt_surface = c.input.font.render(c.input.text, True, c.input.color)
                    self.cards.append(c)
        except:
            self.save_cards()

    def delete_world_f(self, id):
        for c in self.cards:
            if c.world_id == id:
                self.cards.remove(c)
                break
        self.delete_world(id)
        if self.world_index > 0:
            self.world_index-=1
        if self.cards:
            self.cards[self.world_index].delet_button.clicked = True

    def new_world_f(self):
        id = self.new_world()
        card = MenuCard(self.card_height,self.card_width,self.middle_x,self.middle_y,id,self.button_font,self.size,self.button_scale,self.play_world,self.delete_world_f)
        self.cards.append(card)
        self.world_index = len(self.cards)-1
        self.save_cards()

    def load_buttons(self):
        self.play_button = CustomButton((0,0),(WIDTH//2,HEIGHT//2),self.empty_button_path,self.button_scale,self.button_font,"Play")
        self.quit_button = CustomButton((0,0),(WIDTH//2,HEIGHT//2+height_calculator(100)),self.empty_button_path,self.button_scale,self.button_font,"Quit")
        self.new_world_button = CustomButton((0,0),(WIDTH//2,HEIGHT-height_calculator(100)),self.empty_button_path,self.button_scale,self.button_font,"New World")
        self.back_button = CustomButton((0,0),(WIDTH//2,HEIGHT//2),self.empty_button_path,self.button_scale,self.button_font,"Back")

    def load_bgs(self):
        for i in range(0,self.bg_num):
            bg = scale_image(load_image(f"{GRAPHICS_PATH}bgs/{i}.png"),None,WIDTH,HEIGHT)
            self.bgs.append(bg)

    def change_bg(self):
        if pygame.time.get_ticks()-self.last_change >= self.change_cool:
            self.last_change = pygame.time.get_ticks()
            self.bg_index = randint(0,self.bg_num-1)

    def change_card(self,dir):
        if dir > 0:
            if self.world_index < len(self.cards)-1:
                self.world_index += 1*dir
        else:
            if self.world_index > 0:
                self.world_index += 1*dir

    def input_event(self,e):
        if self.cards:
            self.cards[self.world_index].event(e)

    def button_actions(self):
        if self.is_selecting_world == False:
            if self.quit_button.draw_check():
                self.save_cards()
                self.quit()
            if self.play_button.draw_check():
                self.is_selecting_world = True
                self.back_button.clicked = True
        else:
            if self.new_world_button.draw_check():
                self.new_world_f()
            if self.back_button.draw_check():
                self.is_selecting_world = False
            if len(self.cards) > 1:
                if self.left_arrow_button.draw():
                    self.change_card(-1)
                if self.right_arrow_button.draw():
                    self.change_card(1)
            if self.cards:
                self.cards[self.world_index].draw_update()

    def draw_update(self):
        draw_image(self.bgs[self.bg_index],(0,0))

        self.button_actions()

        draw_image(self.title_img,self.title_rect)

        # update
        self.change_bg()
