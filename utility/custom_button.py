from pygame_helper.helper_classes import ImageButton
from pygame_helper.helper_graphics import draw_image

from utility.pixel_calculator import width_calculator

class CustomButton(ImageButton):
    def __init__(self,pos_top,pos_center,path,scale,font,text=False,color="white",width=None,height=None,convert=False):
        ImageButton.__init__(self,pos_top[0],pos_top[1],None,path,convert,scale,width,height)

        if pos_center:
            self.rect.center = pos_center
        if text != None:
            self.text_img = font.render(text,True,color)
            self.text_rect = self.text_img.get_rect(center=self.rect.center)
            self.txt_img_2 = font.render(text,True,(60,60,60))
        self.offset = width_calculator(3)

    def draw_check(self):
        action = ImageButton.draw(self)
        draw_image(self.txt_img_2,(self.text_rect.topleft[0]+self.offset,self.text_rect.topleft[1]+self.offset))
        draw_image(self.text_img,self.text_rect)
        return action