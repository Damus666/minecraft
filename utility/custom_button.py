from pygame_helper.helper_classes import ImageButton
from pygame_helper.helper_graphics import draw_image

class CustomButton(ImageButton):
    def __init__(self,pos_top,pos_center,path,scale,font,text,color="white"):
        ImageButton.__init__(self,pos_top[0],pos_top[1],None,path,False,scale,None,None)

        if pos_center:
            self.rect.center = pos_center
        self.text_img = font.render(text,True,color)
        self.text_rect = self.text_img.get_rect(center=self.rect.center)
        self.txt_img_2 = font.render(text,True,(60,60,60))

    def draw_check(self):
        action = ImageButton.draw(self)
        draw_image(self.txt_img_2,(self.text_rect.topleft[0]+3,self.text_rect.topleft[1]+3))
        draw_image(self.text_img,self.text_rect)
        return action