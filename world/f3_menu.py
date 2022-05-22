import pygame, os, psutil, time
from utility.pixel_calculator import medium_calculator,width_calculator,height_calculator
from settings import BLOCK_SIZE,WIDTH,HEIGHT
from dict.data import blocks_data, tools_data, items_data
from pygame_helper.helper_classes import draw_image

class f3Menu:
    def __init__(self,get_selected,get_p_r,get_scroll,get_fps):
        
        self.f3_font = pygame.font.Font("assets/fonts/regular.ttf",height_calculator(30,True))
        self.f3_offset = medium_calculator(35)
        self.f3_spacing = height_calculator(10)
        ex = self.f3_font.render("CAPS",True,"white")
        self.f3_height = ex.get_height()

        self.infos = {"fps":60,"pos":(0,0),"selected":"", "time":0,"last_save":0,"render":0}
        self.extra_infos = {"ram":0,"cpu":0}
        self.extra_offset = width_calculator(500)

        self.process = os.getpid()
        self.python = psutil.Process(self.process)

        self.keys = ["Keys:","Walk: 'A' & 'D'","Jump: 'SPACE'","Pause: 'ESC'","This Menu: 'F3'","Destroy/Attack: 'MOUSE_LEFT'","Place: 'MOUSE_RIGHT'","Item Interaction: 'R'","Open Inventory: 'E'","Drop Items: 'Q'"]
        self.index_offset = height_calculator(4,True)

        self.get_selected = get_selected
        self.get_p_rect = get_p_r
        self.get_scroll = get_scroll
        self.get_fps = get_fps

    def get_pos(self):
        x = ((WIDTH//2+self.get_p_rect().x)//BLOCK_SIZE)+(self.get_scroll().x//BLOCK_SIZE)-23
        y = ((HEIGHT//2-self.get_p_rect().y)//BLOCK_SIZE)-(self.get_scroll().y//BLOCK_SIZE)
        return int(x),int(y)

    def get_memory(self):
        return "RAM: "+str(round(self.python.memory_info()[0]/1073741824,2))+" GB / "+str(round(psutil.virtual_memory()[0]/1073741824,2))+" GB"

    def get_cpu(self):
        return "CPU: "+str(round(self.python.cpu_percent()/os.cpu_count(),1))+" %"

    def draw_f3_infos(self,seconds,last_save,chunk_colliders,rect_colliders,loaded_entities):

        self.infos["fps"] = str(int(self.get_fps()))+" FPS"
        self.infos["pos"] = "X: "+str(self.get_pos()[0])+"  Y: "+str(self.get_pos()[1])
        self.infos["time"] = "Time Played: "+time.strftime("%H:%M:%S", time.gmtime(seconds))
        self.infos["last_save"] = "Last Save: "+str(int(((pygame.time.get_ticks()-last_save)/1000)/60))+" Minutes Ago"
        self.infos["render"] = "Rendering: "+str(len(chunk_colliders))+" Chunks, "+str(len(rect_colliders))+" Blocks, "+str(loaded_entities+1)+" Entities"
        try:
            if self.get_selected().empty == False:
                item = self.get_selected().item
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
            self.draw_info(WIDTH-self.extra_offset,index,self.extra_infos[info])

        for index, info in enumerate(self.keys):
            self.draw_info(0,index+6+self.index_offset,info)

    def draw_info(self,x,y_order,text):
        img = self.f3_font.render(str(text),True,"white")
        bg = pygame.Surface((img.get_width()+2.5,img.get_height()+2.5))
        bg.fill((60,60,60))
        bg.set_alpha(100)
        draw_image(bg,(x+self.f3_offset-1.25,self.f3_offset+self.f3_height*y_order+self.f3_spacing*y_order-1.25))
        draw_image(img,(x+self.f3_offset,self.f3_offset+self.f3_height*y_order+self.f3_spacing*y_order))