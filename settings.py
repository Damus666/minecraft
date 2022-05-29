import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# WINDOW

WIDTH = screensize[0]
HEIGHT = screensize[1]
MY_WIDTH = 1920
MY_HEIGHT = 1080
FPS = 60

from utility.pixel_calculator import width_calculator,height_calculator, medium_calculator

# PIXELS CONSTANTS

BLOCK_SIZE = medium_calculator(80,True)
CHUNK_SIZE = 5
ITEM_SIZE = medium_calculator(35)
SLOT_OFFSET = medium_calculator(16)
SLOT_OFFSET_H = medium_calculator(16)
SCROLL_LINE_X = WIDTH//4
SCROLL_LINE_Y = HEIGHT//5
CRAFTING_CARD_WIDTH = width_calculator(180)
CRAFTING_CARD_HEIGHT = height_calculator(100)
CRAFTING_CARD_OFFSET = medium_calculator(5)
FURNACE_SLOT_SIZE = medium_calculator(80)
MAX_DUR_WIDTH = ITEM_SIZE
DUR_HEIGHT = height_calculator(5)
BIOME_SIZES = [35,55]

# COLORS

# inventory
SLOT_COLOR = (141,140,138)
INV_BG_COLOR = (212,211,211)
DUR_BG_COLOR = (30,30,30)
# card
OUTLINE_COLOR = (200,200,200)
COMPLETE_OUTLINE_COLOR = "white"
BG_COLOR = (30,30,30)
BG_COLOR_COMPLETE = (100,100,100)


# PATHS

GRAPHICS_PATH = "assets/graphics/"
W_DATA_F = "data/worlds_data/"
FILE_NAMES = {"chunk":"chunks_data.json","structure":"structures_data.json","block":"player_blocks_data.json","drop":"drops_data.json","other":"world_data.json","entity":"entities_data.json","special":"specials_blocks_data.json"}

# GAME CONSTANTS

GRAVITY_CONSTANT = medium_calculator(0.5)
PLAYER_MINE_RANGE = BLOCK_SIZE*8
PLAYER_BUILD_RANGE = BLOCK_SIZE*5
PLAYER_HIT_RANGE = BLOCK_SIZE*5
MAX_HEALTH = 20
MAX_HUNGER = 20
SAFE_BLOCKS_NUM = 4
STACK_SIZE = 64
BLOCK_DAMAGE = 1
ENTITY_DESPAWN_RANGE = BLOCK_SIZE*1000
MONSTER_DESPAWN_RANGE = BLOCK_SIZE*500

# COOLDOWNS

HEALTH_REGEN_COOLDOWN = 20*1000
HUNGER_DECREASE_COOLDOWN = 60*1000
WALK_COOLDOWN = 500
BG_CHANGE_COOLDOWN = 20*1000
ENTITY_DIR_COOLDOWN = 10*1000
DAY_DURATION = 6*1000*60
NIGHT_DURATION = 3*1000*60
TRANSITION_DUR = 3*1000
PLAYER_DAMAGE_COOLDOWN = 0.42*1000
MOB_DAMAGE_COOLDOWN = 0.2*1000
DESPAWN_COOLDOWN = 5*1000*60
MONSTER_CREATION_COOLDOWN = 5*1000

# OTHER

ENTITIES = ["porcupine"]
MONSTERS = ["zombie","skeleton"]




