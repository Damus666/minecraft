from pygame_helper.pygame_helper import debug
from mechanics.combat_system import CombatSystem
from item.item import ItemInstance
from mechanics.furnace_system import FurnacesManager
from mechanics.storage_system import StorageManager
from player.player import Player
import pygame, json
from utility.asset_loader import return_assets
from settings import BIOME_SIZES, BLOCK_SIZE, CHUNK_SIZE, ENTITIES, ENTITY_DESPAWN_RANGE, GRAPHICS_PATH, HEIGHT, MONSTERS, WIDTH, FILE_NAMES,W_DATA_F,DAY_DURATION,NIGHT_DURATION,TRANSITION_DUR
from noise import pnoise1, snoise2, perlin
from perlin_noise import PerlinNoise
from dict.data import block_ids, frames, entities_data,ores_data,biomes_data,biomes_ids
from random import randint, choice
from world.f3_menu import f3Menu
from world.structures import *
from mechanics.mining_system import MiningSystem
from item.drop import Drop
from mechanics.build_system import BuildSystem
from pygame_helper.helper_graphics import draw_image
from utility.custom_button import CustomButton
from entity.entities import PorcupineEntity, SkeletonEntity, ZombieEntity
from crafting.crafting_system import CraftingSystem
from utility.pixel_calculator import height_calculator, medium_calculator
from world.day_night_cycle import DayNightCycle

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

        self.is_f3 = False

        self.red_tint = pygame.Surface((WIDTH,HEIGHT))
        self.red_tint.fill("red")
        self.red_tint.set_alpha(50)
        self.death_font = pygame.font.Font("assets/fonts/regular.ttf",medium_calculator(60,True))
        self.button_font = pygame.font.Font("assets/fonts/regular.ttf",medium_calculator(30,True))
        self.death_img = self.death_font.render("You Died!",True,"white")
        self.death_img_2 = self.death_font.render("You Died!",True,(60,60,60))
        self.death_rect = self.death_img.get_rect(midbottom = (WIDTH//2,HEIGHT//2-self.death_img.get_height()))
        self.pause_img = self.button_font.render("Pause",True,(220,220,220))
        self.pause_img_2 = self.button_font.render("Pause",True,(60,60,60))
        self.died_offset = medium_calculator(5)
        self.pause_offset = medium_calculator(3)
        self.pause_rect = self.pause_img.get_rect(midbottom = (WIDTH//2,HEIGHT//2-self.pause_img.get_height()))
        self.respawn_button = CustomButton((0,0),(WIDTH//2,HEIGHT//2+height_calculator(50)),f"{GRAPHICS_PATH}gui/buttons/empty_button.png",medium_calculator(2.5),self.button_font,"Respawn")
        self.resume_button = CustomButton((0,0),(WIDTH//2,HEIGHT//2+height_calculator(50)),f"{GRAPHICS_PATH}gui/buttons/empty_button.png",medium_calculator(2.5),self.button_font,"Resume")
        self.exit_button = CustomButton((0,0),(WIDTH//2,HEIGHT//2+height_calculator(150)),f"{GRAPHICS_PATH}gui/buttons/empty_button.png",medium_calculator(2.5),self.button_font,"Exit")

        self.rect_colliders = []
        self.chunk_colliders = []
        self.free_pos_rects = []
        self.structure_b_id = CHUNK_SIZE*CHUNK_SIZE+1
        self.player_block_id = -1
        self.currently_loaded_chunks = []
        self.before_loaded_chunks = []

        self.world_data = {}
        self.structures_data = []
        self.drops = []
        self.animal_entities = []
        self.monster_entities = []
        self.player_blocks = []
        self.block_heights = {"stone":16,"dirt":8,"deepslate":50,"bedrock":64}

        self.player = Player((WIDTH//2,HEIGHT//2),self.scroll_x,self.scroll_y,self.assets,self.add_drop,self.trigger_death,self.close_crafting)

        self.repeat_noise = 99999999
        self.amplitude_multiplier = 0.08#0.08
        self.height_multiplier = 5
        self.structure_render_offset = 5*BLOCK_SIZE

        self.left_biome_size = 0
        self.right_biome_size = 0
        self.biome_size = randint(BIOME_SIZES[0],BIOME_SIZES[1])
        self.last_x_biome_r = 0
        self.last_x_biome_l = 0
        self.left_biomes_ranges = [{"start":-1,"biome":0}]
        self.right_biomes_ranges = [{"start":0,"biome":0}]

        self.mining_system = MiningSystem(self.get_block_rects,self.get_chunk_rects,self.get_world_data,self.edit_chunk_data, self.get_scroll, self.get_structures,self.edit_structures, self.get_player_pos,self.player.hotbar.get_selected,self.add_drop,self.get_player_blocks,self.remove_player_block,self.player.statistics.get_hunger,self.player.change_selected_item,self.delete_special_block)
        self.build_system = BuildSystem(self.get_free_pos_rects,self.player.hotbar.get_selected,self.add_block,self.get_current_block_id,self.update_current_block_id,self.player.hotbar.decrease_slot,self.player.get_rect,self.get_player_pos,self.get_player_blocks,self.get_scroll,self.trigger_special_actions)
        self.combat_system = CombatSystem(self.get_entities,self.player.hotbar.get_selected,self.player.get_rect,self.player.change_selected_item)
        self.crafting_system = CraftingSystem(self.player.inventory.slot_rects["0;0"].left,self.player.inventory.inv_sizes[0],self.player.inventory.inv_rect.bottom+self.player.inventory.y_pos_special,self.player.inventory.get_slots,self.player.inventory.add_item,self.player.inventory.get_free_pos_by_id,self.player.inventory.remove_item)
        self.furnaces_manager = FurnacesManager(self.update_block_frame,self.player.inventory.inv_rect.bottom+self.player.inventory.y_pos_special,self.player.inventory.add_item,self.player.inventory.get_free_pos_by_id,self.get_furnace_open,self.add_drop,self.get_scroll)
        self.storages_manager = StorageManager(self.player.inventory.slot_rects["0;0"].left,self.player.inventory.inv_rect.bottom+self.player.inventory.y_pos_special,self.player.inventory.try_place_item_in_here_please,self.get_chest_open)

        self.player.inventory.place_in_furnace = self.furnaces_manager.place_items_in_furnace
        self.player.inventory.place_in_chest = self.storages_manager.try_place_item_in_here_please

        self.crafting_open = False
        self.furnace_open = False
        self.storage_open = False
        self.player.refresh_crafting = self.crafting_system.refresh_correct_items

        self.exit = exit
        self.get_fps = get_fps
        self.create_folder = c_folder

        self.seconds = 0
        self.last_time = 0
        self.last_save = pygame.time.get_ticks()

        self.day_night_cycle_bg = DayNightCycle(self.kill_monsters,self.spawn_monsters)

        self.loaded_entities = 0

        self.f3_menu = f3Menu(self.player.hotbar.get_selected,self.player.get_rect,self.get_scroll,self.get_fps)

        self.load_data()

        self.perlin_noise = perlin.SimplexNoise()

    def get_chest_open(self):
        return self.storage_open

    def get_furnace_open(self):
        return self.furnace_open

    def update_block_frame(self,unique,frame):
        for block in self.player_blocks:
            if block["unique"] == unique:
                block["frame"] = frame
                break

    def kill_monsters(self):
        for m in self.monster_entities:
            m.die()

    def delete_drop(self,drop):
        self.drops.remove(drop)

    def delete_special_block(self,type,block):
        if type == "furnace":
            self.furnaces_manager.delete_furnace(block)

    def trigger_special_actions(self, action, id=0):
        if action == "crafting":
            self.player.inventory_open = True
            self.player.inventory.move_inventory(1)
            self.crafting_open = True
            self.crafting_system.refresh_correct_items()
        elif action == "furnace":
            self.player.inventory_open = True
            self.player.inventory.move_inventory(1)
            self.furnace_open = True
            self.furnaces_manager.open_furnace(id)
        elif action == "chest":
            self.player.inventory_open = True
            self.player.inventory.move_inventory(1)
            self.storage_open = True
            self.storages_manager.open_storage(id)

    def close_crafting(self):
        self.crafting_open = False
        self.furnace_open = False
        if self.storage_open:
            self.storages_manager.paste_slots_to_storage()
        self.storage_open = False

    def set_ids(self,struct,block):
        self.structure_b_id = struct
        self.player_block_id = block

    def spawn_monsters(self):
        for chunk in self.world_data.values():
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
                    break

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
                self.day_night_cycle_bg.is_day = other["is_day"]
                self.day_night_cycle_bg.sun_x_pos = other["sun_x"]
                self.day_night_cycle_bg.moon_x_pos = other["moon_x"]
                self.day_night_cycle_bg.alpha = other["alpha"]
                self.day_night_cycle_bg.is_in_transition = other["in_trans"]
                self.day_night_cycle_bg.night_tint.set_alpha(self.day_night_cycle_bg.alpha)
                self.left_biome_size = other["l_b_s"]
                self.right_biome_size = other["r_b_s"]
                self.last_x_biome_l = other["last_x_l"]
                self.last_x_biome_r = other["last_x_r"]
                self.left_biomes_ranges = other["left_biomes"]
                self.right_biomes_ranges = other["right_biomes"]

            with open(name+FILE_NAMES["special"],"r") as f_file:
                special = json.load(f_file)
                print(special["furnaces"])
                self.furnaces_manager.load_furnaces(special["furnaces"])
                self.storages_manager.load_storages(special["storages"])

            self.player.load_data(self.id)
        except Exception as e:
            print(e)
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

            other_dict = {"scroll":[self.scroll.x,self.scroll.y],"structure_b_id":self.structure_b_id,"player_b_id":self.player_block_id,"seconds":self.seconds,"is_day":self.day_night_cycle_bg.is_day,"sun_x":self.day_night_cycle_bg.sun_x_pos,"moon_x":self.day_night_cycle_bg.moon_x_pos,"in_trans":self.day_night_cycle_bg.is_in_transition,"alpha":self.day_night_cycle_bg.alpha\
                ,"l_b_s":self.left_biome_size,"r_b_s":self.right_biome_size,"last_x_r":self.last_x_biome_r,"last_x_l":self.last_x_biome_l,"left_biomes":self.left_biomes_ranges,"right_biomes":self.right_biomes_ranges}
            with open(name+FILE_NAMES["other"],"w") as o_file:
                json.dump(other_dict,o_file)
            self.player.save_data(self.id)
            self.last_save = pygame.time.get_ticks()

            special_dict = {"furnaces":self.furnaces_manager.get_furnaces_dict(),"storages":self.storages_manager.get_chests_dict()}
            with open(name+FILE_NAMES["special"],"w") as f_file:
                json.dump(special_dict,f_file)

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

    def add_drop(self,pos,item,quantity=1,direction=0):
        self.drops.append(Drop(pos,item,self.delete_drop,quantity,direction))

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
        self.scroll.x += self.player.x_speed*self.player.direction*round(dt)
        if self.drops:
            for drop in self.drops:
                drop.rect.x -= self.player.x_speed*self.player.direction*round(dt)
        if self.animal_entities:
            for e in self.animal_entities:
                e.rect.x -= self.player.x_speed*self.player.direction*round(dt)
        if self.monster_entities:
            for m in self.monster_entities:
                m.rect.x -= self.player.x_speed*self.player.direction*round(dt)

    def scroll_y(self,dt):
        self.scroll.y += self.player.gravity*round(dt)
        if self.drops:
            for drop in self.drops:
                drop.rect.y -= self.player.gravity*round(dt)
        if self.animal_entities:
            for e in self.animal_entities:
                e.rect.y -= self.player.gravity*round(dt)
        if self.monster_entities:
            for m in self.monster_entities:
                m.rect.y -= self.player.gravity*round(dt)

    def generate_chunk(self,x,y):
        has_tree = False
        has_entity = False
        chunk_data = []
        unique_id = 0
        final__x = x*CHUNK_SIZE
        final__y = y*CHUNK_SIZE
        chunk_data.append({"pos":[final__x,final__y],"id":-2,"collider":False,"frame":0,"unique":-1,"cooldown":0})

        if self.scroll.x >= 0 and x > self.last_x_biome_r:
            self.last_x_biome_r = x
            self.right_biome_size+= 1
            if self.right_biome_size > self.biome_size:
                self.biome_size = randint(BIOME_SIZES[0],BIOME_SIZES[1])
                self.right_biomes_ranges[-1]["end"] = x
                self.right_biomes_ranges.append({"start":x+1,"biome":choice(list(biomes_ids.values()))})
                self.right_biome_size = 0
        elif self.scroll.x < 0 and x < self.last_x_biome_l:
            self.last_x_biome_l = x
            self.left_biome_size+= 1
            if self.left_biome_size > self.biome_size:
                self.biome_size = randint(BIOME_SIZES[0],BIOME_SIZES[1])
                self.left_biomes_ranges[-1]["end"] = x
                self.left_biomes_ranges.append({"start":x-1,"biome":choice(list(biomes_ids.values()))})
                self.left_biome_size = 0

        biome_id = 0
        found_biome = False
        for r in self.right_biomes_ranges:
            if x >= r["start"]:
                if r.get("end"):
                    if x <= r["end"]:
                        biome_id = r["biome"]
                        found_biome = True
                        break
                else:
                    biome_id = r["biome"]
                    found_biome = True
                    break

        if not found_biome:
            for r in self.left_biomes_ranges:
                if x <= r["start"]:
                    if r.get("end"):
                        if x >= r["end"]:
                            biome_id = r["biome"]
                            break
                    else:
                        biome_id = r["biome"]
                        break

        biome_data = biomes_data[biome_id]

        for y_pos in range(CHUNK_SIZE):
            for x_pos in range(CHUNK_SIZE):
                self.block_heights = {"stone":randint(15,17),"dirt":8,"deepslate":randint(46,54),"bedrock":randint(64,70)}

                final_x = x*CHUNK_SIZE+x_pos
                final_y = y*CHUNK_SIZE+y_pos

                height = int(pnoise1(final_x*biome_data["noise_data"]["amplitude_multiplier"],repeat=self.repeat_noise) * biome_data["noise_data"]["height_multiplier"])
                
                block_id = -1
                collider = True
                frame = 0
                found_ore = False
                if randint(0,100) <= 10:
                    for ore in ores_data.keys():
                        if final_y in range(ores_data[ore]["range"][0]-height,ores_data[ore]["range"][1]-height):
                            if randint(0,100) <= ores_data[ore]["chances"]:
                                block_id = ore
                                frame = choice([0,1])
                                found_ore = True
                if not found_ore:
                    if final_y >= self.block_heights["bedrock"] - height:
                        block_id = block_ids["bedrock"]

                    elif final_y >= self.block_heights["deepslate"] - height:
                        block_id = biome_data["deep_layer"]

                    elif final_y >= self.block_heights["stone"] - height:
                        block_id = block_ids["stone"]

                    elif final_y > self.block_heights["dirt"] - height:
                        block_id = choice(biome_data["bottom_layer"])

                    elif final_y == self.block_heights["dirt"]-height:
                        block_id = biome_data["top_layer"]

                    elif final_y == self.block_heights["dirt"]-height-1:
                        if randint(1,100) <= biome_data["grass_chances"]:
                            block_id = biome_data["grass_type"]
                            frame_num = frames[biome_data["grass_type"]]
                            frame = randint(0,frame_num-1)
                            collider = False
                        else:
                            if 1 < x_pos < CHUNK_SIZE-1:
                                if randint(1,100) <= biome_data["tree_chances"] and has_tree == False:
                                    tree_data = generate_structure(final_x,final_y,self.structure_b_id,biome_data["tree_type"])
                                    self.structures_data.append(tree_data[0])
                                    self.structure_b_id = tree_data[1]
                                    has_tree = True
                        if not has_tree and not has_entity:
                            if self.day_night_cycle_bg.is_day:
                                e_name = choice(biome_data["animal_entities"])
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
                ok_for_entity = False
                target_x = x - 1 + int(round(self.scroll.x/(CHUNK_SIZE*BLOCK_SIZE)))
                target_y = y - 1 + int(round(self.scroll.y/(CHUNK_SIZE*BLOCK_SIZE)))
                target_chunk = str(target_x)+";"+str(target_y)
                if target_chunk not in self.world_data:
                    self.world_data[target_chunk] = self.generate_chunk(target_x,target_y)
                    ok_for_entity = False
                else:
                    if not target_chunk in self.before_loaded_chunks:
                        ok_for_entity = True
                self.chunk_colliders.append([pygame.Rect(self.world_data[target_chunk][0]["pos"][0]*BLOCK_SIZE-self.scroll.x,self.world_data[target_chunk][0]["pos"][1]*BLOCK_SIZE-self.scroll.y,CHUNK_SIZE*BLOCK_SIZE,CHUNK_SIZE*BLOCK_SIZE),target_chunk])
                self.currently_loaded_chunks.append(target_chunk)
                for block in self.world_data[target_chunk]:
                    if block["id"] >= 0:
                        self.draw_block(block)
                        if ok_for_entity:
                            if block["id"] == 1:
                                if self.day_night_cycle_bg.is_day:
                                    e_name = choice(ENTITIES)
                                    if randint(0,100) <= entities_data[e_name]["chances"]/2:
                                        match e_name:
                                            case "porcupine":
                                                e = PorcupineEntity((block["pos"][0]*BLOCK_SIZE-self.scroll.x,block["pos"][1]*BLOCK_SIZE-self.scroll.y),e_name,self.add_drop,self.delete_entity)
                                                self.animal_entities.append(e)
                                        ok_for_entity = False
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

    def render_drops(self,dt):
        if self.drops:
            for drop in self.drops:
                if drop.rect.right > 0-BLOCK_SIZE and drop.rect.left < WIDTH+BLOCK_SIZE and drop.rect.bottom > 0-BLOCK_SIZE and drop.rect.top < HEIGHT+BLOCK_SIZE:
                    if not self.is_dead:
                        if self.player.drop_collision(drop):
                            self.drops.remove(drop)
                    drop.draw()
                    drop.update(self.rect_colliders,dt)
                    self.loaded_entities += 1

    def render_entities(self,dt):
        if self.animal_entities:
            for e in self.animal_entities:
                if e.rect.right > 0-BLOCK_SIZE*3 and e.rect.left < WIDTH+BLOCK_SIZE*3 and e.rect.bottom > 0-BLOCK_SIZE*3 and e.rect.top < HEIGHT+BLOCK_SIZE*3:
                    e.draw()
                    if not self.is_dead and not self.is_paused:
                        e.walk_animation(dt)
                        e.update(self.rect_colliders,dt)
                    self.loaded_entities += 1
                else:
                    if abs(e.rect.x) >= ENTITY_DESPAWN_RANGE:
                        e.die(False)
        if self.day_night_cycle_bg.alpha > 0:
            if self.monster_entities:
                for m in self.monster_entities:
                    if m.rect.right > 0-BLOCK_SIZE*3 and m.rect.left < WIDTH+BLOCK_SIZE*3 and m.rect.bottom > 0-BLOCK_SIZE*3 and m.rect.top < HEIGHT+BLOCK_SIZE*3:
                        m.draw()
                        if not self.is_dead and not self.is_paused:
                            m.walk_animation(dt)
                            m.update(self.rect_colliders,dt)
                        self.loaded_entities += 1
                    else:
                        if abs(m.rect.x) >= ENTITY_DESPAWN_RANGE:
                            m.die(False)

    def death_actions(self):
        draw_image(self.red_tint,(0,0))
        draw_image(self.death_img_2,(self.death_rect.topleft[0]+self.died_offset,self.death_rect.topleft[1]+self.died_offset))
        draw_image(self.death_img,self.death_rect)
        
        if self.respawn_button.draw_check():
            self.reset_world()
            self.is_dead = False

    def pause_actions(self):
        draw_image(self.pause_img_2,(self.pause_rect.topleft[0]+self.pause_offset,self.pause_rect.topleft[1]+self.pause_offset))
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

    def draw(self,dt):
        self.day_night_cycle_bg.draw_bg()
        self.day_night_cycle_bg.draw_day_night()
        # player
            
        self.render_chunks()
        self.render_structures()
        
        self.render_player_blocks()
        self.render_entities(dt)
        if not self.is_dead:
            self.player.custom_draw(dt)

        if self.is_f3:
            self.f3_menu.draw_f3_infos(self.seconds,self.last_save,self.chunk_colliders,self.rect_colliders,self.loaded_entities)
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
            self.furnace_open = False
            if self.storage_open:
                self.storages_manager.paste_slots_to_storage()
            self.storage_open = False

        if keys[pygame.K_F3] and self.can_press:
            self.is_f3 = not self.is_f3
            self.can_press = False

        if not keys[pygame.K_ESCAPE] and not keys[pygame.K_F3]:
            self.can_press = True

    def update(self,dt):
        mouse = pygame.mouse.get_pressed()
        self.render_drops(dt)

        # player

        if not self.is_dead:
            self.input()
            if not self.is_paused:
                self.day_night_cycle_bg.update_day_night(dt)
                self.furnaces_manager.passive_update()
                if not self.player.inventory_open:
                    self.mining_system.update(mouse)
                    self.build_system.update(mouse)
                    self.combat_system.update(mouse)
                else:
                    if self.crafting_open:
                        self.crafting_system.update(mouse)
                        self.crafting_system.draw()
                    elif self.furnace_open:
                        self.furnaces_manager.active_update(mouse)
                        self.furnaces_manager.draw()
                    elif self.storage_open:
                        self.storages_manager.render_slots()
                        self.storages_manager.update(mouse)
            else:
                self.last_milli = pygame.time.get_ticks()

        self.player.update(self.rect_colliders,dt,mouse)

        # refresh
        self.rect_colliders.clear()
        self.chunk_colliders.clear()
        self.free_pos_rects.clear()
        self.before_loaded_chunks = self.currently_loaded_chunks.copy()
        self.currently_loaded_chunks.clear()

        if self.is_dead:
            self.death_actions()
        elif self.is_paused:
            self.pause_actions()

        if pygame.time.get_ticks()-self.last_time >= 1000 and self.is_paused==False and self.is_dead == False:
            self.last_time=pygame.time.get_ticks()
            self.seconds+=1