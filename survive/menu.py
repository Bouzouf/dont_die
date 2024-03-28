import save_method, arcade
from loading import Loading
from game import *
from game_settings import *
import time
print("Menu Initiated")

class Menu(arcade.Window):
    def __init__(self, width, height, title): # This function was taken from a tutorial
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title)


        # Track the current state of what key is pressed

        self.enter_pressed = False

        self.mouse_position = [0,0]


        # Set the background color
        arcade.set_background_color(arcade.color.BLIZZARD_BLUE)

        self.last_click = 0
        self.CLICK_COOLDOWN = 0.25

        self.map_size_multiplier = 1

        self.buttons = ["New Game","Load Game","Wipe Saved Game","Map Size: Normal"]
    # def setup(self):
    #     self.selected_button = 0
    def draw_interactive_text(self,number,text):
        """
        Draw text that enlargens the closer the mouse is to it
        
            Parameters:
                number (int): The amount of texts previously rendered in this frame; so that the text is beneath other texts
                text (str): The text to be displayed
        """
        y_position = SCREEN_HEIGHT//1.5 - ((SCREEN_HEIGHT/10)*number)
        distance_to_mouse = ((self.mouse_position[1]-y_position)**2)**0.5 # The indices are to ensure the number is positive, e.g. (-2)**2**0.5 = 2
        text_size = (SCREEN_HEIGHT-SCREEN_HEIGHT//1.05)
        if distance_to_mouse <= SCREEN_HEIGHT//10:
            text_size = (SCREEN_HEIGHT-SCREEN_HEIGHT//1.05) + (SCREEN_HEIGHT//10-distance_to_mouse)//4
        if text_size < 10:
            text_size = 10
        arcade.draw_text(str(text),SCREEN_WIDTH//2,y_position,arcade.color.BLACK_LEATHER_JACKET,text_size,anchor_x='center',anchor_y='center')
    def on_draw(self):
        """
        Draw everything neccessary on the screen.
        """
        self.clear(arcade.color.BLIZZARD_BLUE) # Set the background
        arcade.draw_text("Don't Die",SCREEN_WIDTH//2,SCREEN_HEIGHT//1.2,arcade.color.BLACK_LEATHER_JACKET,SCREEN_HEIGHT-SCREEN_HEIGHT//1.1,anchor_x='center') # Draw the game's name in the top
        button_number = 0
        for button in self.buttons:
            self.draw_interactive_text(button_number,button)
            button_number += 1



    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called when the mouse cursor moves
        """
        self.mouse_position = [x,y]

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when a mouse button is pressed
        """
        closest_button = [-1,9999999] # First item is the button number (-1 default as no number has a place -1), second item is the istamce of that button from the mouse
        button_number = 0
        for button in self.buttons: # Calculates the closest button to the mouse cursor
            y_position = SCREEN_HEIGHT//1.5 - ((SCREEN_HEIGHT/10)*button_number)
            distance_to_mouse = ((y-y_position)**2)**0.5
            if distance_to_mouse < closest_button[1]:
                closest_button = [button_number,distance_to_mouse] 
            button_number += 1
        if closest_button[0] == 0: # If the "New Game" button was clicked
            arcade.close_window()
            loading_window = Loading(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
            resources = loading_window.setup(self.map_size_multiplier)
            arcade.close_window()
            time.sleep(0.1) # Delay used so that the main game window isnt closed upon opening
            if resources:
                game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
                game.setup(resources,False)
                arcade.run()
        if closest_button[0] == 1: # If the "Load Game" button was clicked
            try:
                import savegame # NO setup as otherwise a circular import will occur
                old_data = savegame.GameData.load(0)
                assert old_data
                arcade.close_window()
                time.sleep(0.1) # Delay used so that the main game window isnt closed upon opening
                game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
                game.setup(None,old_data,True)
                arcade.run()
            except:
                pass # Do nothing if theres isnt a save to 
        if closest_button[0] == 2: # If the "Wipe Saved Game" button was clicked
            save_method.remove_save(0) # Remove the saved game data
        if closest_button[0] == 3 and time.time() >= self.last_click+self.CLICK_COOLDOWN: # If the "Map Size" button was clicked
            if self.map_size_multiplier == 1: # Changing the map dimension multiplier and displaying the corresponding text
                self.map_size_multiplier = 1.5
                self.buttons[3] = "Map Size: Large (Challenging)"
            elif self.map_size_multiplier == 1.5: # Changing the map dimension multiplier and displaying the corresponding text
                self.map_size_multiplier = 2
                self.buttons[3] = "Map Size: Sparse (Impossible)"
            elif self.map_size_multiplier == 2: # Changing the map dimension multiplier and displaying the corresponding text
                self.map_size_multiplier = 1
                self.buttons[3] = "Map Size: Normal" 
            self.last_click = time.time()