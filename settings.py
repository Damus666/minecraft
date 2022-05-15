import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

WIDTH = screensize[0]
HEIGHT = screensize[1]
WIDTH = 1200
HEIGHT = 800
FPS = 60

BLOCK_SIZE = 80
CHUNK_SIZE = 8
ITEM_SIZE = 35
STACK_SIZE = 64

GRAPHICS_PATH = "assets/graphics/"
W_DATA_F = "data/worlds_data/"

GRAVITY_CONSTANT = 0.5
SCROLL_LINE_X = WIDTH//6
SCROLL_LINE_Y = HEIGHT//6

SLOT_COLOR = (141,140,138)
SLOT_OFFSET = 16
SLOT_OFFSET_H = 16
INV_BG_COLOR = (212,211,211)

PLAYER_MINE_RANGE = BLOCK_SIZE*8
PLAYER_BUILD_RANGE = BLOCK_SIZE*5

MAX_HEALTH = 20
MAX_HUNGER = 20
SAFE_BLOCKS_NUM = 4

HEALTH_REGEN_COOLDOWN = 20*1000
HUNGER_DECREASE_COOLDOWN = 60*1000
WALK_COOLDOWN = 500

BG_CHANGE_COOLDOWN = 20*1000

FILE_NAMES = {"chunk":"chunks_data.json","structure":"structures_data.json","block":"player_blocks_data.json","drop":"drops_data.json","other":"world_data.json"}

