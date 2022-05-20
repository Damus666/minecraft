from pygame_helper.helper_graphics import load_image,scale_image
from settings import BLOCK_SIZE,GRAPHICS_PATH
from dict.data import block_ids,frames

def return_assets():
    assets = {}
    for id in block_ids.values():
        if id == block_ids["grass"]:
            assets[id] = load_assets(id,frames[id])
        else:
            assets[id] = list([load_asset(id)])
    return assets

def load_asset(id,path=None):
    if not path:
        img = load_image(f"{GRAPHICS_PATH}blocks/{id}.png",True)
    else:
        img = load_image(f"{GRAPHICS_PATH}blocks/{path}/{id}.png",True)
    img = scale_image(img,None,BLOCK_SIZE,BLOCK_SIZE)
    return img

def load_assets(name, num):
    images = []
    for i in range(num):
        img = load_asset(i,name)
        images.append(img)
    return images