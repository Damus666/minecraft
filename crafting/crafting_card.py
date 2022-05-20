from settings import CRAFTING_CARD_WIDTH,CRAFTING_CARD_HEIGHT, CRAFTING_CARD_OFFSET
import pygame
from pygame_helper.pygame_helper import draw_image, get_window_surface, scale_image, load_image

class RecipeCard:
    def __init__(self,type,final_item_id,recipe_list, level=0):

        self.font = pygame.font.Font("assets/fonts/regular.ttf",20)

        self.type = type 
        self.final_item_id = final_item_id
        self.recipe_list = recipe_list
        self.level = level

        self.width = CRAFTING_CARD_WIDTH
        self.height = CRAFTING_CARD_HEIGHT
        self.offset = CRAFTING_CARD_OFFSET
        self.l_offset = self.offset/2

        self.outline_color = (155,155,155)
        self.bg_color = (30,30,30)

        self.bg = pygame.Surface((CRAFTING_CARD_WIDTH,CRAFTING_CARD_HEIGHT))
        self.bg.fill(self.bg_color)
        self.bg.set_alpha(100)

        self.final_item_img_scale = self.height-self.offset-self.offset
        self.recipe_img_scale = self.final_item_img_scale// 3
        self.final_img_width = self.final_item_img.get_width()

        if self.type != "tools":
            self.final_item_img = scale_image(load_image(f"assets/graphics/{self.type}/{self.final_item_id}.png",True),None,self.final_item_img_scale,self.final_item_img_scale)
        else:
            self.final_item_img = scale_image(load_image(f"assets/graphics/{self.type}/{self.final_item_id}/{self.level}.png",True),None,self.final_item_img_scale,self.final_item_img_scale)

        self.recipes_data = self.load_recipe_images()

    def load_recipe_images(self):
        recipes_list = []
        for recipe in self.recipe_list:
            type = recipe["item"]["type"]
            id = recipe["item"]["id"]
            img = scale_image(load_image(f"assets/graphics/{type}/{id}",True),None,self.recipe_img_scale,self.recipe_img_scale)
            need = recipe["quantity"]
            has = 0
            text_img = self.font.render(str(has)+"/"+str(need),True,"white")
            data = {"img":img,"need":need,"has":has,"text":text_img}
            recipes_list.append(data)

    def refresh_recipes_text(self):
        for r in self.recipe_list:
            new_img = self.font.render(str(r["has"])+"/"+str(r["need"]),True,"white")
            r["text"] = new_img

    def draw(self,topleft,rect):
        draw_image(self.bg,topleft)

        draw_image(self.final_item_img,(topleft[0]+self.offset,topleft[1]+self.offset))

        for index,r in enumerate(self.recipes_data):
            draw_image(r["img"],(self.offset*2+self.final_img_width,self.offset+index*self.recipe_img_scale+index*self.l_offset))
            draw_image(r["text"],(self.offset*2+self.final_img_width+self.recipe_img_scale+self.l_offset,self.offset+index*self.recipe_img_scale+index*self.l_offset))

        pygame.draw.rect(get_window_surface(),self.outline_color,rect,3,5)