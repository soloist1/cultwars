"""
Commands

Commands describe the input the player can do to the game.

"""

from evennia import Command as BaseCommand
from evennia import default_cmds
from evennia import create_object
from evennia import utils
from evennia import OOB_HANDLER
from world import rules
from menus import *
#from menus import factionmenu
from evennia.utils.evmenu import EvMenu
import random

class Command(BaseCommand):
    """
    Inherit from this if you want to create your own
    command styles. Note that Evennia's default commands
    use MuxCommand instead (next in this module).

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    """
    # these need to be specified

    key = "MyCommand"
    aliases = ["mycmd", "myc"]
    locks = "cmd:all()"
    help_category = "General"

    # optional
    # auto_help = False      # uncomment to deactive auto-help for this command.
    # arg_regex = r"\s.*?|$" # optional regex detailing how the part after
                             # the cmdname must look to match this command.

    # (we don't implement hook method access() here, you don't need to
    #  modify that unless you want to change how the lock system works
    #  (in that case see evennia.commands.command.Command))

    def at_pre_cmd(self):
        """
        This hook is called before `self.parse()` on all commands.
        """
        pass

    def parse(self):
        """
        This method is called by the `cmdhandler` once the command name
        has been identified. It creates a new set of member variables
        that can be later accessed from `self.func()` (see below).

        The following variables are available to us:
           # class variables:

           self.key - the name of this command ('mycommand')
           self.aliases - the aliases of this cmd ('mycmd','myc')
           self.locks - lock string for this command ("cmd:all()")
           self.help_category - overall category of command ("General")

           # added at run-time by `cmdhandler`:

           self.caller - the object calling this command
           self.cmdstring - the actual command name used to call this
                            (this allows you to know which alias was used,
                             for example)
           self.args - the raw input; everything following `self.cmdstring`.
           self.cmdset - the `cmdset` from which this command was picked. Not
                         often used (useful for commands like `help` or to
                         list all available commands etc).
           self.obj - the object on which this command was defined. It is often
                         the same as `self.caller`.
        """
        pass

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
        by the `cmdhandler` right after `self.parser()` finishes, and so has access
        to all the variables defined therein.
        """
        self.caller.msg("Command called!")

  #  def at_post_cmd(self):
        """
        This hook is called after `self.func()`.
        """

                   
  #      prompt = "HP:2, MP:1,SP:3" 
  #      self.caller.msg(prompt=prompt)

   #     pass


class MuxCommand(default_cmds.MuxCommand):
    """
    This sets up the basis for Evennia's 'MUX-like' command style.
    The idea is that most other Mux-related commands should
    just inherit from this and don't have to implement parsing of
    their own unless they do something particularly advanced.

    A MUXCommand command understands the following possible syntax:

        name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]

    The `name[ with several words]` part is already dealt with by the
    `cmdhandler` at this point, and stored in `self.cmdname`. The rest is stored
    in `self.args`.

    The MuxCommand parser breaks `self.args` into its constituents and stores them
    in the following variables:
        self.switches = optional list of /switches (without the /).
        self.raw = This is the raw argument input, including switches.
        self.args = This is re-defined to be everything *except* the switches.
        self.lhs = Everything to the left of `=` (lhs:'left-hand side'). If
                     no `=` is found, this is identical to `self.args`.
        self.rhs: Everything to the right of `=` (rhs:'right-hand side').
                    If no `=` is found, this is `None`.
        self.lhslist - `self.lhs` split into a list by comma.
        self.rhslist - list of `self.rhs` split into a list by comma.
        self.arglist = list of space-separated args (including `=` if it exists).

    All args and list members are stripped of excess whitespace around the
    strings, but case is preserved.
    """

    def func(self):
        """
        This is the hook function that actually does all the work. It is called
        by the `cmdhandler` right after `self.parser()` finishes, and so has access
        to all the variables defined therein.
        """
        # this can be removed in your child class, it's just
        # printing the ingoing variables as a demo.
        super(MuxCommand, self).func()




class CmdAbilities(Command):

    key = "abilities"
    aliases = ["abi"]
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
         xp, hitpoints, manapoints, combat, level = self.caller.get_abilities()
         string = "XP: %s, HP: %s, MP: %s, COMBAT: %s, LEVEL: %s" % (xp, hitpoints, manapoints, combat, level)
         self.caller.msg(string)



class CmdMyStats(Command):

    key = "score"
    aliases = ["sc"]
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
         strength, dexterity, charisma, intelligence, stamina, hitpoints, manapoints = self.caller.get_my_stats()

         self.caller.msg("Strength: %i." % strength)
         self.caller.msg("Dexterity: %i." % dexterity)
         self.caller.msg("Charisma: %i." % charisma)
         self.caller.msg("Intelligence: %i." % intelligence)
         self.caller.msg("Stamina: %i." % stamina)
         self.caller.msg("HP: %i." % hitpoints)
         self.caller.msg("MP: %i." % manapoints)

class CmdAttack(Command):
    """
    attack an opponent

    Usage:
      attack <target>

    This will attack a target in the same room, dealing 
    damage with your bare hands. 
    """
    def func(self):
        "Implementing combat"

        if not self.args:
            caller = self.caller
            caller.msg("You need to pick a target to attack.")
            return

        character1 = self.caller
        character2 = self.caller.search(self.args)

        rules.roll_challenge(character1, character2, "combat")





class CmdLook(MuxCommand):
    """
    look at location or object

    Usage:
      look
      look <obj>
      look *<player>

    Observes your location or objects in your vicinity.
    """
    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        args = self.args
        if args:
            # Use search to handle duplicate/nonexistant results.
            looking_at_obj = caller.search(args, use_nicks=True)
            if not looking_at_obj:
                return
        else:
            looking_at_obj = caller.location
            if not looking_at_obj:
                caller.msg("You have no location to look at!")
                return

        if not hasattr(looking_at_obj, 'return_appearance'):
            # this is likely due to us having a player instead
            looking_at_obj = looking_at_obj.character
        if not looking_at_obj.access(caller, "view"):
            caller.msg("Could not find '%s'." % args)
            return
        # get object's appearance
        caller.msg(looking_at_obj.return_appearance(caller))
        # the object's at_desc() method.
        looking_at_obj.at_desc(looker=caller)

       ## Command line prompt stuffz
        hitpoints, manapoints, stamina = self.caller.get_stats()
        prompt = "[{rHP:{y %s,{b MP:{y %s,{g STA:{y %s{n]> " % (hitpoints, manapoints, stamina)
        self.caller.msg(prompt=prompt)
 


class CmdGetSession(Command):


        key = "getsessionid"
        aliases = ["sid"]
        def func(self):
       ## Bad attempt at sending OOB msgs
            sessid = self.caller.sessid.get()[0]
            OOB_HANDLER.execute_cmd(sessid, "ECHO", "Test")
            self.caller.msg("\nSession ID is '%s'. " % sessid)


class CmdTarget(default_cmds.MuxCommand):
            """f.caller
            Simple command example

            Usage: 
              target <text>

            This command simply echoes target text back to the caller.
            """

            key = "target"
            locks = "cmd:all()"

            def func(self):
                "This actually does things" 
                if not self.args:
                    self.caller.msg("You didn't enter anything!")           
                else:
                    self.caller.msg("You are now targeting: '%s'" % self.args)



class CmdGenStats(Command):
    """
    set the stats of a character

    Usage: 
      +genstats

    This generates the stats of the current character. This can only be 
    used during character generation.    
    """

    key = "+genstats"
    help_category = "mush"

    def func(self):
        "This performs the actual command"

        hitpoints = random.randint(5,10)
        self.caller.db.hitpoints = hitpoints
        self.caller.msg("Your current hitpoints was set to %i." % hitpoints)

        manapoints = random.randint(5,10)
        self.caller.db.manapoints = manapoints
        self.caller.msg("Your current manapoints was set to %i." % manapoints)

        strength = random.randint(1, 18)
        self.caller.db.strength = strength
        self.caller.msg("Your Strength was set to %i." % strength)

        dexterity = random.randint(1, 18)
        self.caller.db.dexterity = dexterity
        self.caller.msg("Your Dexterity was set to %i." % dexterity)

        charisma = random.randint(1, 18)
        self.caller.db.charisma = charisma
        self.caller.msg("Your Charisma was set to %i." % charisma)

        intelligence = random.randint(1, 18)
        self.caller.db.intelligence = intelligence
        self.caller.msg("Your Intelligence was set to %i." % intelligence)

        stamina = random.randint(1, 18)
        self.caller.db.stamina = stamina
        self.caller.msg("Your Stamina was set to %i." % stamina)

class CmdCreateNPC(Command):
    """
    create a new npc

    Usage:
    +createNPC <name>

    Creates a new, named NPC.
    """ 
 ### Note the space after the key and aliases. Without it the argument "npc name" will end up with a space in front --SG 
    key = "+createnpc " 
    aliases = ["+createNPC "]
    locks = "call:not perm(nonpcs)"
    help_category = "mush" 

    def func(self):
        "creates the object and names it"
        caller = self.caller
        if not self.args:
            caller.msg("Usage: +createNPC <name>")
            return
        if not caller.location:
            # may not create npc when OOC
            caller.msg("You must have a location to create an npc.")
            return
        # make name always start with capital letter
        name = self.args.capitalize()
        # create npc in caller's location
        npc = create_object("characters.Character", 
                      key=name, 
                      location=caller.location,
                      locks="edit:id(%i) and perm(Builders)" % caller.id)
        # announce 
        message = "%s created the NPC '%s'.\n"
        caller.msg(message % ("You", name)) 
        caller.location.msg_contents(message % (caller.key, name), 
                                                exclude=caller)       

       #Let's set the initial stats for the NPC  --SG

        hitpoints = random.randint(5,10)
        npc.db.hitpoints = hitpoints
        caller.msg("Your current hitpoints was set to %i." % hitpoints)

        manapoints = random.randint(5,10)
        npc.db.manapoints = manapoints
        caller.msg("Your current manapoints was set to %i." % manapoints)
       
        strength = random.randint(1, 18)
        npc.db.strength = strength
        message = "%s's Strength was set to %i."
        caller.msg(message % (name, strength))

        dexterity = random.randint(1, 18)
        npc.db.dexterity = dexterity
        message = "%s's Dexterity was set to %i."
        caller.msg(message % (name, dexterity))

        charisma = random.randint(1, 18)
        npc.db.charisma = charisma
        message = "%s's Charisma was set to %i."
        caller.msg(message % (name, charisma))

        intelligence = random.randint(1, 18)
        npc.db.intelligence = intelligence
        message = "%s's Intelligence was set to %i."
        caller.msg(message % (name, intelligence))

        stamina = random.randint(1, 18)
        npc.db.stamina = stamina
        message = "%s's Stamina was set to %i.\n"
        caller.msg(message % (name, stamina))


class CmdNPC(Command):
    """
    controls an NPC

    Usage: 
        +npc <name> = <command>

    This causes the npc to perform a command as itself. It will do so
    with its own permissions and accesses. 
    """
    key = "+npc"
    locks = "call:not perm(nonpcs)"
    help_category = "mush"

    def parse(self):
        "Simple split of the = sign"
        name, cmdname = None, None
        if "=" in self.args:
            name, cmdname = [part.strip() 
                             for part in self.args.rsplit("=", 1)]
        self.name, self.cmdname = name, cmdname

    def func(self):
        "Run the command"
        caller = self.caller
        if not self.cmdname:
            caller.msg("Usage: +npc <name> = <command>")
            return
        npc = caller.search(self.name)   
        if not npc:
            return
        if not npc.access(caller, "edit"):
            caller.msg("You may not order this NPC to do anything.")
            return
        # send the command order
        npc.execute_cmd(self.cmdname)
        caller.msg("You told %s to do '%s'." % (npc.key, self.cmdname))
      #  npc.execute_cmd(self.cmdname, sessid=self.caller.sessid)

# Menu nodes 


# Menu command to create the menu

class CmdTestMenu(Command):
    """
    Test menu

    Usage:
      testmenu <menumodule>

    Starts a demo menu from a menu node definition module.

    """
    key = "testmenu"

    def func(self):

        if not self.args:
            self.caller.msg("Usage: testmenu menumodule")
            return
        # start menu
        EvMenu(self.caller, self.args.strip(), 
               startnode="test_start_node", 
               cmdset_mergetype="Replace")
