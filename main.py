from pygame_helper.pygame_helper import *
from settings import WIDTH,HEIGHT,FPS, W_DATA_F
from world import World
import time, sys, os, string
from main_menu import MainMenu
from random import choice

screen = init_setup(WIDTH,HEIGHT,"PyCraft",True)
clock = pygame.time.Clock()

class Game:
    def __init__(self):        
        
        self.in_game = False
        self.world = None
        self.world_index = 0
        self.worlds = []
        
        self.main_menu = MainMenu(screen,self.quit, self.play_world,self.delete_world,self.new_world)

    def generate_id(self,lenght):
        str = string.ascii_lowercase+string.ascii_uppercase+string.digits+"_"
        id = "".join(choice(str)for i in range(lenght))
        return id

    def delete_folder(self,name):
        if os.path.exists(W_DATA_F+name):
            file_list = os.listdir(W_DATA_F+name)
            for file in file_list:
                os.remove(W_DATA_F+name+"/"+file)
            os.rmdir(W_DATA_F+name)

    def create_folder(self,name):
        if not os.path.exists(W_DATA_F+name):
            os.mkdir(W_DATA_F+name)

    def play_world(self,id):
        found = False
        for index,world in enumerate(self.worlds):
            if world.id == id:
                self.world_index = index
                found = True
                break
        if not found:
            world = World(screen,id,self.exit_world,clock.get_fps,self.create_folder)
            self.worlds.append(world)
        self.world = self.worlds[self.world_index]
        self.in_game = True

    def exit_world(self):
        self.in_game = False

    def delete_world(self,id):
        for world in self.worlds:
            if world.id == id:
                self.worlds.remove(world)
                break
        self.delete_folder(id)

    def new_world(self):
        id = self.generate_id(10)
        self.create_folder(id)
        world = World(screen,id,self.exit_world,clock.get_fps,self.create_folder)
        self.worlds.append(world)
        return world.id

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self,dt):
        
        if self.in_game:
            self.world.draw()
            self.world.update(dt)
        else:
            self.main_menu.draw_update()

game = Game()
last_time = time.time()

while True: 
    dt = time.time()-last_time
    dt *= FPS
    last_time = time.time()

    for event in get_events():
        if event.type == pygame.QUIT:
            if not game.in_game:
                game.main_menu.save_cards()
            pygame.quit()
            sys.exit()

        if game.in_game:
            if event.type == MOUSEWHEEL and not game.world.is_dead and not game.world.is_paused:
                game.world.player.hotbar.scroll_mousewheel(-event.y)

        else:
            if game.main_menu.is_selecting_world:
                game.main_menu.input_event(event)

    fill_window((0,180,255))

    game.run(dt)
    #debug(int(clock.get_fps()))

    pygame.display.update()
    clock.tick(FPS)
    

