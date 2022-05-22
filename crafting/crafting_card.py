from settings import CRAFTING_CARD_WIDTH,CRAFTING_CARD_HEIGHT, CRAFTING_CARD_OFFSET, GRAPHICS_PATH, OUTLINE_COLOR,COMPLETE_OUTLINE_COLOR,BG_COLOR,BG_COLOR_COMPLETE
import pygame
from pygame_helper.pygame_helper import draw_image, get_window_surface, scale_image, load_image
from dict.data import block_ids
from utility.pixel_calculator import  medium_calculator, height_calculator

class RecipeCard:
    def __init__(self,type,final_item_id,recipe_list,amount, level=0):

        self.font = pygame.font.Font("assets/fonts/regular.ttf",height_calculator(20,True))

        self.type = type 
        self.final_item_id = final_item_id
        self.recipe_list = recipe_list
        self.level = level
        self.amount = amount

        self.width = CRAFTING_CARD_WIDTH
        self.height = CRAFTING_CARD_HEIGHT
        self.offset = CRAFTING_CARD_OFFSET
        self.l_offset = self.offset/1.2

        self.outline_color = OUTLINE_COLOR
        self.complete_outline_color = COMPLETE_OUTLINE_COLOR
        self.bg_color = BG_COLOR
        self.bg_has_color = BG_COLOR_COMPLETE

        self.bg = pygame.Surface((CRAFTING_CARD_WIDTH,CRAFTING_CARD_HEIGHT))
        self.bg_has = pygame.Surface((CRAFTING_CARD_WIDTH,CRAFTING_CARD_HEIGHT))
        self.smal_bg = pygame.Surface((CRAFTING_CARD_WIDTH+6,CRAFTING_CARD_HEIGHT+6))
        self.bg.fill(self.bg_color)
        self.bg.set_alpha(100)
        self.bg_has.fill(self.bg_has_color)
        self.bg_has.set_alpha(100)

        self.final_item_img_scale = self.height-self.offset-self.offset
        self.recipe_img_scale = self.final_item_img_scale// 3

        self.has_needed = False
        
        if self.type != "tools":
            st = str(self.final_item_id)
            if self.final_item_id == block_ids["furnace"]:
                st = f"{self.final_item_id}/0"
            self.final_item_img = scale_image(load_image(f"{GRAPHICS_PATH}{self.type}/{st}.png",True),None,self.final_item_img_scale,self.final_item_img_scale)
        else:
            self.final_item_img = scale_image(load_image(f"{GRAPHICS_PATH}{self.type}/{self.final_item_id}/{self.level}.png",True),None,self.final_item_img_scale,self.final_item_img_scale)

        self.final_img_width = self.final_item_img.get_width()
        self.recipes_data = self.load_recipe_images()

        self.amount_txt_img = self.font.render("x"+str(self.amount),True,"white")

        self.first_time = True
        self.rect = pygame.Rect(0,0,0,0)

        self.outline_size = medium_calculator(3,True)
        self.b_radius = medium_calculator(5,True)

    def load_recipe_images(self):
        recipes_list = []
        for recipe in self.recipe_list:
            type = recipe["item"]["type"]
            id = recipe["item"]["id"]
            img = scale_image(load_image(f"{GRAPHICS_PATH}{type}/{id}.png",True),None,self.recipe_img_scale,self.recipe_img_scale)
            need = recipe["quantity"]
            has = 0
            text_img = self.font.render(str(has)+"/"+str(need),True,"white")
            data = {"img":img,"need":need,"has":has,"text":text_img,"type":type,"id":id}
            recipes_list.append(data)

        return recipes_list

    def refresh_correct_items(self,items_player_has):
        has_all = 0
        for recipe in self.recipes_data:
            string = str(recipe["type"])+";"+str(recipe["id"])
            if items_player_has.get(string):
                recipe["has"] = items_player_has[string]
                if recipe["has"] >= recipe["need"]:
                    has_all += 1
            else:
                recipe["has"] = 0

        if has_all == len(self.recipes_data):
            self.has_needed = True
        else:
            self.has_needed = False

        self.refresh_recipes_text()

    def refresh_recipes_text(self):
        for r in self.recipes_data:
            color = "red"
            if r["has"] >= r["need"]:
                color = "white"
            if self.has_needed:
                color = "green"
            new_img = self.font.render(str(r["has"])+"/"+str(r["need"]),True,color)
            r["text"] = new_img

    def draw(self,topleft):
        if self.first_time:
            self.first_time = False
            self.rect = self.smal_bg.get_rect(topleft=(topleft[0]-3,topleft[1]-3))
        if self.has_needed:
            draw_image(self.bg_has,topleft)
        else:
            draw_image(self.bg,topleft)

        draw_image(self.final_item_img,(topleft[0]+self.offset,topleft[1]+self.offset))
        draw_image(self.amount_txt_img,(topleft[0]+self.offset,topleft[1]+self.offset))

        for index,r in enumerate(self.recipes_data):
            draw_image(r["img"],(topleft[0]+self.offset*2+self.final_img_width,topleft[1]+self.offset+index*self.recipe_img_scale+index*self.l_offset))
            draw_image(r["text"],(topleft[0]+self.offset*2+self.final_img_width+self.recipe_img_scale+self.l_offset,topleft[1]+self.offset+index*self.recipe_img_scale+index*self.l_offset))

        if not self.has_needed:
            pygame.draw.rect(get_window_surface(),self.outline_color,self.rect,self.outline_size,self.b_radius)
        else:
            pygame.draw.rect(get_window_surface(),self.complete_outline_color,self.rect,self.outline_size,self.b_radius)