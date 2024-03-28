print("Variables Defined")
from tool import Tool
import arcade, math

# DEFINE ALL THE CONSANTS FOR THE GAME TO USE

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

IMAGE_SCALING = (SCREEN_HEIGHT+SCREEN_WIDTH)//10

SCREEN_TITLE = "Don't Die"
MAP_DIMENSIONS = 15000
SPACING_VALUE = 300
RESOURCE_SPACING = (MAP_DIMENSIONS // SPACING_VALUE)**2
MOVEMENT_SPEED = 100
ROCK_HEIGHT_RANGE = [20,60]
AMOUNT_OF_ROCK_VERTICES = 20
CHAOS_FACTOR = 2
ROCK_RADII = [20,30]
HEALTH_BAR_OUTLINE_THICKNESS = 5
PLAYER_HEALTH_BAR_GAP = 20

MIN_CAMP_DISTANCE = MAP_DIMENSIONS//5

DISPLAY_TEXT_WIDTH_GAP = 5
DISPLAY_TEXT_HEIGHT_GAP = 10
GAP_BETWEEN_TEXTS = 40
TEXT_COOLDOWN = 5

DELAY_FOR_EVENING = 200
DELAY_FOR_NIGHT = 45
DELAY_FOR_DAY = 60

DELAY_FOR_NIGHT += DELAY_FOR_EVENING
DELAY_FOR_DAY += DELAY_FOR_NIGHT

DAY_TICK_COOLDOWN = 40
EVENING_TICK_COOLDOWN = 1
NIGHT_TICK_COOLDOWN = 0.5

LEVEL_ENEMY_MULTIPLIER = 0.1 # enemy stats = (1+(LEVEL_ENEMY_MULTIPLIER*level)) * base_stats
ENEMY_MAX_DISTANCE_FROM_PLAYER = 1000
ENEMY_MIN_DISTANCE_FROM_PLAYER = 500
ENEMY_TRIGGER_ATTACK_DISTANCE = 40
PLACEHOLDER_ENEMY_DIMENSIONS = 30
EXTRA_SPEED_DISTANCE = math.sqrt(SCREEN_HEIGHT**2+SCREEN_WIDTH**2)
EXTRA_SPEED_MAGNITUDE = 3

SAVE_COOLDOWN = 2

# RESOURCE ITEM DROP RATES
TREE_WOOD_RATE = [3,5]
PEBBLE_ROCK_RATE = [2,4]
ROCK_ROCK_RATE = [1,2]
IRON_ROCK_RATE = [1,3]

ATTACK_DISTANCE = 40
ATTACK_COOLDOWN = 1.5

LOADING_COOLDOWN = 0.01

HEAL_COOLDOWN = 1
HEAL_RATE = 1 # 1 health per HEAL_COOLDOWN seconds

# INVENTORY RELATED VARIABLES
INVENTORY_BIND = [arcade.key.E,arcade.key.TAB]
INVENTORY_BUTTON_WIDTH = SCREEN_WIDTH//4
INVENTORY_BUTTON_HEIGHT = SCREEN_HEIGHT//8
INVENTORY_OUTLINE_THICKNESS = SCREEN_WIDTH//20
INVENTORY_GAP = SCREEN_WIDTH//20
INVENTORY_WIDTH = SCREEN_WIDTH//1.1
INVENTORY_HEIGHT = SCREEN_HEIGHT//1.1
INVENTORY_ITEM_HEIGHT = INVENTORY_HEIGHT//10

INVENTORY_CLICK_COOLDOWN = 0.15
INVENTORY_NAVIGATION_COOLDOWN = 0.15
AMOUNT_OF_ITEMS_THAT_CAN_BE_DISPLAYED = (INVENTORY_HEIGHT-(INVENTORY_BUTTON_HEIGHT*2)-INVENTORY_ITEM_HEIGHT)//INVENTORY_ITEM_HEIGHT

TREE_IMAGE = arcade.load_texture('sprites/tree.png')
ROCK_IMAGES = []

DAY_TRACK = arcade.Sound('music/day.mp3')
EVENING_TRACK = arcade.Sound('music/evening.mp3')
DARK_TRACK = arcade.Sound('music/dark.mp3')

FOOTSTEP_SOUND = arcade.Sound('sfx/footsteps.mp3')

RIGHT_ENEMY_ANIMATION_FRAMES = []
LEFT_ENEMY_ANIMATION_FRAMES = []
ENEMY_ANIMATION_TIME = 0.1

DARK_OVERLAY = arcade.load_texture('extra/dark_overlay.png')

for x in range(1,10):
    try:
        RIGHT_ENEMY_ANIMATION_FRAMES.append(arcade.load_texture("enemy/"+str(x)+'.png'))
    except:
        pass

for x in range(1,10):
    try:
        LEFT_ENEMY_ANIMATION_FRAMES.append(arcade.load_texture("enemy/l"+str(x)+'.png'))
    except:
        pass

ROCK_SOUNDS = []

for x in range(1,10):
    try:
        ROCK_SOUNDS.append(arcade.Sound("sfx/rock"+str(x)+'.mp3'))
    except:
        pass

for x in range(1,10):
    try:
        ROCK_IMAGES.append(arcade.load_texture("sprites/simple_rock"+str(x)+'.png'))
    except:
        pass
IRON_IMAGES = []
for x in range(1,10):
    try:
        IRON_IMAGES.append(arcade.load_texture("sprites/iron_rock"+str(x)+'.png'))
    except:
        pass

CRAFTING_RECIPES = [[['wood',1],['pebble',2],'rope',1,'item'],
                    [['wood', 1], ['rock', 1], 'stick', 1, 'item'],
                    [['stick', 2], ['pebble', 4], 'handle', 1, 'item'],
                    [['stick', 2], ['rope', 1], 'reinforced stick', 1, 'item'],
                    [['reinforced stick', 1], ['handle', 1], 'tool base', 1, 'item'],
                    [['rock', 1], ['rope', 2], 'reinforced rock', 1, 'item'],
                    [['wood', 2], ['stick', 2], 'fuel', 1, 'item'],
                    [['fuel', 1], ['raw iron', 1], 'iron bar', 1, 'item'],
                    [['reinforced rock', 1], ['iron bar', 1], 'reinforced iron', 1, 'item'],
                    [['wood',2],['pebble',4],'makeshift pickaxe',1,'tool',Tool('makeshift pickaxe',['rock'],20,1.5,True)],
                    [['tool base', 1], ['reinforced iron', 2], 'steel knife', 1, 'tool',Tool('steel knife',['enemy'],20,0.75,True)],
                    [['tool base', 1], ['reinforced iron', 4], 'steel axe', 1, 'tool',Tool('steel axe',['wood'],25,1,True,0,True,0.2)],
                    [['tool base', 1], ['reinforced iron', 6], 'steel pickaxe', 1, 'tool',Tool('steel pickaxe',['rock','iron'],65,1.5,True)],
                    [['tool base', 1], ['reinforced rock', 1], 'weak knife', 1, 'tool',Tool('weak knife',['enemy'],20,0.75,True)],
                    [['tool base', 1], ['reinforced rock', 2], 'weak axe', 1, 'tool',Tool('weak axe',['wood'],10,0.75,True)],
                    [['tool base', 1], ['reinforced rock', 3], 'weak pickaxe', 1, 'tool',Tool('weak pickaxe',['rock','iron'],35,1.4,True)],
                    ]
RESOURCE_LIST = []
for recipe in CRAFTING_RECIPES:
    if not(recipe[0][0] in RESOURCE_LIST):
        RESOURCE_LIST.append(recipe[0][0])
    if not(recipe[1][0] in RESOURCE_LIST):
        RESOURCE_LIST.append(recipe[1][0])
    if not(recipe[2] in RESOURCE_LIST):
        RESOURCE_LIST.append(recipe[2])
IMAGES = {}
for resource in RESOURCE_LIST:
    try:
        filename = "sprites/"+str(resource)+".png"
        temp = arcade.load_texture(filename)
        IMAGES[resource] = temp
    except:
        pass

# The following assert statements ensure that all of the following lists that require information have something to access. There are 3 other python assert statements within this folder - search: Assert statement (ctrl/cmd + f)
assert IMAGES
assert ROCK_IMAGES
assert IRON_IMAGES
assert RIGHT_ENEMY_ANIMATION_FRAMES
assert LEFT_ENEMY_ANIMATION_FRAMES
assert ROCK_SOUNDS

# Ensures the map dimensions are valid
assert MAP_DIMENSIONS
