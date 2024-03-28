import arcade,time,random
import game_settings as settings
from resources import Resource

def calculate_distance(pos1, pos2):
    """
    Calculate the distance between two positions
    """
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

def generate_resource(resource_type,minimum_spacing,range=[-500,500], all_resources=False, resources=[],id=0):
    """
    Generates a reource with minimum spacing from other resources for a clean look

        Paremeters:
            resource_type (str): The type of resource to generate (e.g. 'tree')
            minimum_spacing (float): The minimum distance that the resource must have from other resources
            range (list): A list with 2 items; the minimum and maximum position x and y wise that the resource can be generates
            all_resources (bool): If False, only calculate minimum spacing for resources of the same type as the resource being generated (RECOMMENDED)
            resources (list): A list of all the resource objects; used for minimum spacing calculations
            id (int): The unqiue id of the resource.
        Returns:
            Resource() object
                    """
    # Define the area where resources can be placed
    x_range = (range[0], range[1])
    y_range = (range[0], range[1])
    position = [random.randint(x_range[0], x_range[1]), random.randint(y_range[0], y_range[1])] # Generate a random position for the resource
    if resources:
        found_valid_position = False
        while not found_valid_position: # Runs as long as a valid position has not been found
            position = [random.randint(x_range[0], x_range[1]), random.randint(y_range[0], y_range[1])] # Generate a random position for the resource
            found_valid_position = True
            if not all_resources: # If minimum spacing should only be calculated for the same resource types
                for resource in resources:
                    # Check if the generated position violates the minimum spacing rule for the same type of resource
                    if resource.resource_type == resource_type and calculate_distance(position, resource.pos) < minimum_spacing:
                        found_valid_position = False  # Return False if the spacing rule is violated for the same type of resource
            else: # If minimum spacing should be calculated for all resources
                for resource in resources:
                    # Check if the generated position violates the minimum spacing rule for any given resource
                    if calculate_distance(position, resource.pos) < minimum_spacing:
                        found_valid_position = False # Return False if the spacing rule is violated for a resource
    
    return Resource(position,resource_type,id)
class Loading(arcade.Window):
    def __init__(self, width, height, title): # This function was taken from a tutorial
        """
        Initializer
        """
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHITE)
    def setup(self,map_size_multiplier=1):

        self.resources = []
        self.last_loading_tick = 0 # Tracks when the last time the screen was updated, so that the screen only updates every x seconds, to save computing power for the resource generation
        self.load_rotation = 0 # Controls the rotation of the loading circle

        settings.MAP_DIMENSIONS = settings.MAP_DIMENSIONS * map_size_multiplier

        assert settings.RESOURCE_SPACING # stops the code if the resource spaciong is 0 whcih would lead to no resources being drawn

        amount_of_trees = settings.RESOURCE_SPACING


        total_resources = amount_of_trees+amount_of_trees//3+amount_of_trees//6
        current_resources = 0
        for x in range(amount_of_trees): # TREE GENERATION
            new_tree = generate_resource('tree',settings.SPACING_VALUE//1.5,[(settings.MAP_DIMENSIONS//2)*-1,settings.MAP_DIMENSIONS//2],False,self.resources,x)
            self.resources.append(new_tree)
            if time.time() >= self.last_loading_tick+settings.LOADING_COOLDOWN:
                arcade.start_render()
                
                self.clear(arcade.color.WHITE)

                # DRAWING LOADING SCREEN ANIMATION
                arcade.draw_text("...Generating Trees...",settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT/1.7,arcade.color.BLACK,24,anchor_x='center')
                arcade.draw_rectangle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2,settings.SCREEN_WIDTH//1.4,settings.SCREEN_HEIGHT//10,arcade.color.GRAY)
                arcade.draw_rectangle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2,settings.SCREEN_WIDTH//1.4*(current_resources/total_resources),settings.SCREEN_HEIGHT//10,arcade.color.BLUE)
                arcade.draw_circle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2.5,25,arcade.color.AFRICAN_VIOLET)
                arcade.draw_circle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2.5,20,arcade.color.WHITE)
                arcade.draw_rectangle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2.5,50,15,arcade.color.RED_ORANGE,self.load_rotation)
                self.load_rotation += 5
                self.last_loading_tick = time.time()

                arcade.finish_render()
            current_resources += 1

        for x in range(amount_of_trees//3): # ROCK GENERATION
            new_rock = generate_resource('simple_rock',settings.SPACING_VALUE//1.5,[(settings.MAP_DIMENSIONS//2)*-1,settings.MAP_DIMENSIONS//2],False,self.resources,x+amount_of_trees)
            self.resources.append(new_rock)
            if time.time() >= self.last_loading_tick+settings.LOADING_COOLDOWN:
                arcade.start_render()
                self.clear(arcade.color.WHITE)

                # DRAWING LOADING SCREEN ANIMATION
                arcade.draw_text("...Generating Rocks...",settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT/1.7,arcade.color.BLACK,24,anchor_x='center')
                arcade.draw_rectangle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2,settings.SCREEN_WIDTH//1.4,settings.SCREEN_HEIGHT//10,arcade.color.GRAY)
                arcade.draw_rectangle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2,settings.SCREEN_WIDTH//1.4*(current_resources/total_resources),settings.SCREEN_HEIGHT//10,arcade.color.BLUE)
                arcade.draw_circle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2.5,25,arcade.color.AFRICAN_VIOLET)
                arcade.draw_circle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2.5,20,arcade.color.WHITE)
                arcade.draw_rectangle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2.5,50,15,arcade.color.RED_ORANGE,self.load_rotation)
                self.load_rotation += 5
                self.last_loading_tick = time.time()

                arcade.finish_render()
            current_resources += 1
        for x in range(amount_of_trees//6): # IRON ROCK GENERATION
            new_rock = generate_resource('iron_rock',settings.SPACING_VALUE//1.5,[(settings.MAP_DIMENSIONS//2)*-1,settings.MAP_DIMENSIONS//2],False,self.resources,x+amount_of_trees+amount_of_trees//3)
            
            self.resources.append(new_rock)
            if time.time() >= self.last_loading_tick+settings.LOADING_COOLDOWN:
                arcade.start_render()
                
                self.clear(arcade.color.WHITE)

                # DRAWING LOADING SCREEN ANIMATION
                arcade.draw_text("...Generating Iron Deposits...",settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT/1.7,arcade.color.BLACK,24,anchor_x='center')
                arcade.draw_rectangle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2,settings.SCREEN_WIDTH//1.4,settings.SCREEN_HEIGHT//10,arcade.color.GRAY)
                arcade.draw_rectangle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2,settings.SCREEN_WIDTH//1.4*(current_resources/total_resources),settings.SCREEN_HEIGHT//10,arcade.color.BLUE)
                arcade.draw_circle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2.5,25,arcade.color.AFRICAN_VIOLET)
                arcade.draw_circle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2.5,20,arcade.color.WHITE)
                arcade.draw_rectangle_filled(settings.SCREEN_WIDTH//2,settings.SCREEN_HEIGHT//2.5,50,15,arcade.color.RED_ORANGE,self.load_rotation)
                self.load_rotation += 5
                self.last_loading_tick = time.time()

                arcade.finish_render()
            current_resources += 1
        return self.resources