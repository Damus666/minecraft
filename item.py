from settings import ITEM_SIZE, GRAPHICS_PATH
from pygame_helper.helper_graphics import load_image,scale_image

class ItemInstance:
    def __init__(self,id,type,is_stackable,level=0):

        self.id = id
        self.level = level
        self.type = type
        self.is_stackable = is_stackable
        path = str(self.id) if self.type == "blocks" else str(self.id)+"/"+str(self.level)
        image = load_image(f"{GRAPHICS_PATH}{type}/{path}.png",True)
        self.image = scale_image(image,None,ITEM_SIZE,ITEM_SIZE)

    def __copy__(self):
        return ItemInstance(self.id,self.type,self.is_stackable,self.level)