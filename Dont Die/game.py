import arcade,random,math,time,keyboard
import save_method # Module 5 - uses return and parameters (Search for Module 6 for the other module thautilises return and parameters)

# IMPORTING MODULES - THIS NEEDS TO HAVE A VERY SPECIFIC ORDER TO AVOID CIRCULAR IMPORTS AND UNDEFINE VARIABLES

# 1 - Tool first as it doesnt need ANY modules to run
from tool import Tool # Module 1

# 2 - Game Settings And Variables - Requires the tool object to run
global game_settings
import game_settings
from game_settings import *

assert SCREEN_HEIGHT > 0 and SCREEN_WIDTH > 0 and SCREEN_TITLE # Assert statement 3aa: Ensuring the screen dimension are valid and that the game has a title

# 3 - Loading Class, requires game settings to be set up
global Loading
from loading import Loading # Module 2


def initiate_modules():
    global Resource 
    from resources import Resource # Import the Resource class > Module 3

    global Menu
    from menu import Menu # Import the Menu class > Module 4


def unit_vector(speed,goal_position,current_position,delta_time=1):
    """
    Find the vector going between two positions, and reduces it to a certain length
    
        Parameters:
            speed (float): The desired length of the final vector in pixels
            goal_position (list): A two dimensional coordinate of the original vector's end position
            current_position (list): The vector's start position as a two dimensional coordinate
            delta_time (float): The time since the last update, used for making movement smooth, ignore if uneccessary
        
        Returns:
            new_position (list): A two dimensional coordinate of where the object should be now after having applied the vector to it.
    """
    displacement_vector = [goal_position[0] - current_position[0], goal_position[1] - current_position[1]] # Calculate the vector from the current pos to end pos
    displacement_magnitude = math.sqrt(displacement_vector[0]**2 + displacement_vector[1]**2) # Find the length of the vecotr just found
    unit_vector = [0,0] 
    try:
        assert displacement_magnitude != 0 # Assert Statement 2 - division by 0 error avoidance
        unit_vector[0] = (displacement_vector[0] / displacement_magnitude) # Dividing the x component of the vector by its magnitude to make it a unit vector
    except:
        pass
    try:
        assert displacement_magnitude != 0 # Assert Statement 2 - division by 0 error avoidance
        unit_vector[1] = (displacement_vector[1] / displacement_magnitude) # Dividing the y component of the vector by its magnitude to make it a unit vector
    except:
        pass
    distance_to_move = delta_time * speed # Find the distance to move by multiplying delta time by speed (the desired length of the outcome vector)
    if distance_to_move >= displacement_magnitude:
        return goal_position # If the distance to move (desired length of vector) is greater than the distance from the start to end pos, simply return the position of the end goal so the object doesnt go past its end goal
    else:
        if displacement_magnitude >= EXTRA_SPEED_DISTANCE: # Multiply the distance to move if the displacement vector's length is more than the constant EXTRA_SPEED_DISTANCE (used to speed enemies up if they are out of the screen)
            distance_to_move = distance_to_move * EXTRA_SPEED_MAGNITUDE
        new_position = [current_position[0]+unit_vector[0] * distance_to_move,current_position[1]+unit_vector[1] * distance_to_move] # Calculates the new position of the object by adding the unity vector multiplied by the distance to move to the original position
        return new_position
class Player(arcade.Sprite):
    """
    A class used to represent the Player.
    """
    def update(self):
        """ Move the player """

        # Check if the player is leaving the screen (i intend to use this when the player reaches the end of the map)
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1
        





def calculate_distance(pos1, pos2):
    """
    Calculates the distance between pos1 and pos2
    """
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

class Enemy():
    """
    A class used to represent an enemy
    
    (Most attributes are randomly generated in the __init__ function)
    
    Attributes
    ----------
    global_pos (list): The global position of the player, used to generate the enemy a safe distance from the player
    (Recomended but Optional)
    level (int): The player's current level, used to make enemies harder the higher the number
    (Not recomended and Optional)
    generate_enemy (bool): False if you want to generate the enemy yourself. If you choose to do this, you must fill in all the other optional parameters, which are straightforward
    """
    def __init__(self,global_pos,generate_enemy=True,level=0,health=100,pathfinding_type=1,stat_type=1):
        """
        Generate the Enemy
        """
        self.pathfinding_methods = ['straight'] # Waas supposed to be a list of possible pathfinding methods but i didnt have time for that
        self.possible_stats = [[10,50,20],[20,20,20],[5,10,60],[30,50,8]] # Statistics to choose from 0 = attack dmg, 1 = health, 2 = enemy speed
        if generate_enemy: 
            self.pathfinding_method = random.choice(self.pathfinding_methods) # Choose a pathfinding method (only 1 right now)
            self.stats = random.choice(self.possible_stats) # Choose a random set of statistics
        else:
            self.pathfinding_method = pathfinding_type
            self.stats = stat_type

        self.attack = self.stats[0] * (1+(LEVEL_ENEMY_MULTIPLIER*level)) # Setting the enemie's statistics
        self.health = self.stats[1] * (1+(LEVEL_ENEMY_MULTIPLIER*level)) # <
        self.speed = self.stats[2] * (1+(LEVEL_ENEMY_MULTIPLIER*level)) # <

        self.last_animation_frame = 0
        self.last_attack = 0
        self.current_animation_frame = 0

        temporaray_point = [random.randint(-ENEMY_MAX_DISTANCE_FROM_PLAYER,ENEMY_MAX_DISTANCE_FROM_PLAYER),random.randint(-ENEMY_MAX_DISTANCE_FROM_PLAYER,ENEMY_MAX_DISTANCE_FROM_PLAYER)] # Calculating a possible point for the enemy to be
        while calculate_distance(temporaray_point,[global_pos[0],global_pos[1]]) < ENEMY_MIN_DISTANCE_FROM_PLAYER or calculate_distance(temporaray_point,[global_pos[0],global_pos[1]]) > ENEMY_MAX_DISTANCE_FROM_PLAYER: # If the enemy is too far or too close to the player, re-calcualte a possible point
            temporaray_point = [global_pos[0]+random.randint(-ENEMY_MAX_DISTANCE_FROM_PLAYER,ENEMY_MAX_DISTANCE_FROM_PLAYER),global_pos[1]+random.randint(-ENEMY_MAX_DISTANCE_FROM_PLAYER,ENEMY_MAX_DISTANCE_FROM_PLAYER)]
        # multi_temp = random.randint(1,2)
        # if multi_temp == 2:
        #     multi_temp = -1
        # x_deviation = random.randint(ENEMY_MIN_DISTANCE_FROM_PLAYER,ENEMY_MAX_DISTANCE_FROM_PLAYER) * multi_temp
        # multi_temp = random.randint(1,2)
        # if multi_temp == 2:
        #     multi_temp = -1
        # y_deviation = random.randint(ENEMY_MIN_DISTANCE_FROM_PLAYER,ENEMY_MAX_DISTANCE_FROM_PLAYER) * multi_temp
        self.position = temporaray_point
    def draw_enemy(self,global_position):
        """
        Draw the enemy taking in account the player's position
        """
        global_position = list(global_position)
        center_x = global_position[0] - self.position[0] + SCREEN_WIDTH//2
        center_y = global_position[1] - self.position[1] + SCREEN_HEIGHT//2
        if time.time() >= self.last_animation_frame+ENEMY_ANIMATION_TIME:
            self.current_animation_frame += 1 # Change the current fram of the animation of the cooldown has refreshed
            self.last_animation_frame = time.time()
            if self.current_animation_frame > len(RIGHT_ENEMY_ANIMATION_FRAMES)-1:
                self.current_animation_frame = 0
        if self.position[0] >= global_position[0]: # If the enemy is to the left of the player, draw them as facing right
            arcade.draw_scaled_texture_rectangle(center_x,center_y,RIGHT_ENEMY_ANIMATION_FRAMES[self.current_animation_frame],1)
        else: # If the enemy is to the right of the player, draw them as facing left
            arcade.draw_scaled_texture_rectangle(center_x,center_y,LEFT_ENEMY_ANIMATION_FRAMES[self.current_animation_frame],1)
        # if center_x - PLACEHOLDER_ENEMY_DIMENSIONS >= 0 and center_x + PLACEHOLDER_ENEMY_DIMENSIONS <= SCREEN_WIDTH and center_y + PLACEHOLDER_ENEMY_DIMENSIONS >= 0 and center_y - PLACEHOLDER_ENEMY_DIMENSIONS <= SCREEN_HEIGHT:
        #     arcade.draw_rectangle_filled(center_x,center_y,PLACEHOLDER_ENEMY_DIMENSIONS,PLACEHOLDER_ENEMY_DIMENSIONS,arcade.color.RED)
    def move_to(self,global_pos,delta_time):
        """
        Move the enemy towards the player
        
            Parameters:
                global_pos (list): The player's global position
                delta_time (float): The last time since an update"""
        if self.pathfinding_method == 'straight':
            moving_vector = unit_vector(self.speed,global_pos,self.position,delta_time) # Calculat the position to move to by using the unit_vector() function
            self.position = moving_vector
    def mind(self,global_pos,delta_time):
        """
        The enemy will perform movement automatically with the given parameters.
        """
        if self.pathfinding_method == 'straight':
            self.move_to(global_pos,delta_time)
        if calculate_distance(self.position,[global_pos[0],global_pos[1]]) <= ATTACK_DISTANCE and time.time() >= self.last_attack + ATTACK_COOLDOWN:
            self.last_attack = time.time()
            return self.attack # If the enemy is close enough to the player and it's attack cooldown has refreshed return the damage it deals for the player to take that as damage
    def detect_hit(self,global_position,mouse_position,damage):
        """
        Detect if the enemy is hit, and if so deal a certain amount of damage
        """
        center_x = global_position[0] - self.position[0] + SCREEN_WIDTH//2
        center_y = global_position[1] - self.position[1] + SCREEN_HEIGHT//2
        hit = False
        dead = False
        # print([center_x,center_y],mouse_position)
        if mouse_position[0] >= center_x-40 and mouse_position[0] <= center_x+40 and mouse_position[1] >= center_y-40 and mouse_position[1] <= center_y+40:
            hit = True # If the mouse clicked the enemy, set hit to True
            moving_vector = unit_vector(-50,global_position,self.position,1) # Calculate the position of the enemy after taking knockback
            self.position = moving_vector
            self.health -= damage
            if self.health <= 0:
                dead = True
        return [hit,dead] # 0 = Was the enemy hit 1 = is the enemy dead? (used for removing that enemy object from the enemies list)


    # def pathfind() 
def draw_inventory():
    """
    Draw the base inventory/crafting UI
    """
    arcade.draw_rectangle_filled(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,INVENTORY_WIDTH,INVENTORY_HEIGHT,arcade.color.GHOST_WHITE)
    arcade.draw_rectangle_filled(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,INVENTORY_WIDTH-INVENTORY_OUTLINE_THICKNESS,INVENTORY_HEIGHT-INVENTORY_OUTLINE_THICKNESS,arcade.color.GRAY)
def draw_button(highlighted,inventory_type,button_number,text):
    """
    Draw a button in the inventory/crafting UI
    """
    left_most_x = (SCREEN_WIDTH-INVENTORY_WIDTH)//2+INVENTORY_OUTLINE_THICKNESS//2 + (button_number*INVENTORY_BUTTON_WIDTH)
    top_most_y = SCREEN_HEIGHT - (SCREEN_HEIGHT-INVENTORY_HEIGHT)//2-INVENTORY_OUTLINE_THICKNESS//2
    if inventory_type == highlighted:
        arcade.draw_lrtb_rectangle_filled(left_most_x,left_most_x+INVENTORY_BUTTON_WIDTH,top_most_y,top_most_y-INVENTORY_BUTTON_HEIGHT,arcade.color.ALLOY_ORANGE)
    else:
        arcade.draw_lrtb_rectangle_filled(left_most_x,left_most_x+INVENTORY_BUTTON_WIDTH,top_most_y,top_most_y-INVENTORY_BUTTON_HEIGHT,arcade.color.DIM_GRAY)
    arcade.draw_text(str(text),left_most_x+(INVENTORY_BUTTON_WIDTH//2),top_most_y-INVENTORY_BUTTON_HEIGHT//2,arcade.color.WHITE,24,anchor_x='center',anchor_y='center')
def show_items(item,amount,number=0):
    """
    Show an item or tool in the inventory
    
        Parameters:
            amount (int): Amount of the item
            numebr (int): The number that the item has in the inventory; used for displaying purposes"""
    top_most_y = SCREEN_HEIGHT - (SCREEN_HEIGHT-INVENTORY_HEIGHT)//2-INVENTORY_OUTLINE_THICKNESS//2-INVENTORY_BUTTON_HEIGHT-(INVENTORY_ITEM_HEIGHT*number)
    if item in list(IMAGES.keys()): # If the item has a corrseponding image, draw it VVVV
        left_most_x = (SCREEN_WIDTH-INVENTORY_WIDTH)//2+INVENTORY_OUTLINE_THICKNESS//2
        arcade.draw_lrwh_rectangle_textured(left_most_x,top_most_y-INVENTORY_ITEM_HEIGHT,INVENTORY_ITEM_HEIGHT,INVENTORY_ITEM_HEIGHT,IMAGES[item])
        left_most_x = (SCREEN_WIDTH-INVENTORY_WIDTH)//2+INVENTORY_OUTLINE_THICKNESS//2+(INVENTORY_ITEM_HEIGHT)
    else:
        left_most_x = (SCREEN_WIDTH-INVENTORY_WIDTH)//2+INVENTORY_OUTLINE_THICKNESS//2
    arcade.draw_text(str(item),left_most_x,top_most_y,arcade.color.WHITE,24,anchor_x='left',anchor_y='top')
    if amount != 1: # If the amount of the item is not 1, display how much of that item the player has to the left of the item
        arcade.draw_text("x"+str(amount),SCREEN_WIDTH-INVENTORY_OUTLINE_THICKNESS-INVENTORY_GAP,top_most_y,arcade.color.WHITE,24,anchor_x='right',anchor_y='top')
def show_crafting_ui(item1,item2,item1_amount,item2_amount):
    """
    Displays the text showing the two items the player is combining in the crafting UI
    """
    left_most_x = (SCREEN_WIDTH-INVENTORY_WIDTH)//2+INVENTORY_OUTLINE_THICKNESS//2
    bottom_most_y = INVENTORY_GAP+INVENTORY_OUTLINE_THICKNESS
    outcome = ""
    outcome_amount = ""
    for recipe in CRAFTING_RECIPES: 
        if [item1,item1_amount] in recipe and [item2,item2_amount] in recipe and [item1,item1_amount] != [item2,item2_amount]:
            outcome = recipe[2] # If  items in the crafting slots make something, set the outcome item to this variable and the amount of that item to the below one
            outcome_amount = str(recipe[3])
    arcade.draw_text("("+str(item1_amount)+") "+str(item1).upper()+" + ("+str(item2_amount)+") "+str(item2).upper()+" >> "+str(outcome).upper() + " ("+str(outcome_amount)+")",left_most_x,bottom_most_y,arcade.color.WHITE,24,anchor_x='left',anchor_y='top',font_name='calibri') # Draw the items being combined and the resultant item and amount (if applicable)
def detect_inventory_button_press(button_number,mouse_position):
    """
    Detects if the player has clicked on a button
    """
    left_most_x = (SCREEN_WIDTH-INVENTORY_WIDTH)//2+INVENTORY_OUTLINE_THICKNESS//2 + (button_number*INVENTORY_BUTTON_WIDTH)
    top_most_y = SCREEN_HEIGHT - (SCREEN_HEIGHT-INVENTORY_HEIGHT)//2-INVENTORY_OUTLINE_THICKNESS//2
    clicked = False
    if mouse_position[0] >= left_most_x and mouse_position[0] <= left_most_x+INVENTORY_BUTTON_WIDTH and mouse_position[1] <= top_most_y and mouse_position[1] >= top_most_y-INVENTORY_BUTTON_HEIGHT:
        clicked = True # If the mouse is within the coordinates of the button, set clicked to True
    return clicked
def detect_inventory_item_clicked(item_number,mouse_position):
    """
    Detects if the player has clicked on an item or tool in the inventory
    """
    clicked = False
    left_most_x = (SCREEN_WIDTH-INVENTORY_WIDTH)//2+INVENTORY_OUTLINE_THICKNESS//2
    top_most_y = SCREEN_HEIGHT - (SCREEN_HEIGHT-INVENTORY_HEIGHT)//2-INVENTORY_OUTLINE_THICKNESS//2-INVENTORY_BUTTON_HEIGHT-(INVENTORY_ITEM_HEIGHT*item_number)
    if mouse_position[0] >= left_most_x and mouse_position[0] <= left_most_x+INVENTORY_WIDTH-INVENTORY_OUTLINE_THICKNESS and mouse_position[1] <= top_most_y and mouse_position[1] >= top_most_y-INVENTORY_ITEM_HEIGHT:
        clicked = True # If the item was clicked, set clicked to true, and draw a white rectangle over it for quality of life to show that the player pressed it VVVV
        arcade.draw_lrtb_rectangle_filled(left_most_x,left_most_x+INVENTORY_WIDTH-INVENTORY_OUTLINE_THICKNESS,top_most_y,top_most_y-INVENTORY_ITEM_HEIGHT,arcade.color.WHITE)
    return clicked
def draw_craft_button(mouse_pressed,mouse_position):
    '''
    Draw the "Craft" button
    '''
    clicked = False
    left_most_x = (SCREEN_WIDTH-INVENTORY_WIDTH)//2+INVENTORY_OUTLINE_THICKNESS//2
    bottom_most_y = INVENTORY_GAP+INVENTORY_OUTLINE_THICKNESS
    if mouse_pressed:
        if mouse_position[0] >= left_most_x and mouse_position[0] <= left_most_x+INVENTORY_BUTTON_WIDTH and mouse_position[1] >= bottom_most_y and mouse_position[1] <= bottom_most_y+INVENTORY_BUTTON_HEIGHT:
            clicked = True
    if clicked:
        arcade.draw_lrtb_rectangle_filled(left_most_x,left_most_x+INVENTORY_BUTTON_WIDTH,bottom_most_y+INVENTORY_BUTTON_HEIGHT,bottom_most_y,arcade.color.ALLOY_ORANGE)
    else:
        arcade.draw_lrtb_rectangle_filled(left_most_x,left_most_x+INVENTORY_BUTTON_WIDTH,bottom_most_y+INVENTORY_BUTTON_HEIGHT,bottom_most_y,arcade.color.DIM_GRAY)
    arcade.draw_text("Craft",left_most_x+INVENTORY_BUTTON_WIDTH//2,bottom_most_y+(INVENTORY_BUTTON_HEIGHT//2),arcade.color.WHITE,24,font_name='calibri',anchor_x='center',anchor_y='center')
    return clicked


class MyGame(arcade.Window):

    """
    The main game class object, inherting the arcade.Winow class
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Inherit the parent class's initialiser
        super().__init__(width, height, title)

        # variable that holds sprite lists
        self.player_list = None 

        # Set up the player info
        self.player_sprite = None


        # Track what key is pressed

        self.left_pressed = False

        self.right_pressed = False

        self.up_pressed = False

        self.down_pressed = False

        

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        global savegame # make savegame global so that other functions can use it
        import savegame # Import this now to avoid circular import error (Module 6 > returns values and utilises parameters, and used for assisting with user acceptance testing to save data)
        # ^ USED TO HELP WITH USER ACCEPTANCE TESTING (UAT, UAF)
    def setup(self,resources,extra_data,previous_data=False):
        
        """
        Setting up the game window
        
            Parameters:
                resources (list): List of Resource class objects
                extra_data (json): Json string of previously saved game data (use None if not needed)
                previous_data (bool): If true, load the previous game using the extra_data argument
        """

        self.debugging = False
        with open('debug/debug.txt') as file:
            data = file.read()
            if data == "1" or data == "2":
                self.debugging = True

        if not(previous_data): # Previous data wiill be given if the game i sbeing loaded from a previous save

            self.player_list = arcade.SpriteList()

            # Setting up the player
            self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                        SPRITE_SCALING)
            self.player_sprite.center_x = SCREEN_WIDTH // 2
            self.player_sprite.center_y = SCREEN_HEIGHT // 2
            self.player_list.append(self.player_sprite)

            self.resources = resources # Resources generated by the loading window
            self.global_position = [0,0] # The position of the player relative to the point (0,0). WHen the player moves, instead of moving along the screen, this realtive position changes

            # Player items
            self.current_tool = Tool('fists','wood',5,0.75,True,1,True,1) # The player's equipped tool
            self.inventory = {}#{"reinforced rock":10,"tool base":6,'rock':50,'wood':100,'pebble':100,"reinforced iron":20} # The player's inventory
            self.player_tools = {'fists':[1,Tool('fists','wood',5,0.75,True,1,True,1)]} # A dictionary of all the tools that the player has
            self.max_health = 100 # The maximum health the player can have, used for the health bar to know the maximum value and for healing (if implemented)
            self.player_health = self.max_health # Setting the player's health

            self.start_time = time.time() # The time that the game was started
            self.dawn_time = time.time() # The time when a day starts, used for determining when the next phases, evening and night, will occur
            self.current_phase = 'day' # The game's current day-night cycle phase
            self.level = 1 # The current level - affected by the amount of nights survived, used to make enemies more challenging the greater the number

            self.crafting = False # If the player has the inventory UI open
            self.inventory_type = 'item' # The filter applied to the inventory, e.g. "item" => only items are displayed
            self.crafting_items = [['None',0],['None',0]] # The two items placed in the crafting UI
            self.crafting_spot_to_fill = 0 # Used to alternate which crafting spot an item will fill
            self.text_displayed = [] # A list of messages to announce, each with the time at which they were initiated to know when to remove them according to the text cooldown constant
            self.craft_click_cooldown = time.time() # The last time a click was made in the inventory, combined with the inventory click cooldown constant, ensures only single clicks can happen
            self.last_inventory_navigate = time.time() # The last time the player clicked UP or DOWN in the inventory to scroll the items, paired with a cooldown constant, makes it so that the player doesnt scroll too fast
            self.inventory_navigation_number = 0 # The number of times the inventory was scrolled down. E.g. DOWN pressed twice, this variable will be 2

            self.last_tick = time.time() # The last time an enemy was spawned, used with cooldowns
            self.enemies = [] # A list of all Enemy() class objects in the game

            self.mouse_pressed = False # bool if the mouse is pressed in the current frame
            self.mouse_position = [0,0]
            self.mine_cooldown = time.time() # Last time a player used a tool, used so that tools have cooldowns 

            self.last_loading_tick = 0
            self.load_rotation = 0

            self.bg_music = DAY_TRACK.play(0.5,0,True) # Play the day music
            self.footstep_sfx = FOOTSTEP_SOUND.play(0.5,0,True,0.8)

            self.camp_position = [0,0]

            # USED FOR DEBUGGING - visit MARKERREADME.txt for more info
            with open('debug/debug.txt') as file:
                
                data = file.read()
                if data == "0":
                    pass
                if data == "1" or data == "2":
                    self.debugging = True
                    print("DEBUG MODE DETECTED: DISPLAYING RECIPES")
                    for recipe in CRAFTING_RECIPES:
                        print(str(recipe[0][1])+" "+recipe[0][0]+" + "+str(recipe[1][1])+" "+recipe[1][0]+" => "+str(recipe[3])+" "+recipe[2])
                    if data == "2":
                        print("\n GRANTING PLAYER EXTRA ITEMS")
                        self.inventory = {"reinforced rock":10,"tool base":6,'rock':50,'wood':100,'pebble':100,"reinforced iron":20}

        else:
            self.player_list = arcade.SpriteList()
            # Setting up the player
            self.player_sprite = Player(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                        SPRITE_SCALING)
            self.player_sprite.center_x = SCREEN_WIDTH // 2
            self.player_sprite.center_y = SCREEN_HEIGHT // 2
            self.player_list.append(self.player_sprite)

            self.current_tool = Tool('fists','wood',5,0.75,True,1,True,1)

            self.bg_music = DAY_TRACK.play(0.5,0,True) # Play the day music
            self.footstep_sfx = FOOTSTEP_SOUND.play(0.5,0,True,0.8)

            if self.debugging:
                print("DEBUG MODE DETECTED: DISPLAYING RECIPES")
                for recipe in CRAFTING_RECIPES:
                    print(str(recipe[0][1])+" "+recipe[0][0]+" + "+str(recipe[1][1])+" "+recipe[1][0]+" => "+str(recipe[3])+" "+recipe[2])


            self.enemies = []
            self = save_method.load_saved_data(save_method.GameData(),extra_data,self) # Inheriting the self object from another class that has loaded all the neccessary data for the game to run



        self.last_autosave = 0
        self.in_camp = False
        self.last_heal = 0



    def show_messages(self,adding_to_list=False,message='',display_type='',collected_items=[]):
        """Displays all the messages given, and removes them if they hae exceeded their cooldown time."""
        if adding_to_list: # Used for adding elements to the list of messages
            if display_type == 'item': # If the function was given a list of items, add each item and the amount gained to the list of messages
                for a in collected_items:
                    self.text_displayed.append(["× "+str(a[1])+" "+str(a[0]),time.time()+TEXT_COOLDOWN]) # Item 0 = Text to be displayed, Item 1 = time the text was wrote (text dissapear after TEXT_COOLDOWN seconds)
            elif display_type == 'custom' or not(display_type): # if the message given is just a plain message, add it to the list of messages
                self.text_displayed.append([str(message),time.time()+TEXT_COOLDOWN])
        else:
            message_num = 0
            for message in self.text_displayed:
                if time.time() >= message[1]: # message[1] = the time the message was initiated
                    self.text_displayed.pop(message_num) # If current time is greater than when the message was initiated + TEXT_COOLDOWN, remove the message from the list of messages
                    message_num -= 1
                else: #V If the message hasnt exceeded the time cooldown, draw the message
                    arcade.draw_text(message[0], DISPLAY_TEXT_WIDTH_GAP, DISPLAY_TEXT_HEIGHT_GAP+(message_num*GAP_BETWEEN_TEXTS), arcade.color.BLACK, 24)
                message_num += 1
    def compact_data(self):
        """Takes the self object and returns a dictionary useable for saving"""
        data = save_method.save_data(self)
        return data
    def autosave(self):
        """Saves the game data"""
        savegame.GameData.save(self.compact_data(),0)

    def tick(self):
        """Called constantly, determines if an enemy should spawn and spawns one if needed."""
        spawn_enemy = False
        if self.current_phase == 'day' and time.time() >= self.last_tick + DAY_TICK_COOLDOWN/self.level: # If it is day and the last tick was more than DAY_TICK_COOLDOWN seconds ago, spawn an enemy
            spawn_enemy = True
        elif self.current_phase == 'evening' and time.time() >= self.last_tick + EVENING_TICK_COOLDOWN/(self.level/2): # If it is eveing and the last tick was more than EVENING_TICK_COOLDOWN seconds ago, spawn an enemy
            spawn_enemy = True
        elif self.current_phase == 'dark' and time.time() >= self.last_tick + NIGHT_TICK_COOLDOWN/(self.level/2): # If it is dark and the last tick was more than NIGHT_TICK_COOLDOWN seconds ago, spawn an enemy
            spawn_enemy = True
        if spawn_enemy: # If an enemy is to be spawned, do the following:
            temp_global_position = list(self.global_position) # create a copy of the global position (used to avoid an obscure variable assignment bug)
            new_enemy = Enemy(temp_global_position,True,self.level) # Creates a new Enemy() class, and stores it in a variable
            self.enemies.append(new_enemy) # adds this new enemy to the list of enemies
            self.last_tick = time.time() # updates the last time an enemy was spawned
    def on_draw(self):
        """
        Draw everything neccessary on the screen.
        """
        # Clear the screen
        if self.player_health <= 0:
            arcade.close_window() # Close the currebt game window
            if not(self.debugging):
                save_method.remove_save(0) # Preserve the save file if the game is in debug mode, so that the data can be analysed (see MARKERREADME.txt)
            death_screen = Death(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,time.time()-self.start_time,self.level) # Open the death screen
            arcade.run()
        arcade.start_render()
        self.clear()

        # Draw everything needed, resources by y height, then ui elements on top
        sorted_resources = sorted(self.resources, key=lambda resource: resource.pos[1]) # AI Assisted
        player_drawn = False
        for resource in sorted_resources:
            resource.draw_resource(self.global_position) # Drawing a resource
            if self.global_position[1] - resource.pos[1] >= SCREEN_HEIGHT//2-self.player_sprite.height*3 and not(player_drawn):
                player_drawn = True # Draw the player if the last resource drawn was above the center of the screen (where the player is drawn)
                self.player_list.draw()
        if not(player_drawn):
            self.player_list.draw()
        for enemy in self.enemies:
            temp_position = list(self.global_position)
            enemy.draw_enemy(list(temp_position))
        displayed_information = False
        for resource in self.resources:
            health_bar = resource.display_health(self.mouse_position,self.global_position)
            if health_bar:
                displayed_information = True
        if displayed_information and not(self.crafting):
            self.set_mouse_visible(False) # If the mouse is hovering over something, hide the mouse cursor to make it look cleaner
        else:
            self.set_mouse_visible(True)
        if self.current_phase == 'evening':
            arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,DARK_OVERLAY,0,120) # Drawing the darkness overlay
        elif self.current_phase == 'dark':
            arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,DARK_OVERLAY,0,255)# Drawing the darkness overlay
        if calculate_distance(self.camp_position,[self.global_position[0]+SCREEN_WIDTH//2,self.global_position[1]+SCREEN_HEIGHT//2]) > SCREEN_HEIGHT//2 and self.current_phase == 'dark':
            arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,DARK_OVERLAY,0,255)# Drawing the darkness overlay
            arcade.draw_text("Reduce Distance To Camp",SCREEN_WIDTH//2,SCREEN_HEIGHT//1.2,arcade.color.RED,SCREEN_HEIGHT/20,anchor_x='center',anchor_y='center')
        
        arcade.draw_lrtb_rectangle_filled(SCREEN_WIDTH-SCREEN_WIDTH//2,SCREEN_WIDTH-PLAYER_HEALTH_BAR_GAP,SCREEN_HEIGHT//20+PLAYER_HEALTH_BAR_GAP,PLAYER_HEALTH_BAR_GAP,arcade.color.GRAY) # Drawing the health bar
        # ^ Draws the gray section of the health bar
        x_gap = (SCREEN_WIDTH-PLAYER_HEALTH_BAR_GAP) - (SCREEN_WIDTH-SCREEN_WIDTH//2)
        percent_filled = self.player_health/self.max_health
        green_section_length = x_gap * percent_filled
        left_side = SCREEN_WIDTH-SCREEN_WIDTH//2
        arcade.draw_lrtb_rectangle_filled(left_side,left_side+green_section_length,SCREEN_HEIGHT//20+PLAYER_HEALTH_BAR_GAP,PLAYER_HEALTH_BAR_GAP,arcade.color.ANDROID_GREEN)
        # ^ Draws the green section of the health bar
        arcade.draw_text(str(self.player_health),(SCREEN_WIDTH-SCREEN_WIDTH//2),SCREEN_HEIGHT//20+PLAYER_HEALTH_BAR_GAP,arcade.color.DIM_GRAY,20,anchor_x='left',anchor_y='top')
        self.show_messages()
        if self.crafting: # OPEN CRAFTING MENU
            
            draw_inventory()
            buttons = [['item','Items'],['tool','Tools']]
            number = 0
            for button in buttons:
                draw_button(self.inventory_type,button[0],number,button[1]) # Draw the inventory filtering buttons
                number += 1
            if self.inventory_type == 'item': # Run if the inventory is filtering for only items
                number = 0
                actual_number = 0
                for item in list(self.inventory.keys()):
                    if actual_number >= self.inventory_navigation_number and number < AMOUNT_OF_ITEMS_THAT_CAN_BE_DISPLAYED:
                        show_items(item,self.inventory[item],number) # If the item is within the displayable range of the inventory, display it
                        number += 1
                    actual_number += 1
                if number == 0 and self.inventory_navigation_number > 0:
                    self.inventory_navigation_number -= 1 # Failsafe so if that no item can be shown, automatically scroll up
                if self.mouse_pressed:
                    number1 = 0
                    for item1 in list(self.inventory.keys()):
                        if number1-self.inventory_navigation_number >=0 and number1-self.inventory_navigation_number < AMOUNT_OF_ITEMS_THAT_CAN_BE_DISPLAYED:
                            if detect_inventory_item_clicked(number1-self.inventory_navigation_number,self.mouse_position): # If the item is clicked
                                second_number = 0
                                duplicate_number = 0
                                found_duplicate = False
                                for crafting_item in self.crafting_items:
                                    if crafting_item[0] == item1:
                                        found_duplicate = True # If the item selected is already in a crafting slot, set this varaible to True
                                        duplicate_number = second_number
                                    second_number += 1
                                if found_duplicate and time.time() >self.craft_click_cooldown+INVENTORY_CLICK_COOLDOWN and self.crafting_items[duplicate_number][1] < self.inventory[item1]:
                                    #                       ^ If click isnt on cooldown             ------->                            ^ If the amount of the item in the crafting ui is smaller than the amount of the item owned
                                    self.crafting_items[duplicate_number][1] += 1 # The program found that the selected item existed in a crafting spot, so it simply adds 1 to the amount of that item in the crafting slot
                                    self.craft_click_cooldown = time.time()
                                elif time.time() >self.craft_click_cooldown+INVENTORY_CLICK_COOLDOWN and self.inventory[item1] > 0:
                                    self.crafting_items[self.crafting_spot_to_fill] = [item1,1] # The program found that the selected item wasn't already in a crafting slot so the selected item replaces the slot that is to be filled next
                                    self.craft_click_cooldown = time.time()
                                    if self.crafting_spot_to_fill: # Change the crafting slot to fill next time
                                        self.crafting_spot_to_fill = 0
                                    else:
                                        self.crafting_spot_to_fill = 1
                        number1 += 1
            elif self.inventory_type == 'tool':
                number = 0
                actual_number = 0
                for item in list(self.player_tools.keys()):
                    if actual_number >= self.inventory_navigation_number and number < AMOUNT_OF_ITEMS_THAT_CAN_BE_DISPLAYED:
                        show_items(item,self.player_tools[item][0],number)
                        number += 1
                    actual_number += 1
                if number == 0 and self.inventory_navigation_number > 0:
                    self.inventory_navigation_number -= 1
                if self.mouse_pressed:
                    number = 0
                    for tool in list(self.player_tools.keys()):
                        if detect_inventory_item_clicked(number-self.inventory_navigation_number,self.mouse_position) and time.time() >= self.craft_click_cooldown+INVENTORY_CLICK_COOLDOWN:
                            self.current_tool = self.player_tools[tool][1] # If the tool is in the displayable range of the inventory, display it
                            self.craft_click_cooldown = time.time()
                        number += 1
        

            show_crafting_ui(self.crafting_items[0][0],self.crafting_items[1][0],self.crafting_items[0][1],self.crafting_items[1][1]) # Show the crafting slots and what it makes if applicable
            if draw_craft_button(self.mouse_pressed,self.mouse_position) and time.time() >= self.craft_click_cooldown+INVENTORY_CLICK_COOLDOWN: # Exexcute if the craft button was pressed and its cooldown was refreshed
                self.craft_click_cooldown = time.time()
                for recipe in CRAFTING_RECIPES:
                    if self.crafting_items[0] in recipe and self.crafting_items[1] in recipe and self.crafting_items[1] != self.crafting_items[0] and self.inventory[self.crafting_items[0][0]] >= self.crafting_items[0][1] and self.inventory[self.crafting_items[1][0]] >= self.crafting_items[1][1]:
                        try:
                            self.inventory[self.crafting_items[0][0]] -= self.crafting_items[0][1] # Try removing the amount of the item/tool in the first crafting spot from the players inventory; which stores items only
                        except:
                            self.player_tools[self.crafting_items[0][0]] -= self.crafting_items[0][1] # If that doesnt work, the porgram knows that the thing in the first crafting slot is a tool, so it removes that amount from the tool in the players tool inventory
                        try:
                            self.inventory[self.crafting_items[1][0]] -= self.crafting_items[1][1] # Same thing as the last try-except statement but for the item/tool in the second crafting slot
                        except:
                            self.player_tools[self.crafting_items[1][0]] -= self.crafting_items[1][1]
                        if recipe[4] == 'item': # Execute if the outcome of the craft is an item
                            if recipe[2] in list(self.inventory.keys()):
                                self.inventory[recipe[2]] += recipe[3] # If the player already has the item in its inventory, increase the count of that item by the outcome amount of the crafting recipe
                            else:
                                self.inventory[recipe[2]] = recipe[3] # Add the item and the amount of the item that the recipe created to the player's inventory
                        elif recipe[4] == 'tool': # Execute if the outcome of the craft is a tool
                            if recipe[2] in list(self.player_tools.keys()):
                                self.player_tools[recipe[2]][0] += recipe[3] # If the player already has the tool in its inventory, increase the count of that tool by the outcome amount of the crafting recipe
                            else:
                                self.player_tools[recipe[2]] = [recipe[3],recipe[5]] # Add the tool and the amount of the tool that the recipe created to the player's tool inventory
                        # self.crafting_items = [['None',0],['None',0]]  

            if self.mouse_pressed:
                number = 0
                for button in buttons:
                    if detect_inventory_button_press(number,self.mouse_position): # If the mouse clicked a button
                        self.inventory_type = button[0]
                        self.inventory_navigation_number = 0
                    
                    number += 1
                number = 0
                # arcade.draw_text("Items",left)

        if self.current_phase != 'day' and not(self.crafting): # If it isnt daytime, draw an arrow directing hte player to the camp area
            x_difference = self.global_position[0] - self.camp_position[0] + SCREEN_WIDTH//2 # Calculate the x distance from the player's position to the camp
            y_difference = self.global_position[1] - self.camp_position[1] + SCREEN_HEIGHT//2 # Calculate the y distance from the player's position to the camp
            # print(x_difference,y_difference)
            angle_to_camp = math.atan2(y_difference,x_difference)# Finds the angle from the player to the camp (theres probably a better way to do this but this is the only way i found)
            # Now, use the angle to the camp and the radius of the circle that directs the player to it
            circle_radius = SCREEN_HEIGHT//4 # Calcultuing the radius of the circle depending on the screen size
            circle_x_pos = circle_radius * math.cos(angle_to_camp) + SCREEN_WIDTH//2 # calculating the x pos of the circle to navigate the player to camp (adding half of the screen width so that it is centered to the screen)
            circle_y_pos = circle_radius * math.sin(angle_to_camp) + SCREEN_HEIGHT//2 # Same as the last line but for the y position

            distance_to_camp = calculate_distance([self.global_position[0]+SCREEN_WIDTH//2,self.global_position[1]+SCREEN_HEIGHT//2],self.camp_position) # Find the player's distance from the camp
            if distance_to_camp > circle_radius:
                if distance_to_camp <= 1000: # If the pl;ayer is close to the camp, show the navigation circle as green to notify the player
                    arcade.draw_circle_filled(circle_x_pos,circle_y_pos,10,arcade.color.GREEN)
                elif distance_to_camp >= MAP_DIMENSIONS//2: # If the player has more than half the map's distance lengthwise from the camp, notify them by showing a red navigation circle so that they hurry up 
                    arcade.draw_circle_filled(circle_x_pos,circle_y_pos,10,arcade.color.RED)
                else:
                    arcade.draw_circle_filled(circle_x_pos,circle_y_pos,10,arcade.color.WHITE) #If the player isnt too far but not too close from the camp, draw a neutral white navigation circle
                arcade.draw_text("Camp",circle_x_pos,circle_y_pos-20,arcade.color.WHITE,15,anchor_x='center',anchor_y='center')
            else:
                arcade.draw_circle_filled(self.global_position[0] - self.camp_position[0]+SCREEN_WIDTH,self.global_position[1] - self.camp_position[1]+SCREEN_HEIGHT,10,arcade.color.GREEN)
                arcade.draw_text("Camp",self.global_position[0] - self.camp_position[0]+SCREEN_WIDTH,self.global_position[1] - self.camp_position[1]+SCREEN_HEIGHT-20,arcade.color.WHITE,15,anchor_x='center',anchor_y='center')

            # arcade.draw_line(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,self.global_position[0]-self.camp_position[0]+SCREEN_WIDTH,self.global_position[1]-self.camp_position[1]+SCREEN_HEIGHT,arcade.color.WHITE,20)
        arcade.finish_render()
    def on_mouse_motion(self, x, y, dx, dy): 
        """
        Called when the mouse cursor is moved
        """
        self.mouse_position = [x,y]
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when a mouse button is pressed
        """
        self.mouse_pressed = True
    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a mouse button is released
        """
        self.mouse_pressed = False

    def update_player_speed(self):
        """
        Used to determine how to move the player depending on the keys pressed.
        """
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED


    def on_update(self, delta_time):
        """
        Called constantly by arcade. Runs everything neccessary for game calculations
        """
        # Calling update moves the sprite depending on the valyes of the keys pressed
        if calculate_distance(self.camp_position,[self.global_position[0]+SCREEN_WIDTH//2,self.global_position[1]+SCREEN_HEIGHT//2]) <= SCREEN_HEIGHT and self.current_phase=='dark':
            self.in_camp = True
        else:
            self.in_camp = False

        if time.time() >= self.last_heal+HEAL_COOLDOWN:
            multiplier = (3 if self.in_camp else 1)
            if calculate_distance(self.camp_position,[self.global_position[0]+SCREEN_WIDTH//2,self.global_position[1]+SCREEN_HEIGHT//2]) > SCREEN_HEIGHT//2 and self.current_phase == 'dark':
                multiplier = -4 # Deal damage if it is night time and the player isnt at camp
            self.player_health += 1 * multiplier
            if self.player_health > self.max_health:
                self.player_health = self.max_health
            self.last_heal = time.time()

        if self.player_health <= 0:
            arcade.close_window() # If the player dies close the game window and run the death screen
            if not(self.debugging): # only remove the save if not debbuging; keep it for data analytic purposes
                save_method.remove_save(0)
            death_screen = Death(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE,time.time()-self.start_time,self.level)
            arcade.run()
        if time.time() >= self.last_autosave+SAVE_COOLDOWN:
            self.autosave() # Create an autosave if the autosave cooldown has refreshed
            self.last_autosave = time.time()
        self.player_list.update()
        if not(self.player_sprite.change_x) and not(self.player_sprite.change_y):
            self.footstep_sfx.pause() # Stop the footstep sfx if theplayer isnt moving
        else:
            self.footstep_sfx.play() # Resum the footstep sfx if the player is moving
        multiplier = (1.5 if self.in_camp == True else 1) # Buff if the player is in camp
        self.global_position[0] -= self.player_sprite.change_x * delta_time * multiplier # Calculating the global x postion by ading the player's movement and a camp buff if applicable
        self.global_position[1] -= self.player_sprite.change_y * delta_time * multiplier # Calculating the global y postion by ading the player's movement and a camp buff if applicable
        if self.mouse_pressed:
            if time.time() >= self.mine_cooldown:
                for a in self.resources:
                    if not self.crafting:
                        harvest = a.harvest_resource(self.mouse_position,self.global_position,self.current_tool)
                        if harvest[0]: # If the resource interacted with the tool
                            multiplier = (0.5 if self.in_camp else 1) # Buff if the player is in camp
                            self.mine_cooldown = time.time() + (harvest[2]*multiplier) # harvest[2] = the cooldown for the specfic tool used # Make the cooldown half if the player is in the camp
                            if harvest[1]: # If the resource the player interacted with was destroyed as a result
                                self.resources.pop(harvest[3]) # harvest[3] = the id of the resource interacted with
                                for b in self.resources:
                                    b.change_id(harvest[3])
                                for c in harvest[4]: # harvest[4] = the loot dropped as a consequence of the click
                                    if c[0] in list(self.inventory.keys()): # checking if there already is the type of item in the inventory
                                        self.inventory[c[0]] += c[1] # add the amount dropped to the existing amount
                                    else: # Run if the player does not have that item in their inventory yet
                                        self.inventory[c[0]] = c[1] # Create a new dictionary key with the name of the item and set it to the amount of that item dropped
                                self.show_messages(True,'','item',harvest[4])
            if time.time() >= self.mine_cooldown:
                enemy_number = 0
                hit = False
                for enemy in self.enemies:
                    if time.time() >= self.mine_cooldown: # Run if the attack cooldown has refreshed
                        if 'enemy' in self.current_tool.tool_type:
                            damage = self.current_tool.damage # the damage the current tool can deal is equal to its damge if it is made to damage enemies
                        else:
                            damage = self.current_tool.enemy_damge # the damage the current tool can deal if it isnt made to deal damage to enemies (some tools can still damage enemies if they werent made to, but with a debuff to the damage they deal)
                        if damage > 0: # If the damage the tool deals is more than 0, run this code block
                            multiplier = (1.25 if self.in_camp else 1) # 1.25x damage if in camp
                            data = enemy.detect_hit(self.global_position,self.mouse_position,damage*multiplier)
                            if data[0]: # If the enemy is hit
                                hit = True
                            if data[1]:
                                self.enemies.pop(enemy_number) # Remove the enemy if the enemy got killed from the attack
                                enemy_number -= 1
                    enemy_number += 1
                if hit: # Only set cooldown after having detected for all enemies, so that the player can hit multiplie enemies at a time
                    multiplier = (0.5 if self.in_camp else 1) # half cooldown time if in camp
                    self.mine_cooldown = time.time()+(self.current_tool.cooldown*multiplier) # Make the cooldown half if the player is in the camp
        
        
        self.tick() # Spawn an enemy if the cooldown allows

        # Checking to see if a phase needs to be changed
        if self.current_phase == 'day' and time.time() - self.dawn_time >= DELAY_FOR_EVENING:
            self.current_phase = 'evening'
            self.show_messages(True,'It is now the evening.')
            arcade.stop_sound(self.bg_music)
            self.bg_music = EVENING_TRACK.play(0.5,0,True)

            self.camp_position = [random.randint(-MAP_DIMENSIONS//2,MAP_DIMENSIONS//2),random.randint(-MAP_DIMENSIONS//2,MAP_DIMENSIONS//2)] # Calculating a possible camp position
            while calculate_distance(self.camp_position,self.global_position) < MIN_CAMP_DISTANCE: # if the camp position is too close to the player, try another position
                self.camp_position = [random.randint(-MAP_DIMENSIONS//2,MAP_DIMENSIONS//2),random.randint(-MAP_DIMENSIONS//2,MAP_DIMENSIONS//2)]
        elif self.current_phase == 'evening' and time.time() - self.dawn_time >= DELAY_FOR_NIGHT:
            self.current_phase = 'dark'
            self.show_messages(True,'It is now dark...')
            arcade.stop_sound(self.bg_music)
            self.bg_music = DARK_TRACK.play(0.5,0,True)
        elif self.current_phase == 'dark' and time.time() - self.dawn_time >= DELAY_FOR_DAY:
            self.current_phase = 'day'
            self.show_messages(True,'It is now the morning!')
            self.level += 1 # 1 level per night survived
            self.enemies = []
            self.dawn_time = time.time()
            arcade.stop_sound(self.bg_music)
            self.bg_music = DAY_TRACK.play(0.5,0,True)
        for enemy in self.enemies:
            attack = enemy.mind(self.global_position,delta_time)
            if attack:
                self.player_health -= attack
            
    def on_key_press(self, key, modifiers):
        """
        Called when a key is pressed
        """
        if key in INVENTORY_BIND:
            if self.crafting:
                self.crafting = False
            else:
                self.crafting = True
                self.crafting_items = [['None',0],['None',0]]
        if key == 120: # X = Debug Key
            print("Coords = ",[self.global_position[0]+SCREEN_WIDTH//2,self.global_position[1]+SCREEN_HEIGHT//2])
            print("Camp coords = ",self.camp_position)
            print(calculate_distance(self.camp_position,[self.global_position[0]+SCREEN_WIDTH//2,self.global_position[1]+SCREEN_HEIGHT//2]))
        if not self.crafting:
            if key == 119: # 119 = key W
                self.up_pressed = True
                self.update_player_speed()
            elif key == 115: # 97 = key A
                self.down_pressed = True
                self.update_player_speed()
            elif key == 97: # 115 = key S
                self.left_pressed = True
                self.update_player_speed()
            elif key == 100: # 100 = key D
                self.right_pressed = True
                self.update_player_speed()
        if self.crafting and time.time() >= self.last_inventory_navigate + INVENTORY_NAVIGATION_COOLDOWN:
            if key == arcade.key.UP and self.inventory_navigation_number > 0:
                self.inventory_navigation_number -= 1
                self.last_inventory_navigate = time.time()
            if key == arcade.key.DOWN: #and self.inventory_navigation_number <= max([max(list(self.inventory.keys())),max(list(self.player_tools.keys()))]):
                self.inventory_navigation_number += 1
                self.last_inventory_navigate = time.time()

    def on_key_release(self, key, modifiers):
        """
        Called when a key is released
        """
        if key == 119: # 119 = key W
            self.up_pressed = False
            self.update_player_speed()
        elif key == 115: # 97 = key A
            self.down_pressed = False
            self.update_player_speed()
        elif key == 97: # 115 = key S
            self.left_pressed = False
            self.update_player_speed()
        elif key == 100: # 100 = key D
            self.right_pressed = False
            self.update_player_speed()

class Death(arcade.Window):
    
    """An instance of the arcade Window class, used to display death statistics"""

    def __init__(self, width, height, title,time_survived,level):

        super().__init__(width, height, title)

        self.time_initiated = time.time()
        self.time_survived = time_survived
        self.level = level-1
    def on_draw(self):
        """
        Draw everything neccessary on the screen.
        """
        self.clear(arcade.color.WHITE)
        characters = ["ᚠ", "ᚢ", "ᚦ", "ᚨ", "ᚱ", "ᚼ", "ᚾ", "ᛁ", "ᛇ", "ᛈ", "ᛉ", "ᛏ", "ᛒ", "ᛖ", "ᛗ", "ᛚ", "ᛟ", "ᛞ"]
        random_char_string = ''
        for x in range(10):
            random_char_string = random_char_string + random.choice(characters)
        arcade.draw_text("You Died",SCREEN_WIDTH//2,SCREEN_HEIGHT-(time.time()-self.time_initiated)*50,arcade.color.RED,75,anchor_x='center',anchor_y='center')
        arcade.draw_text(random_char_string,SCREEN_WIDTH//2,SCREEN_HEIGHT-(time.time()-self.time_initiated-2)*50,arcade.color.GREEN,50,anchor_x='center',anchor_y='center')
        arcade.draw_text("Time Survived: " + str(int(self.time_survived))+" Seconds.",SCREEN_WIDTH//2,SCREEN_HEIGHT-(time.time()-self.time_initiated-5)*50,arcade.color.BLACK,35,anchor_x='center',anchor_y='center')
        arcade.draw_text("Nights Survived: "+str(self.level),SCREEN_WIDTH//2,SCREEN_HEIGHT-(time.time()-self.time_initiated-7)*50,arcade.color.GREEN,35,anchor_x='center',anchor_y='center')
        if self.level == 0:
            arcade.draw_text("Hello? Is anyone there?.",SCREEN_WIDTH//2,SCREEN_HEIGHT-(time.time()-self.time_initiated-10)*50,arcade.color.RED,25,anchor_x='center',anchor_y='center')
        elif self.level >= 1 and self.level <= 3:
            arcade.draw_text("You can do better.",SCREEN_WIDTH//2,SCREEN_HEIGHT-(time.time()-self.time_initiated-10)*50,arcade.color.RED,50,anchor_x='center',anchor_y='center')
        elif self.level >= 4 and self.level <= 6:
            arcade.draw_text("Well Played.",SCREEN_WIDTH//2,SCREEN_HEIGHT-(time.time()-self.time_initiated-10)*50,arcade.color.BLACK,55,anchor_x='center',anchor_y='center')
        else:
            arcade.draw_text("Impressive!",SCREEN_WIDTH//2,SCREEN_HEIGHT-(time.time()-self.time_initiated-10)*50,arcade.color.GREEN,55,anchor_x='center',anchor_y='center')
        if time.time() > self.time_initiated+18:
            exit("Game Over. Better Luck Next Time.")


def main():
    initiate_modules()
    menu_window = Menu(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
    # if resources:
    #             arcade.close_window()
    #             window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    #             window.setup(resources)
    #             arcade.run()
                
    


if __name__ == "__main__":
    main()