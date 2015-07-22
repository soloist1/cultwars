"""
Room

Rooms are simple containers that has no location of their own.

"""
import random
from evennia import DefaultRoom, TICKER_HANDLER
from evennia import utils
from characters import Character
from npc import Npc
from commands.default_cmdsets import ChargenCmdset


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def at_object_receive(self, obj, source_location):
        if utils.inherits_from(obj, Npc): # An NPC has entered
            pass

        else:
            if utils.inherits_from(obj, Character): 
                # A PC has entered, NPC is caught above.
                # Cause the character to look around
                obj.execute_cmd('look')
                for item in self.contents:
                    if utils.inherits_from(item, Npc): 
                        # An NPC is in the room
                        item.at_char_entered(obj)

class ChargenRoom(Room):
    """
    This room class is used by character-generation rooms. It makes
    the ChargenCmdset available.
    """
    def at_object_creation(self):
        "this is called only at first creation"
        self.cmdset.add(ChargenCmdset, permanent=True)



ECHOES = ["The sky is clear.", 
              "Clouds gather overhead.",
              "It's starting to drizzle.",
              "A breeze of wind is felt.",
              "The wind is picking up"] # etc  

class WeatherRoom(DefaultRoom):
    "This room is ticked at regular intervals"        

    def at_object_creation(self):
        "called only when the object is first created"
        TICKER_HANDLER.add(self, 60, hook_key="at_weather_update")

    def at_weather_update(self, *args, **kwargs):
        "ticked at regular intervals"
        echo = random.choice(ECHOES)
        self.msg_contents(echo)

#class NPCRoom(Room):

#    """
#    This room class is used by NPC-generation rooms. It makes
#    the NPCCmdset available.
#    """
#    def at_object_creation(self):
#        "this is called only at first creation"
#        self.cmdset.add(NPCCmdset, permanent=True)

