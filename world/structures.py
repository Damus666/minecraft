from dict.data import block_ids, trees_ids
from random import randint

def generate_structure(x,y,start_id,type):
    if type == trees_ids["oak_tree"]:
        return generate_tree(x,y,start_id)
    elif type == trees_ids["birch_tree"]:
        return generate_birch_tree(x,y,start_id)
    elif type == trees_ids["cactus"]:
        return generate_cactus(x,y,start_id)

def generate_cactus(x,y,start_id):
    tree_data = []
    collider = True
    frame = 0 
    unique = start_id
    more = randint(0,2)

    tree_data.append({"pos":[x,y],"id":block_ids["cactus"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x,y-1],"id":block_ids["cactus"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    for i in range(more+1):
        tree_data.append({"pos":[x,y-1-i],"id":block_ids["cactus"],"collider":collider,"frame":frame,"unique":unique,})
        unique+=1

    return tree_data,unique

def generate_birch_tree(x,y,start_id):
    tree_data = []
    collider = True
    frame = 0 
    unique = start_id
    choice = randint(0,3)
    minuser = 3

    tree_data.append({"pos":[x,y],"id":block_ids["birchlog"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x,y-1],"id":block_ids["birchlog"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x,y-2],"id":block_ids["birchlog"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    if choice == 0:
        minuser = 4
        tree_data.append({"pos":[x,y-3],"id":block_ids["birchlog"],"collider":collider,"frame":frame,"unique":unique,})
        unique+=1
    if choice == 2:
        minuser = 5
        tree_data.append({"pos":[x,y-3],"id":block_ids["birchlog"],"collider":collider,"frame":frame,"unique":unique,})
        unique+=1
        tree_data.append({"pos":[x,y-4],"id":block_ids["birchlog"],"collider":collider,"frame":frame,"unique":unique,})
        unique+=1
    tree_data.append({"pos":[x,y-minuser],"id":block_ids["redleaves"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x-1,y-minuser],"id":block_ids["redleaves"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x+1,y-minuser],"id":block_ids["redleaves"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x,y-minuser-1],"id":block_ids["redleaves"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x-1,y-minuser-1],"id":block_ids["redleaves"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1
    tree_data.append({"pos":[x+1,y-minuser-1],"id":block_ids["redleaves"],"collider":collider,"frame":frame,"unique":unique,})
    unique+=1

    return tree_data,unique

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