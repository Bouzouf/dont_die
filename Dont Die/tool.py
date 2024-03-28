print('Tool Class Initiated')
class Tool():
    """
    A class used to represent a tool.
    
    Attributes
    ----------
    name (str): Name of the tool
    tool_type (list): List of the resource types the tool can interact with (this includes 'enemy' if the tool can attack enemies)
    damage (float): The damage that the tool deals
    cooldown (float): The cooldown to use the tool
    single_use (bool): If the tool can interact with things other than defined in the tool_type list
    other_use_debuff (float): The debuff applied when mining an object not in the defined tool_type list
    hurts_enemies (bool): Whether the tool can be used to attack enemies (if the tool's main use is to attack enemies, add 'enemy' to tool_type instead)
    enemy_damage_debuff (float): The debuff applied when attacking an enemy (not applied if 'enemy' is in tool_type)
    """
    def __init__(self,name,tool_type,damage,cooldown=1.5,single_use=True,other_use_debuff=0.2,hurts_enemies=False,enemy_damage_debuff=0.5):
        """
        Setting up the tool
        """
        self.name = name
        self.tool_type = tool_type
        self.damage = damage
        self.single_use = single_use
        self.debuff = 0.2
        self.cooldown = cooldown
        self.enemy_damge = 0
        self.other_use_debuff = other_use_debuff
        self.hurts_enemies = hurts_enemies
        self.enemy_damage_debuff = enemy_damage_debuff
        if self.hurts_enemies:
            self.enemy_damge = int(damage * self.enemy_damage_debuff)
        else:
            self.enemy_damge = 0
