import json
class GameData:
    def save(data, save_number):
        """
        Saves game data to a pre-determined folder

            Parameters:
                data (dictionary): Dictionary of data that you want to save
                save_number (int): The number that the save file will have
        """
        filename = 'saves/save' + str(save_number) + '.json' # Load the file name
        data_to_save = {"my_game_data": data} # creating the data to save (putting a dict in a dict to avoid a weakref error)
        with open(filename, 'w') as file:
            json.dump(data_to_save, file) # write the game data to the file

    def load(save_number):
        """
        Load saved game data from a pre-determined folder
        
            Parameters:
                save_number (int): The save number to load
            
            Returns:
                loaded_data (dict): The saved game data in a dictionary"""
        filename = 'saves/save' + str(save_number) + '.json' # Load the file name
        with open(filename, 'r') as file:
            loaded_data = json.load(file) # Load the data from the file name
            return loaded_data["my_game_data"] # Return the game data in dictionary form 