from pygame_helper.pygame_helper import debug
from mechanics.combat_system import CombatSystem
from item.item import ItemInstance
from player.player import Player
import pygame
from utility.asset_loader import return_assets
from settings import BLOCK_SIZE, CHUNK_SIZE, ENTITIES, GRAPHICS_PATH, HEIGHT, MONSTERS, WIDTH, FILE_NAMES,W_DATA_F,DAY_DURATION,NIGHT_DURATION,TRANSITION_DUR
from noise import pnoise1
from dict.data import block_ids,blocks_data, frames, tools_data,items_data, entities_data
from random import randint, choice
from world.structures import *
from mechanics.mining_system import MiningSystem
from item.drop import Drop
from mechanics.build_system import BuildSystem
from pygame_helper.helper_graphics import draw_image, load_image,scale_image
from utility.custom_button import CustomButton
import psutil,os,time, json
from entity.entities import PorcupineEntity, SkeletonEntity, ZombieEntity
from crafting.crafting_system import CraftingSystem

class World:
    def __init__(self, screen,id,exit,get_fps,c_folder):
        
        self.screen = screen
        self.is_dead = False
        self.is_paused = False
        self.id = id
        self.can_press = True

        self.x_range = int(WIDTH/(BLOCK_SIZE*CHUNK_SIZE))+3
        self.y_range = int(HEIGHT/(BLOCK_SIZE*CHUNK_SIZE))+3

        self.scroll = pygame.Vector2((0,0))

        self.assets = return_assets()

        self.f3_font = pygame.font.Font("assets/fonts/regular.ttf",30)
        self.f3_offset = 35
        self.f3_spacing = 10
        self.is_f3 = False
        ex = self.f3_font.render("CAPS",True,"white")
        self.f3_height = ex.get_height()

        self.bg_img_0 = load_image("assets/graphics/world_bg/0.png")
        self.bg_img_1 = load_image("assets/graphics/world_bg/1.png")
        self.bg_img_2 = load_image("assets/graphics/world_bg/2.png")
        self.bg_sizes = self.bg_img_0.get_width(), self.bg_img_0.get_height()

        self.red_tint = pygame.Surface((WIDTH,HEIGHT))
        self.red_tint.fill("red")
        self.red_tint.set_alpha(50)
        self.death_font = pygame.font.Font("assets/fonts/regular.ttf",60)
        self.button_font = pygame.font.Font("assets/fonts/regular.ttf",30)
        self.death_img = self.death_font.render("You Died!",True,"white")
        self.death_img_2 = self.death_font.render("You Died!",True,(60,60,60))
        self.death_rect = self.death_img.get_rect(midbottom = (WIDTH//2,HEIGHT//2-self.death_img.get_height()))
        self.pause_img = self.button_font.render("Pause",True,(220,220,220))
        self.pause_img_2 = self.button_font.render("Pause",True,(60,60,60))
        self.pause_rect = self.pause_img.get_rect(midbottom = (WIDTH//2,HEIGHT//2-self.pause_img.get_height()))
        self.respawn_button = CustomButton((0,0),(WIDTH//2,HEIGHT//2+50),f"{GRAPHICS_PATH}gui/buttons/empty_button.png",2.5,self.button_font,"Respawn")
        self.resume_button = CustomButton((0,0),(WIDTH//2,HEIGHT//2+50),f"{GRAPHICS_PATH}gui/buttons/empty_button.png",2.5,self.button_font,"Resume")
        self.exit_button = CustomButton((0,0),(WIDTH//2,HEIGHT//2+150),f"{GRAPHICS_PATH}gui/buttons/empty_button.png",2.5,self.button_font,"Exit")

        self.rect_colliders = []
        self.chunk_colliders = []
        self.free_pos_rects = []
        self.structure_b_id = CHUNK_SIZE*CHUNK_SIZE+1
        self.player_block_id = -1

        self.world_data = {}
        self.structures_data = []
        self.drops = []
        self.animal_entities = []
        self.monster_entities = []
        self.player_blocks = []
        self.block_heights = {"stone":16,"dirt":8,"deepslate":50,"bedrock":64}

        self.player = Player((WIDTH//2,HEIGHT//2),self.scroll_x,self.scroll_y,self.assets,self.add_drop,self.trigger_death,self.close_crafting)

        self.repeat_noise = 99999999
        self.amplitude_multiplier = 0.08
        self.height_multiplier = 5
        self.structure_render_offset = 5*BLOCK_SIZE

        self.mining_system = MiningSystem(self.get_block_rects,self.get_chunk_rects,self.get_world_data,self.edit_chunk_data, self.get_scroll, self.get_structures,self.edit_structures, self.get_player_pos,self.player.hotbar.get_selected,self.add_drop,self.get_player_blocks,self.remove_player_block,self.player.statistics.get_hunger,self.player.change_selected_item)
        self.build_system = BuildSystem(self.get_free_pos_rects,self.player.hotbar.get_selected,self.add_block,self.get_current_block_id,self.update_current_block_id,self.player.hotbar.decrease_slot,self.player.get_rect,self.get_player_pos,self.get_player_blocks,self.get_scroll,self.trigger_special_actions)
        self.combat_system = CombatSystem(self.get_entities,self.player.hotbar.get_selected,self.player.get_rect,self.player.change_selected_item)
        self.crafting_system = CraftingSystem(self.player.inventory.slot_rects["0;0"].left,self.player.inventory.inv_sizes[0],self.player.inventory.inv_rect.bottom+self.player.inventory.y_pos_special,self.player.inventory.get_slots,self.player.inventory.add_item,self.player.inventory.get_free_pos_by_id,self.player.inventory.remove_item)

        self.crafting_open = False
        self.player.refresh_crafting = self.crafting_system.refresh_correct_items

        self.exit = exit
        self.get_fps = get_fps
        self.create_folder = c_folder

        self.seconds = 0
        self.last_time = 0
        self.last_save = pygame.time.get_ticks()

        self.infos = {"fps":60,"pos":(0,0),"selected":"", "time":self.seconds,"last_save":self.last_save,"render":0}
        self.extra_infos = {"ram":0,"cpu":0}

        self.process = os.getpid()
        self.python = psutil.Process(self.process)

        self.loaded_entities = 0

        self.sun_img = scale_image(load_image(f"{GRAPHICS_PATH}other/sun.png"),0.8)
        self.moon_img = scale_image(load_image(f"{GRAPHICS_PATH}other/moon.png"),0.8)
        self.celestial_height = 200
        self.celestial_default_left = -100
        self.sun_x_pos = self.celestial_default_left
        self.moon_x_pos = self.celestial_default_left
        self.is_day = True
        self.sun_speed = WIDTH/DAY_DURATION
        self.moon_speed = WIDTH/NIGHT_DURATION
        self.night_tint = pygame.Surface((WIDTH,HEIGHT))
        self.night_tint.fill("blue")
        self.night_tint.set_alpha(0)
        self.max_night_alpha = 150
        self.alpha_multiplier = 1
        self.last_milli = 0
        self.alpha = 0
        self.is_in_transition = False
        self.transition_speed = self.max_night_alpha/TRANSITION_DUR

        self.range_x = int(WIDTH/self.bg_sizes[0])+1
        self.range_y = (int(HEIGHT/self.bg_sizes[1])+1)-2

        self.keys = ["Keys:","Walk: 'A' & 'D'","Jump: 'SPACE'","Pause: 'ESC'","This Menu: 'F3'","Destroy/Attack: 'MOUSE_LEFT'","Place: 'MOUSE_RIGHT'","Item Interaction: 'R'","Open Inventory: 'E'","Drop Items: 'Q'"]

        self.load_data()

    def trigger_special_actions(self, action):
        if action == "crafting":
            self.player.inventory_open = True
            self.player.inventory.move_inventory(1)
            self.crafting_open = True
            self.crafting_system.refresh_correct_items()

    def close_crafting(self):
        self.crafting_open = False

    def set_ids(self,struct,block):
        self.structure_b_id = struct
        self.player_block_id = block

    def spawn_monsters(self):
        for chunk in self.world_data.values():
            c = False
            for block in chunk:
                if block["id"] == block_ids["grassblock"]:
                    m_name = choice(MONSTERS)
                    if randint(0,100) <= entities_data[m_name]["chances"]:
                        pos = block["pos"][0],block["pos"][1]-1
                        pos = pos[0]*BLOCK_SIZE-self.scroll.x,pos[1]*BLOCK_SIZE-self.scroll.y
                        match m_name:
                            case "zombie":
                                z = ZombieEntity(pos,m_name,self.add_drop,self.delete_entity,self.player.get_rect,self.player.statistics.damage_player)
                                self.monster_entities.append(z)
                            case "skeleton":
                                s = SkeletonEntity(pos,m_name,self.add_drop,self.delete_entity,self.player.get_rect,self.player.statistics.damage_player)
                                self.monster_entities.append(s)
                    c = True
            if c:
                continue

    def draw_day_night(self):
        if self.night_tint.get_alpha() > 0:
            draw_image(self.night_tint,(0,0))

        if self.is_day:
            draw_image(self.sun_img,(self.sun_x_pos,self.celestial_height))
        else:
            draw_image(self.moon_img,(self.moon_x_pos,self.celestial_height))

    def transition(self):
        self.alpha += self.alpha_multiplier*self.transition_speed*(pygame.time.get_ticks()-self.last_milli)
        if self.alpha <= 0:
            self.alpha = 0
            self.is_in_transition = False
            for m in self.monster_entities:
                m.die()
        if self.alpha >= self.max_night_alpha:
            self.alpha = self.max_night_alpha
            self.is_in_transition = False
            self.spawn_monsters()
        self.night_tint.set_alpha(self.alpha)

    def update_day_night(self,dt):
        if self.is_in_transition:
            self.transition()

        if self.is_day:
            self.sun_x_pos+= self.sun_speed*dt*(pygame.time.get_ticks()-self.last_milli)
            if self.sun_x_pos > WIDTH+50:
                self.is_day = False
                self.sun_x_pos = self.celestial_default_left
                self.alpha_multiplier = 1
                self.is_in_transition = True
        else:
            self.moon_x_pos += self.moon_speed*dt*(pygame.time.get_ticks()-self.last_milli)
            if self.moon_x_pos > WIDTH+50:
                self.is_day = True
                self.moon_x_pos = self.celestial_default_left
                self.alpha_multiplier = -1
                self.is_in_transition = True

        self.last_milli = pygame.time.get_ticks()

    def delete_entity(self,e):
        try:
            self.animal_entities.remove(e)
        except:
            self.monster_entities.remove(e)

    def get_entities(self):
        return self.animal_entities+self.monster_entities

    def load_data(self):
        name = W_DATA_F+self.id+"/"
        try:
            with open(name+FILE_NAMES["chunk"],"r") as c_file:
                self.world_data = json.load(c_file)
            with open(name+FILE_NAMES["structure"],"r") as s_file:
                self.structures_data = json.load(s_file)["structures"]
            with open(name+FILE_NAMES["block"],"r") as b_file:
                self.player_blocks = json.load(b_file)["blocks"]
            with open(name+FILE_NAMES["drop"],"r") as d_file:
                drop_dict = json.load(d_file)
                for drop in drop_dict["drops"]:
                    d = Drop((drop["pos"][0]+drop["offset"],drop["pos"][1]),ItemInstance(drop["item"]["id"],drop["item"]["type"],drop["item"]["is_stackable"]),drop["quantity"])
                    self.drops.append(d)

            with open(name+FILE_NAMES["entity"],"r") as e_file:
                entity_dict = json.load(e_file)
                for e in entity_dict["animals"]:
                    match e["type"]:
                        case "porcupine":
                            new_e = PorcupineEntity(e["pos"],e["type"],self.add_drop,self.delete_entity,e["health"],e["p_f"])
                            self.animal_entities.append(new_e)
                for e in entity_dict["monsters"]:
                    match e["type"]:
                        case "zombie":
                            new_e = ZombieEntity(e["pos"],e["type"],self.add_drop,self.delete_entity,self.player.get_rect,self.player.statistics.damage_player,e["health"],e["p_f"])
                            self.monster_entities.append(new_e)
                        case "skeleton":
                            new_e = SkeletonEntity(e["pos"],e["type"],self.add_drop,self.delete_entity,self.player.get_rect,self.player.statistics.damage_player,e["health"],e["p_f"])
                            self.monster_entities.append(new_e)

            with open(name+FILE_NAMES["other"],"r") as o_file:
                other = json.load(o_file)
                self.scroll = pygame.Vector2((other["scroll"][0],other["scroll"][1]))
                self.set_ids(other["structure_b_id"],other["player_b_id"])
                self.seconds = other["seconds"]
                self.is_day = other["is_day"]
                self.sun_x_pos = other["sun_x"]
                self.moon_x_pos = other["moon_x"]
                self.alpha = other["alpha"]
                self.is_in_transition = other["in_trans"]
                self.night_tint.set_alpha(self.alpha)
            self.player.load_data(self.id)
        except:
            self.save_data()

    def save_data(self):
            self.create_folder(self.id)
            name = W_DATA_F+self.id+"/"
            with open(name+FILE_NAMES["chunk"],"w") as c_file:
                json.dump(self.world_data,c_file)
            with open(name+FILE_NAMES["structure"],"w") as s_file:
                json.dump({"structures":self.structures_data},s_file)
            with open(name+FILE_NAMES["block"],"w") as b_file:
                json.dump({"blocks":self.player_blocks},b_file)
            drop_dict = {"drops":[{"pos":(drop.rect.centerx,drop.rect.centery-20),"offset":drop.offset,"quantity":drop.quantity,"item":{"id":drop.item.id,"type":drop.item.type,"is_stackable":drop.item.is_stackable}} for drop in self.drops]}
            with open(name+FILE_NAMES["drop"],"w") as d_file:
                json.dump(drop_dict,d_file)

            entity_dict = {"animals":[{"pos":(e.rect.centerx,e.rect.centery-20),"type":e.type,"health":e.health,"p_f":e.pixel_fell} for e in self.animal_entities],"monsters":[{"pos":(e.rect.centerx,e.rect.centery-20),"type":e.type,"health":e.health,"p_f":e.pixel_fell} for e in self.monster_entities]}
            with open(name+FILE_NAMES["entity"],"w") as e_file:
                json.dump(entity_dict,e_file)

            other_dict = {"scroll":[self.scroll.x,self.scroll.y],"structure_b_id":self.structure_b_id,"player_b_id":self.player_block_id,"seconds":self.seconds,"is_day":self.is_day,"sun_x":self.sun_x_pos,"moon_x":self.moon_x_pos,"in_trans":self.is_in_transition,"alpha":self.alpha}
            with open(name+FILE_NAMES["other"],"w") as o_file:
                json.dump(other_dict,o_file)
            self.player.save_data(self.id)
            self.last_save = pygame.time.get_ticks()

    def get_pos(self):
        x = ((WIDTH//2+self.player.rect.x)//BLOCK_SIZE)+(self.scroll.x//BLOCK_SIZE)-23
        y = ((HEIGHT//2-self.player.rect.y)//BLOCK_SIZE)-(self.scroll.y//BLOCK_SIZE)
        return int(x),int(y)

    def get_memory(self):
        return "RAM: "+str(round(self.python.memory_info()[0]/1073741824,2))+" GB / "+str(round(psutil.virtual_memory()[0]/1073741824,2))+" GB"

    def get_cpu(self):
        return "CPU: "+str(round(self.python.cpu_percent()/os.cpu_count(),1))+" %"

    def draw_f3_infos(self):

        self.infos["fps"] = str(int(self.get_fps()))+" FPS"
        self.infos["pos"] = "X: "+str(self.get_pos()[0])+"  Y: "+str(self.get_pos()[1])
        self.infos["time"] = "Time Played: "+time.strftime("%H:%M:%S", time.gmtime(self.seconds))
        self.infos["last_save"] = "Last Save: "+str(int(((pygame.time.get_ticks()-self.last_save)/1000)/60))+" Minutes Ago"
        self.infos["render"] = "Rendering: "+str(len(self.chunk_colliders))+" Chunks, "+str(len(self.rect_colliders))+" Blocks, "+str(self.loaded_entities+1)+" Entities"
        try:
            if self.player.hotbar.get_selected().empty == False:
                item = self.player.hotbar.get_selected().item
                if item.type == "blocks":
                    self.infos["selected"] = "Selected Item: "+blocks_data[item.id]["name"]
                elif item.type == "items":
                    self.infos["selected"] = "Selected Item: "+items_data[item.id]["name"]
                elif item.type == "tools":
                    self.infos["selected"] = "Selected Item: "+tools_data[item.id][item.level]["name"]
            else:
                self.infos["selected"] = "Selected Item: None"
        except:pass

        self.extra_infos["ram"] = self.get_memory()
        self.extra_infos["cpu"] = self.get_cpu()

        for index,info in enumerate(self.infos.keys()):
            self.draw_info(0,index,self.infos[info])

        for index,info in enumerate(self.extra_infos.keys()):
            self.draw_info(WIDTH-500,index,self.extra_infos[info])

        for index, info in enumerate(self.keys):
            self.draw_info(0,index+10,info)

    def draw_info(self,x,y_order,text):
        img = self.f3_font.render(str(text),True,"white")
        bg = pygame.Surface((img.get_width()+2.5,img.get_height()+2.5))
        bg.fill((60,60,60))
        bg.set_alpha(100)
        draw_image(bg,(x+self.f3_offset-1.25,self.f3_offset+self.f3_height*y_order+self.f3_spacing*y_order-1.25))
        draw_image(img,(x+self.f3_offset,self.f3_offset+self.f3_height*y_order+self.f3_spacing*y_order))

    def trigger_death(self):
        self.is_dead = True
        self.player.is_dead = True
        self.player.inventory.drop_all()
        self.player.inventory.clear()
        self.player.selected_item = None

    def reset_world(self):
        self.player.rect.center = (WIDTH//2,HEIGHT//2)
        self.scroll = pygame.Vector2((0,0))
        self.player.statistics.reset()
        self.player.hotbar.slots[str(round(self.player.hotbar.columns/2-0.1))+";0"].selected = True
        self.player.hotbar.selection_index = round(self.player.hotbar.columns/2-0.1)
        self.mining_system.reset()
        self.player.reset()

    def remove_player_block(self,block):
        self.player_blocks.remove(block)

    def get_player_blocks(self):
        return self.player_blocks

    def update_current_block_id(self):
        self.player_block_id -= 1 

    def get_current_block_id(self):
        return self.player_block_id

    def add_block(self,block):
        self.player_blocks.append(block) 

    def get_free_pos_rects(self):
        return self.free_pos_rects

    def add_drop(self,pos,item,quantity=1):
        self.drops.append(Drop(pos,item,quantity))

    def get_player_pos(self):
        return self.player.rect

    def edit_structures(self,index,structure):
        self.structures_data[index] = structure

    def get_structures(self):
        return self.structures_data

    def get_scroll(self):
        return self.scroll

    def edit_chunk_data(self,chunk_data,chunk_index):
        self.world_data[chunk_index] = chunk_data

    def get_world_data(self):
        return self.world_data

    def get_chunk_rects(self):
        return self.chunk_colliders

    def get_block_rects(self):
        return self.rect_colliders

    def scroll_x(self,dt):
        self.scroll.x += self.player.x_speed*self.player.direction#*dt
        if self.drops:
            for drop in self.drops:
                drop.rect.x -= self.player.x_speed*self.player.direction#*dt
        if self.animal_entities:
            for e in self.animal_entities:
                e.rect.x -= self.player.x_speed*self.player.direction
        if self.monster_entities:
            for m in self.monster_entities:
                m.rect.x -= self.player.x_speed*self.player.direction

    def scroll_y(self,dt):
        self.scroll.y += self.player.gravity#*dt
        if self.drops:
            for drop in self.drops:
                drop.rect.y -= self.player.gravity#*dt
        if self.animal_entities:
            for e in self.animal_entities:
                e.rect.y -= self.player.gravity
        if self.monster_entities:
            for m in self.monster_entities:
                m.rect.y -= self.player.gravity

    def generate_chunk(self,x,y):
        has_tree = False
        has_entity = False
        chunk_data = []
        unique_id = 0
        final__x = x*CHUNK_SIZE
        final__y = y*CHUNK_SIZE
        chunk_data.append({"pos":[final__x,final__y],"id":-2,"collider":False,"frame":0,"unique":-1,"cooldown":0})

        for y_pos in range(CHUNK_SIZE):
            for x_pos in range(CHUNK_SIZE):
                self.block_heights = {"stone":randint(15,17),"dirt":8,"deepslate":randint(46,54),"bedrock":randint(60,64)}

                final_x = x*CHUNK_SIZE+x_pos
                final_y = y*CHUNK_SIZE+y_pos
                block_id = -1

                height = int(pnoise1(final_x*self.amplitude_multiplier,repeat=self.repeat_noise) * self.height_multiplier)
                collider = True
                frame = 0

                if final_y >= self.block_heights["bedrock"] - height:
                    block_id = block_ids["bedrock"]
                elif final_y >= self.block_heights["deepslate"] - height:
                    block_id = block_ids["grimstone"]
                elif final_y >= self.block_heights["stone"] - height:
                    block_id = block_ids["stone"]
                elif final_y > self.block_heights["dirt"] - height:
                    block_id = block_ids["dirt"]
                elif final_y == self.block_heights["dirt"]-height:
                    block_id = block_ids["grassblock"]
                elif final_y == self.block_heights["dirt"]-height-1:
                    if randint(0,8) == 4:
                        block_id = block_ids["grass"]
                        frame_num = frames[block_ids["grass"]]
                        frame = randint(0,frame_num-1)
                        collider = False
                    else:
                        if 2 < x_pos < CHUNK_SIZE-2:
                            if randint(0,10) == 4 and has_tree == False:
                                tree_data = generate_tree(final_x,final_y,self.structure_b_id)
                                self.structures_data.append(tree_data[0])
                                self.structure_b_id = tree_data[1]
                                has_tree = True
                    if not has_tree and not has_entity:
                        if self.is_day:
                            e_name = choice(ENTITIES)
                            if randint(0,100) <= entities_data[e_name]["chances"]:
                                match e_name:
                                    case "porcupine":
                                        e = PorcupineEntity((final_x*BLOCK_SIZE-self.scroll.x,final_y*BLOCK_SIZE-self.scroll.y),e_name,self.add_drop,self.delete_entity)
                                        self.animal_entities.append(e)
                            has_entity = True
                        else:
                            m_name = choice(MONSTERS)
                            if randint(0,100) <= entities_data[m_name]["chances"]:
                                pos = (final_x*BLOCK_SIZE-self.scroll.x,final_y*BLOCK_SIZE-self.scroll.y)
                                match m_name:
                                    case "zombie":
                                        z = ZombieEntity(pos,m_name,self.add_drop,self.delete_entity,self.player.get_rect,self.player.statistics.damage_player)
                                        self.monster_entities.append(z)
                                    case "skeleton":
                                        s = SkeletonEntity(pos,m_name,self.add_drop,self.delete_entity,self.player.get_rect,self.player.statistics.damage_player)
                                        self.monster_entities.append(s)

                if block_id != -1:
                    chunk_data.append({"pos":[final_x,final_y],"id":block_id,"collider":collider,"frame":frame,"unique":unique_id})
                elif block_id == -1:
                    chunk_data.append({"pos":[final_x,final_y],"id":-1,"unique":-1})
                unique_id += 1

        return chunk_data

    def draw_block(self,block,structure=False,collider=True):
        self.screen.blit(self.assets[block["id"]][block["frame"]],(block["pos"][0]*BLOCK_SIZE-self.scroll.x,block["pos"][1]*BLOCK_SIZE-self.scroll.y))
        if block["collider"] == True:
            rect = pygame.Rect(block["pos"][0]*BLOCK_SIZE-self.scroll.x,block["pos"][1]*BLOCK_SIZE-self.scroll.y,BLOCK_SIZE,BLOCK_SIZE)
            self.rect_colliders.append([rect,block["unique"],collider])
            if structure: 
                if rect in list(list(zip(*self.free_pos_rects))[0]):
                    self.free_pos_rects.remove([rect,block["pos"]]) 

    def render_chunks(self):
        for y in range(self.y_range):
            for x in range(self.x_range):
                target_x = x - 1 + int(round(self.scroll.x/(CHUNK_SIZE*BLOCK_SIZE)))
                target_y = y - 1 + int(round(self.scroll.y/(CHUNK_SIZE*BLOCK_SIZE)))
                target_chunk = str(target_x)+";"+str(target_y)
                if target_chunk not in self.world_data:
                    self.world_data[target_chunk] = self.generate_chunk(target_x,target_y)
                self.chunk_colliders.append([pygame.Rect(self.world_data[target_chunk][0]["pos"][0]*BLOCK_SIZE-self.scroll.x,self.world_data[target_chunk][0]["pos"][1]*BLOCK_SIZE-self.scroll.y,CHUNK_SIZE*BLOCK_SIZE,CHUNK_SIZE*BLOCK_SIZE),target_chunk])

                for block in self.world_data[target_chunk]:
                    if block["id"] >= 0:
                        self.draw_block(block)
                    elif block["id"] == -1:
                        rect = pygame.Rect(block["pos"][0]*BLOCK_SIZE-self.scroll.x,block["pos"][1]*BLOCK_SIZE-self.scroll.y,BLOCK_SIZE,BLOCK_SIZE)
                        self.free_pos_rects.append([rect,block["pos"]])

    def render_player_blocks(self):
        for block in self.player_blocks:
            if block["pos"][0]*BLOCK_SIZE-self.scroll.x > 0-BLOCK_SIZE*2 and block["pos"][0]*BLOCK_SIZE-self.scroll.x < WIDTH+BLOCK_SIZE*2 and block["pos"][1]*BLOCK_SIZE-self.scroll.y > 0-BLOCK_SIZE*2 and block["pos"][1]*BLOCK_SIZE-self.scroll.y < HEIGHT+BLOCK_SIZE*2:
                self.draw_block(block,True)

    def render_structures(self):
        for structure in self.structures_data:
            if len(structure) == 0:
                self.structures_data.remove(structure)
                continue
            if structure[0]["pos"][0]*BLOCK_SIZE-self.scroll.x > 0-self.structure_render_offset and structure[0]["pos"][0]*BLOCK_SIZE-self.scroll.x < WIDTH+self.structure_render_offset and structure[0]["pos"][1]*BLOCK_SIZE-self.scroll.y > 0-self.structure_render_offset and structure[0]["pos"][1]*BLOCK_SIZE-self.scroll.y < HEIGHT+self.structure_render_offset*2:
                for block in structure:
                    self.draw_block(block,True,False)

    def render_drops(self):
        if self.drops:
            for drop in self.drops:
                if drop.rect.right > 0-BLOCK_SIZE and drop.rect.left < WIDTH+BLOCK_SIZE and drop.rect.bottom > 0-BLOCK_SIZE and drop.rect.top < HEIGHT+BLOCK_SIZE:
                    if not self.is_dead:
                        if self.player.drop_collision(drop):
                            self.drops.remove(drop)
                    drop.draw()
                    drop.update(self.rect_colliders)
                    self.loaded_entities += 1

    def render_entities(self):
        if self.animal_entities:
            for e in self.animal_entities:
                if e.rect.right > 0-BLOCK_SIZE*3 and e.rect.left < WIDTH+BLOCK_SIZE*3 and e.rect.bottom > 0-BLOCK_SIZE*3 and e.rect.top < HEIGHT+BLOCK_SIZE*3:
                    e.draw()
                    if not self.is_dead and not self.is_paused:
                        e.walk_animation()
                        e.update(self.rect_colliders)
                    self.loaded_entities += 1
        if self.alpha > 0:
            if self.monster_entities:
                for m in self.monster_entities:
                    if m.rect.right > 0-BLOCK_SIZE*3 and m.rect.left < WIDTH+BLOCK_SIZE*3 and m.rect.bottom > 0-BLOCK_SIZE*3 and m.rect.top < HEIGHT+BLOCK_SIZE*3:
                        m.draw()
                        if not self.is_dead and not self.is_paused:
                            m.walk_animation()
                            m.update(self.rect_colliders)
                        self.loaded_entities += 1

    def death_actions(self):
        draw_image(self.red_tint,(0,0))
        draw_image(self.death_img_2,(self.death_rect.topleft[0]+5,self.death_rect.topleft[1]+5))
        draw_image(self.death_img,self.death_rect)
        
        if self.respawn_button.draw_check():
            self.reset_world()
            self.is_dead = False

    def pause_actions(self):
        draw_image(self.pause_img_2,(self.pause_rect.topleft[0]+3,self.pause_rect.topleft[1]+3))
        draw_image(self.pause_img,self.pause_rect)
        
        if self.resume_button.draw_check():
            self.is_paused = False
            self.player.is_dead = False
            self.player.inventory_open = False
        if self.exit_button.draw_check():
            self.is_paused = False
            self.player.is_dead = False
            self.player.inventory_open = False
            self.save_data()
            self.exit()

    def draw_bg(self):
        for i in range(self.range_x):
            draw_image(self.bg_img_2,(i*self.bg_sizes[0],0-self.bg_sizes[1]/2.5))
            draw_image(self.bg_img_1,(i*self.bg_sizes[0],self.bg_sizes[1]-self.bg_sizes[1]/2.5-1))
            draw_image(self.bg_img_0,(i*self.bg_sizes[0],self.bg_sizes[1]*2-self.bg_sizes[1]/2.5-2))
            if self.range_y > 0:
                for o in range(self.range_y):
                    draw_image(self.bg_img_0,(i*self.bg_sizes[0],self.bg_sizes[1]*(o+2)-self.bg_sizes[1]/2.5-2))

    def draw(self):
        self.draw_bg()
        self.draw_day_night()
        # player
            
        self.render_chunks()
        self.render_structures()
        
        self.render_player_blocks()
        self.render_entities()
        if not self.is_dead:
            self.player.custom_draw()

        if self.is_f3:
            self.draw_f3_infos()
        self.loaded_entities = 0
        
    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] and self.can_press:
            self.can_press = False
            self.is_paused = not self.is_paused
            self.player.is_dead = not self.player.is_dead
            self.player.inventory_open = False
            if self.player.inventory.y_offset != 0:
                self.player.inventory.move_inventory(-1)
            self.crafting_open = False

        if keys[pygame.K_F3] and self.can_press:
            self.is_f3 = not self.is_f3
            self.can_press = False

        if not keys[pygame.K_ESCAPE] and not keys[pygame.K_F3]:
            self.can_press = True

    def update(self,dt):
        mouse = pygame.mouse.get_pressed()
        self.render_drops()

        # player
        self.player.update(self.rect_colliders,dt,mouse)

        if not self.is_dead:
            self.input()
            if not self.is_paused:
                self.update_day_night(dt)
                # mining
                if not self.player.inventory_open:
                    self.mining_system.update(mouse)
                    self.build_system.update(mouse)
                    self.combat_system.update(mouse)
                else:
                    if self.crafting_open:
                        self.crafting_system.update(mouse)
                        self.crafting_system.draw()
            else:
                self.last_milli = pygame.time.get_ticks()

        # refresh
        self.rect_colliders.clear()
        self.chunk_colliders.clear()
        self.free_pos_rects.clear()

        if self.is_dead:
            self.death_actions()
        elif self.is_paused:
            self.pause_actions()

        if pygame.time.get_ticks()-self.last_time >= 1000 and self.is_paused==False and self.is_dead == False:
            self.last_time=pygame.time.get_ticks()
            self.seconds+=1