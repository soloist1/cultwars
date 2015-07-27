"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from random import randint
from evennia import DefaultCharacter
from commands.command import CmdMySkills

class Character(DefaultCharacter):
    """
    The Character defaults to implementing some of its hook methods with the
    following standard functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead)
    at_after_move - launches the "look" command
    at_post_puppet(player) -  when Player disconnects from the Character, we
                    store the current location, so the "unconnected" character
                    object does not need to stay on grid but can be given a
                    None-location while offline.
    at_pre_puppet - just before Player re-connects, retrieves the character's
                    old location and puts it back on the grid with a "charname
                    has connected" message echoed to the room
    """
    def at_object_creation(self):
        "This is called when object is first created, only."   
        self.db.level = 1 
        self.db.XP = 0
        self.db.combat = randint(5, 10)
        self.db.strength = 0
        self.db.dexterity = 0
        self.db.charisma = 0
        self.db.intelligence = 0 
        self.db.stamina = 0
        self.db.hitpoints = 0
        self.db.manapoints = 0

    def get_abilities(self):
        """
        Simple access method to return ability 
        scores as a tuple (str,agi,mag)
        """
        return  self.db.XP, self.db.hitpoints, self.db.manapoints, self.db.combat, self.db.level


    def get_stats(self):

      
        return self.db.hitpoints, self.db.manapoints, self.db.stamina
        
    def get_my_stats(self):
 
        return self.db.strength, self.db.dexterity, self.db.charisma, self.db.intelligence, self.db.stamina, self.db.hitpoints, self.db.manapoints

    def get_my_skills(self):
        return self.db.skills['Tracking'], self.db.skills['Botany'], self.db.skills['Crafting']

    def at_after_move(self, source_location):
        """
        Default is to look around after a move 
        Note:  This has been moved to room.at_object_receive
        """
        #self.execute_cmd('look')
        pass

    
  
