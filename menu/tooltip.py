import pygame
from utility.pixel_calculator import width_calculator,height_calculator,medium_calculator
from pygame_helper.pygame_helper import draw_image
from dict.data import blocks_data,items_data,tools_data

class Tooltip:
    def __init__(self):

        self.x_offset = width_calculator(20)
        self.y_offset = height_calculator(20)
        self.little_offset = height_calculator(3)
        
        self.name_font = pygame.font.Font("assets/fonts/regular.ttf",medium_calculator(30,True))
        self.tooltip_font = pygame.font.Font("assets/fonts/regular.ttf",medium_calculator(25,True))

        self.name_text = self.name_font.render("CAPS",True,"white")
        self.tooltip_text = self.tooltip_font.render("CAPS",True,"white")

        self.name_rect = self.name_text.get_rect(topleft=(self.x_offset,self.y_offset))
        self.tooltip_rect = self.name_text.get_rect(topleft=(self.x_offset,self.y_offset+self.name_text.get_height()+self.little_offset))

    def refresh_texts(self,name,tooltip):
        self.name_text = self.name_font.render(name,True,"white")
        self.tooltip_text = self.tooltip_font.render(tooltip,True,"white")

        self.name_rect = self.name_text.get_rect(topleft=(self.x_offset,self.y_offset))
        self.tooltip_rect = self.name_text.get_rect(topleft=(self.x_offset,self.y_offset+self.name_text.get_height()+self.little_offset))

    def change_tooltip(self,id,type,level=0):
        if type == "blocks":
            name = blocks_data[id]["name"].replace("_"," ").title()
            tooltip = blocks_data[id]["tooltip"] + " Press F3 for more."
            self.refresh_texts(name,tooltip)

        elif type == "items":
            name = items_data[id]["name"].replace("_"," ").title()
            tooltip = items_data[id]["tooltip"]
            if items_data[id]["key"] != None:
                tooltip += " ["+items_data[id]["key"].upper()+"]"+" "+items_data[id]["hotbar_tooltip"]+"."
            tooltip += " Press F3 for more."
            self.refresh_texts(name,tooltip)

        elif type == "tools":
            name = tools_data[id][level]["name"].replace("_"," ").title()
            tooltip = tools_data[id]["tooltip"]
            if tools_data[id]["start_tooltip"] != None:
                if tools_data[id][level]["message"] != None:
                    tooltip += tools_data[id]["start_tooltip"]+tools_data[id][level]["message"]+"."
            tooltip += " Press F3 for more."
            self.refresh_texts(name,tooltip)

    def draw(self):
        draw_image(self.name_text,self.name_rect)
        draw_image(self.tooltip_text,self.tooltip_rect)