from pygame_helper.helper_graphics import draw_image
from settings import GRAVITY_CONSTANT, BLOCK_SIZE, ITEM_SIZE

class Drop:
    def __init__(self,start_pos,item,quantity=1):

        self.item = item
        self.quantity = quantity
        self.rect = self.item.image.get_rect(center=start_pos)

        self.is_standing = False
        self.gravity = 0
        self.offset = 0
        self.first_time = True

    def draw(self):
        draw_image(self.item.image,self.rect)

    def collisions(self,rects):
        near = 0
        not_coll = 0
        if rects:
            for r in rects:
                rect = r[0]
                if abs(rect.x-self.rect.x) <= BLOCK_SIZE and abs(rect.y-self.rect.y) <= BLOCK_SIZE:
                    near += 1
                    if self.rect.colliderect(rect):
                        if self.first_time:
                            self.offset = self.rect.centerx - rect.centerx
                            self.first_time = False
                        self.rect.bottom = rect.top
                        self.gravity = 0
                        self.is_standing = True
                    if not self.rect.inflate(-ITEM_SIZE/3,2).colliderect(rect):
                        not_coll += 1
        if not_coll == near:
            self.is_standing = False

    def fall(self):
        self.gravity+=GRAVITY_CONSTANT/2
        self.rect.y += self.gravity

    def update(self,rects):
        self.collisions(rects)
        if not self.is_standing:
            self.fall()
