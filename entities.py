from entity import Entity

class PorcupineEntity(Entity):
    def __init__(self,start_pos,type,add_drop,delete_entity,h=None,p_f=0):
        Entity.__init__(self,start_pos,type,add_drop,delete_entity,h,p_f)

    def draw(self):
        self.draw_body()