from pygame_helper.helper_graphics import load_image,scale_image,draw_image
from utility.input_box import InputBox
from utility.custom_button import CustomButton
from settings import GRAPHICS_PATH

class MenuCard:
    def __init__(self,height,width,middle_x,middle_y, id, font,f_s, scale, play_world, delete_self):
        
        self.world_id = id
        self.font = font
        self.name = "New World"

        self.card_img = scale_image(load_image("assets/graphics/gui/card_bg.png",True),None,width,height)
        self.card_rect = self.card_img.get_rect(center=(middle_x,middle_y))

        self.input_bg_img = scale_image(load_image("assets/graphics/gui/input_bg.png"),scale)
        self.offset = (self.card_img.get_width()-self.input_bg_img.get_width())//2
        self.input_pos = (self.card_rect.topleft[0]+self.offset,self.card_rect.topleft[1]+self.offset)

        self.play_button = CustomButton((self.input_pos[0],self.input_pos[1]+self.input_bg_img.get_height()+self.offset),False,f"{GRAPHICS_PATH}gui/buttons/empty_button.png",scale,self.font,"Play")
        self.delet_button = CustomButton((self.input_pos[0],self.card_rect.bottom-self.offset-self.input_bg_img.get_height()),False,f"{GRAPHICS_PATH}gui/buttons/empty_button.png",scale,self.font,"Delete")

        self.input = InputBox(self.input_pos[0],self.input_pos[1],self.input_bg_img.get_width(),self.input_bg_img.get_height(),self.change_name,font=self.font,f_s=f_s)

        self.play_world = play_world
        self.delete_self = delete_self

    def change_name(self):
        self.name = self.input.get_text()

    def event(self,e):
        self.input.handle_event(e)

    def draw_update(self):
        draw_image(self.card_img,self.card_rect)

        draw_image(self.input_bg_img,self.input_pos)

        if self.play_button.draw_check():
            self.play_world(self.world_id)
        if self.delet_button.draw_check():
            self.delete_self(self.world_id)

        self.input.draw()