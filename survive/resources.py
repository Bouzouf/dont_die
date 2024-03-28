# from game import *
import arcade, random
from game_settings import *

print('Resources Initiated')

class Resource():
    """
    A class used to represent a resource such as a tree
    
    Attributes
    ----------
    position (list): The position of the resource
    resource_type (str): The type of resource the Resource is (tree, simple_rock, etc)
    id (int): The resource's unique ID
    (Required for loading saved game files - Do not use the following for rsource generation)
    extra (bool): Set to True if you are loading a resource so that the program maintains its health and image number
    rock_img (int): The number used to index the rock image from the list of rock images used to display the resource if it is a rock
    iron_img (int): The number used to index the iron image from the list of iron images used to display the resource if it is an iron deposit
    health (float/int): The health of the resource
    """
    def __init__(self,position=[0,0],resource_type='tree',id=0,extra=False,rock_img=None,iron_img=None,health=None):
        self.id = id
        self.resource_type = resource_type
        self.pos = position
        if resource_type == "tree":
            self.health = 50
        elif resource_type == 'simple_rock':
            self.health = 150
        elif resource_type == 'iron_rock':
            self.health = 300
        else:
            self.health = health
        self.max_health = self.health
        self.rock_structure = []
        if not(extra):
            self.rock_image = random.randint(0,len(ROCK_IMAGES)-1)
            self.iron_image = random.randint(0,len(IRON_IMAGES)-1)
        else:
            self.rock_image = rock_img
            self.iron_image = iron_img
        self.radius = random.randint(ROCK_RADII[0],ROCK_RADII[1])

    def change_id(self,cap_off,amount=-1): # Cap off = the furthest point where the id is changed
        if self.id >= cap_off:
            self.id += amount # Changing the resource's id (usually by -1). This is used when an Enemy is killed, the enemies with a list index higher than that enemy have their id's moved down to make their spot in the enemy list match their id
    def draw_resource(self,global_position):
        center_x = global_position[0] - self.pos[0] # calcuating the x position to display the resource in 
        center_y = global_position[1] - self.pos[1] # calcuating the y position to display the resource in 
        if self.resource_type == 'tree':
            if center_x >= -20 and center_x <= SCREEN_WIDTH+20 and center_y >= -20 and center_y <= SCREEN_HEIGHT+20: # Claculating if the resource is within the screen boundaries
                # Draw the tree trunk
                arcade.draw_scaled_texture_rectangle(center_x,center_y+50,TREE_IMAGE,0.75)
        elif self.resource_type == 'simple_rock':
            if center_x >= -ROCK_RADII[1] and center_x <= SCREEN_WIDTH+ROCK_RADII[1] and center_y >= -ROCK_RADII[1] and center_y <= SCREEN_HEIGHT+ROCK_RADII[1]: # Claculating if the resource is within the screen boundaries
                arcade.draw_scaled_texture_rectangle(center_x,center_y,ROCK_IMAGES[self.rock_image])
        elif self.resource_type == 'iron_rock':
            if center_x >= -ROCK_RADII[1] and center_x <= SCREEN_WIDTH+ROCK_RADII[1] and center_y >= -ROCK_RADII[1] and center_y <= SCREEN_HEIGHT+ROCK_RADII[1]: # Claculating if the resource is within the screen boundaries
                arcade.draw_scaled_texture_rectangle(center_x,center_y,IRON_IMAGES[self.iron_image])
    def harvest_resource(self,mouse_position,global_position,tool):
        center_x = global_position[0] - self.pos[0]
        center_y = global_position[1] - self.pos[1]
        resource_harvested = False
        tool_used = False
        yeild = []
        
        if self.resource_type == 'tree':
            if mouse_position[0] >= center_x-30 and mouse_position[0] <= center_x+30 and mouse_position[1] >= center_y and mouse_position[1] <= center_y+100: # Checking if the mouse cursor collides with the resource
                if 'wood' in tool.tool_type:
                    self.health -= tool.damage # Reduce the resource's health by the damage of the tool
                    tool_used = True
                elif not tool.single_use:
                    self.health -= tool.damage * tool.other_use_debuff # Reduce the resource's health by the damge of the tool accoutning for the debuff applied if the tool isnt meant for that resource type (most tools dont allow this to happen - this is controlled by the single_use variable)
                    tool_used = True
                if tool_used:
                    yeild.append(['wood',random.randint(TREE_WOOD_RATE[0],TREE_WOOD_RATE[1])]) # Add the item yeild from harvesting the resource (to be used later in the script using this function) 
                    yeild.append(['pebble',random.randint(1,2)]) # Add the item yeild from harvesting the resource (to be used later in the script using this function) 
        if self.resource_type == 'simple_rock':
            if mouse_position[0] >= center_x-self.radius and mouse_position[0] <= center_x+self.radius and mouse_position[1] >= center_y-self.radius and mouse_position[1] <= center_y+self.radius: # Checking if the mouse cursor collides with the resource
                if 'rock' in tool.tool_type:
                    self.health -= tool.damage # Reduce the resource's health by the damage of the tool
                    tool_used = True
                elif not tool.single_use:
                    self.health -= tool.damage * tool.other_use_debuff # Reduce the resource's health by the damge of the tool accoutning for the debuff applied if the tool isnt meant for that resource type (most tools dont allow this to happen - this is controlled by the single_use variable)
                    tool_used = True
                if tool_used:
                    yeild.append(['pebble',random.randint(PEBBLE_ROCK_RATE[0],PEBBLE_ROCK_RATE[1])]) # Add the item yeild from harvesting the resource (to be used later in the script using this function) 
                    yeild.append(['rock',random.randint(ROCK_ROCK_RATE[0],ROCK_ROCK_RATE[1])]) # Add the item yeild from harvesting the resource (to be used later in the script using this function) 
                    random.choice(ROCK_SOUNDS).play()
        if self.resource_type == 'iron_rock':
            if mouse_position[0] >= center_x-self.radius and mouse_position[0] <= center_x+self.radius and mouse_position[1] >= center_y-self.radius and mouse_position[1] <= center_y+self.radius: # Checking if the mouse cursor collides with the resource
                if 'iron' in tool.tool_type:
                    self.health -= tool.damage # Reduce the resource's health by the damage of the tool
                    tool_used = True
                elif not tool.single_use:
                    self.health -= tool.damage * tool.other_use_debuff # Reduce the resource's health by the damge of the tool accoutning for the debuff applied if the tool isnt meant for that resource type (most tools dont allow this to happen - this is controlled by the single_use variable)
                    tool_used = True
                if tool_used:
                    yeild.append(['raw iron',random.randint(IRON_ROCK_RATE[0],IRON_ROCK_RATE[1])]) # Add the item yeild from harvesting the resource (to be used later in the script using this function) 
        
        if self.health <= 0:
            resource_harvested = True # If the resource was killed / harvested, set this variable to True
            # Call the dropping of the items here?
        return ([tool_used,resource_harvested,tool.cooldown,self.id,yeild])
    def display_health(self,mouse_position,global_position):
        center_x = global_position[0] - self.pos[0]
        center_y = global_position[1] - self.pos[1]
        drew_health = False
        # if calculate_distance
        if self.resource_type == 'tree':
            if mouse_position[0] >= center_x-30 and mouse_position[0] <= center_x+30 and mouse_position[1] >= center_y and mouse_position[1] <= center_y+100:
                health_percent = self.health / self.max_health # Calculating the ratio of the player's current health to their maximum possible health
                drew_health = True
                if mouse_position[0]+SCREEN_WIDTH//10 >= SCREEN_WIDTH: # Draws health bar to the left of the mouse if drawing it to the right would go out of the screen
                    # DRAWING HEALTH BAR VVVV
                    arcade.draw_rectangle_filled(mouse_position[0]-SCREEN_WIDTH//20-HEALTH_BAR_OUTLINE_THICKNESS, mouse_position[1], SCREEN_WIDTH//10+(HEALTH_BAR_OUTLINE_THICKNESS*2), SCREEN_HEIGHT//45+(HEALTH_BAR_OUTLINE_THICKNESS*2), arcade.color.GRAY)
                    arcade.draw_rectangle_filled(mouse_position[0]-SCREEN_WIDTH//20+((SCREEN_WIDTH//10)-(SCREEN_WIDTH//10)*health_percent)//2-HEALTH_BAR_OUTLINE_THICKNESS, mouse_position[1], (SCREEN_WIDTH//10)*health_percent, SCREEN_HEIGHT//45, arcade.color.GREEN)
                else:
                    # DRAWING HEALTH BAR VVVV
                    arcade.draw_rectangle_filled(mouse_position[0]+SCREEN_WIDTH//20+HEALTH_BAR_OUTLINE_THICKNESS, mouse_position[1], SCREEN_WIDTH//10+(HEALTH_BAR_OUTLINE_THICKNESS*2), SCREEN_HEIGHT//45+(HEALTH_BAR_OUTLINE_THICKNESS*2), arcade.color.GRAY)
                    arcade.draw_rectangle_filled(mouse_position[0]+SCREEN_WIDTH//20-((SCREEN_WIDTH//10)-(SCREEN_WIDTH//10)*health_percent)//2+HEALTH_BAR_OUTLINE_THICKNESS, mouse_position[1], (SCREEN_WIDTH//10)*health_percent, SCREEN_HEIGHT//45, arcade.color.GREEN)
        elif self.resource_type == 'simple_rock' or self.resource_type == 'iron_rock':
            if mouse_position[0] >= center_x-self.radius and mouse_position[0] <= center_x+self.radius and mouse_position[1] >= center_y-self.radius and mouse_position[1] <= center_y+self.radius:
                health_percent = self.health / self.max_health # Calculating the ratio of the player's current health to their maximum possible health
                drew_health = True
                if mouse_position[0]+SCREEN_WIDTH//10 >= SCREEN_WIDTH: # Draws health bar to the left of the mouse if drawing it to the right would go out of the screen
                    # DRAWING HEALTH BAR VVVV
                    arcade.draw_rectangle_filled(mouse_position[0]-SCREEN_WIDTH//20-HEALTH_BAR_OUTLINE_THICKNESS, mouse_position[1], SCREEN_WIDTH//10+(HEALTH_BAR_OUTLINE_THICKNESS*2), SCREEN_HEIGHT//45+(HEALTH_BAR_OUTLINE_THICKNESS*2), arcade.color.GRAY)
                    arcade.draw_rectangle_filled(mouse_position[0]-SCREEN_WIDTH//20+((SCREEN_WIDTH//10)-(SCREEN_WIDTH//10)*health_percent)//2-HEALTH_BAR_OUTLINE_THICKNESS, mouse_position[1], (SCREEN_WIDTH//10)*health_percent, SCREEN_HEIGHT//45, arcade.color.GREEN)
                else:
                    # DRAWING HEALTH BAR VVVV
                    arcade.draw_rectangle_filled(mouse_position[0]+SCREEN_WIDTH//20+HEALTH_BAR_OUTLINE_THICKNESS, mouse_position[1], SCREEN_WIDTH//10+(HEALTH_BAR_OUTLINE_THICKNESS*2), SCREEN_HEIGHT//45+(HEALTH_BAR_OUTLINE_THICKNESS*2), arcade.color.GRAY)
                    arcade.draw_rectangle_filled(mouse_position[0]+SCREEN_WIDTH//20-((SCREEN_WIDTH//10)-(SCREEN_WIDTH//10)*health_percent)//2+HEALTH_BAR_OUTLINE_THICKNESS, mouse_position[1], (SCREEN_WIDTH//10)*health_percent, SCREEN_HEIGHT//45, arcade.color.GREEN)
        return drew_health
                