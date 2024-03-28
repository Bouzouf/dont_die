print("Save Method Imported")

class GameData():
    def __init__(self):
        pass
def load_saved_data(self,save_data,self_data):
    """
    Changes a dictionary of game data to a self object using variable names that the main game script uses.

    Returns a self object. To use this, do self = <this function>()
    """
    from resources import Resource
    from tool import Tool
    import time
    data = save_data
    self = self_data
    self.resources = []
    for data1 in data['resources']:
        self.resources.append(Resource(data1[2],data1[1],data1[0],True,data1[6],data1[7],data1[4]))
    self.global_position = data["global_position"]
    time_to_add = time.time() - data['time_of_save'] # Add the time between when the autosave was made and when the game was loaded - used so that the player cannot skip night time
    self.inventory = data["inventory"]
    self.player_tools = {}
    for tool in data["player_tools"]:
        self.player_tools[tool[1][0]] = [tool[0],Tool(tool[1][0],tool[1][1],tool[1][2],tool[1][5],tool[1][3],tool[1][6],tool[1][7],tool[1][8])]
    self.max_health = data["max_health"]
    self.player_health = data["player_health"]
    self.start_time = data["start_time"]+time_to_add
    self.dawn_time = data["dawn_time"]+time_to_add
    self.current_phase = data["current_phase"]
    self.level = data["level"]
    self.crafting = data["crafting"]
    self.inventory_type = data["inventory_type"]
    self.crafting_items = data["crafting_items"]
    self.crafting_spot_to_fill = data["crafting_spot_to_fill"]
    self.text_displayed = data["text_displayed"]
    self.craft_click_cooldown = data["craft_click_cooldown"]
    self.last_inventory_navigate = data["last_inventory_navigate"]+time_to_add
    self.inventory_navigation_number = data["inventory_navigation_number"]
    self.last_tick = data["last_tick"]+time_to_add
    self.enemies = []#data["enemies"]
    self.mouse_pressed = data["mouse_pressed"]
    self.mouse_position = data["mouse_position"]
    self.mine_cooldown = data["mine_cooldown"]
    self.last_loading_tick = data["last_loading_tick"]+time_to_add
    self.camp_position = data["camp_position"]
    return self
def save_data(self):
    """
    Turns a self object (the function's only paramter) into a dictionary of the game data. Use this for turning your self object into a dictionary that can be used for saving.
    """
    import time
    data = {}
    data["resources"] = []
    for x in self.resources:
        temp = []
        temp.append(x.id)
        temp.append(x.resource_type)
        temp.append(x.pos)
        temp.append(x.health)
        temp.append(x.max_health)
        temp.append(x.rock_structure)                        
        temp.append(x.rock_image)
        temp.append(x.iron_image)
        data["resources"].append(temp)
    data["global_position"] = self.global_position
    data["inventory"] = self.inventory
    data["player_tools"] = []
    for tool_name in list(self.player_tools.keys()):
        temp = [self.player_tools[tool_name][0],[]]
        tool = self.player_tools[tool_name][1]
        temp[1].append(tool.name)
        temp[1].append(tool.tool_type)
        temp[1].append(tool.damage)
        temp[1].append(tool.single_use)
        temp[1].append(tool.debuff)
        temp[1].append(tool.cooldown)
        temp[1].append(tool.other_use_debuff)
        temp[1].append(tool.hurts_enemies)
        temp[1].append(tool.enemy_damage_debuff)
        data["player_tools"].append(temp)
    data["max_health"] = self.max_health
    data["player_health"] = self.player_health
    data["start_time"] = self.start_time
    data["dawn_time"] = self.dawn_time
    data["current_phase"] = self.current_phase
    data["level"] = self.level
    data["crafting"] = self.crafting
    data["inventory_type"] = self.inventory_type
    data["crafting_items"] = self.crafting_items
    data["crafting_spot_to_fill"] = self.crafting_spot_to_fill
    data["text_displayed"] = self.text_displayed
    data["craft_click_cooldown"] = self.craft_click_cooldown
    data["last_inventory_navigate"] = self.last_inventory_navigate
    data["inventory_navigation_number"] = self.inventory_navigation_number
    data["last_tick"] = self.last_tick
    data["mouse_pressed"] = self.mouse_pressed
    data["mouse_position"] = self.mouse_position
    data["mine_cooldown"] = self.mine_cooldown
    data["last_loading_tick"] = self.last_loading_tick
    data['time_of_save'] = time.time()
    data["camp_position"] = self.camp_position
    return data
def remove_save(save_number):
    """
    Removes a save with a ceratin number.
    """
    import os
    try:
        os.remove("saves/save"+str(save_number)+".json")
    except:
        print("No save to clear.")