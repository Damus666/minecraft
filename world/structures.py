from dict.data import block_ids
from random import randint

def generate_tree(x,y,start_id):
    tree_data = []
    collider = True
    frame = 0 
    unique = start_id
    choice = randint(0,3)
    minuser = 3

    tree_data.append({"pos":[x,y],"id":block_ids["log"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x,y-1],"id":block_ids["log"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x,y-2],"id":block_ids["log"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    if choice == 0:
        minuser = 4
        tree_data.append({"pos":[x,y-3],"id":block_ids["log"],"collider":collider,"frame":frame,"unique":unique,})
        unique+=1
    if choice == 2:
        minuser = 5
        tree_data.append({"pos":[x,y-3],"id":block_ids["log"],"collider":collider,"frame":frame,"unique":unique,})
        unique+=1
        tree_data.append({"pos":[x,y-4],"id":block_ids["log"],"collider":collider,"frame":frame,"unique":unique,})
        unique+=1
    tree_data.append({"pos":[x,y-minuser],"id":block_ids["leaves"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x-1,y-minuser],"id":block_ids["leaves"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x+1,y-minuser],"id":block_ids["leaves"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x,y-minuser-1],"id":block_ids["leaves"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1

    return tree_data,unique