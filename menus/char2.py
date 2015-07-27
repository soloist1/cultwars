# Menu nodes 
from commands.command import CmdMySkills

def test_start_node(caller):
    text = """
    {mThis is a {yTEST{m faction selection menu.

    Select options or use {y'quit'{m to exit the menu.

    Choose your faction below.{n
    """
    options = ({"key": ("{r1)-{y A{nnarchist", "a", "1"),
                "desc": "Choose the Anarchist faction",
                "exec": lambda caller: caller.attributes.add("faction", "Anarchist"),
                "goto": "test_set_skilltree"},
               {"key": ("{r2)-{y R{neligious", "r", "2"),
                "desc": "Choose the Religious faction",
                "exec": lambda caller: caller.attributes.add("faction", "Religious"),
                "goto": "test_set_skilltree"},
               {"key": ("{r3)-{y L{naw Enforcement", "l", "3"),
                "desc": "Choose the Law Enforcement faction",
                "exec": lambda caller: caller.attributes.add("faction", "Law Enforcement"),
                "goto": "test_set_skilltree"},
         #      {"key": ("{y V{niew", "v"),
         #       "desc": "View your currently chosen faction.",
         #       "goto": "test_view_node"},
               {"key": ("{r4)-{y Q{nuit", "quit", "q", "Q", "4"),
                "desc": "Quit this menu.",
                "goto": "test_end_node"},
               {"key": "_default",
                "goto": "test_displayinput_node"})
    return text, options


def test_set_node(caller):

    text = ("""
    {m The characters faction was set to{y %s
    {m Meta was set to{y %s {n
    {m Skill tree was set to{y %s {n
    ({wCheck it with examine after quitting the menu{n).

    """ % (caller.db.faction, caller.db.Meta, caller.db.skilltree))

    options = ({"key": ("{r1)-{y B{nack (default)", "_default", "1"),
               "desc": "Back to main menu",
               "goto": "test_start_node"})
    return text, options


def test_set_skilltree(caller):
    if caller.db.faction == 'Anarchist':
        caller.attributes.add("Meta", "Idealogical")
    elif caller.db.faction == 'Religious':
        caller.attributes.add("Meta", "Spiritual")
    elif caller.db.faction == 'Law Enforcement':
        caller.attributes.add("Meta", "Judicial"),

    text = ("""
    {m The characters faction was set to{y %s
    {m Meta was set to{y %s {n
    

    {mThis is a {yTEST{m skill tree selection menu.
    Choose your skill tree below.{n
    """ % (caller.db.faction, caller.db.Meta))
    options = ({"key": ("{r1)-{yT{nechnological", "t", "1"),
                "desc": "Choose the Technological skill tree",
                "exec": lambda caller: caller.attributes.add("skilltree", "Technological"),
                "goto": "test_skills_node"},
               {"key": ("{r2)-{yN{natural", "n", "2"),
                "desc": "Choose the Natural skill tree",
                "exec": lambda caller: caller.attributes.add("skilltree", "Natural"),
                "goto": "test_skills_node"},
               {"key": ("{r3)-{yP{nhysical", "p", "3"),
                "desc": "Choose the Physical skill tree",
                "exec": lambda caller: caller.attributes.add("skilltree", "Physical"),
                "goto": "test_skills_node"})
    return text, options

def test_skills_node(caller):


#### This is *way* wrong, but will suffice for testing.
#### Eventually a better system will need to be worked out.
#### Skills and attributes will need to be designed into a character class --SG

    if caller.db.skilltree == 'Technological':
     caller.attributes.add("Skills", "3")
     caller.db.skills = {'Computers':"1", 'Scavenging':"2", 'Targeting':"3"}  
    elif caller.db.skilltree == 'Physical':
     caller.db.skills = {'Grappling':"1", 'Hand to Hand':"2", 'Speed':"3"}
    elif caller.db.skilltree == 'Natural':
     caller.db.skills = {'Botany':"1", 'Tracking':"2", 'Crafting':"3"}

    text = ("""
    {mYour faction is {y%s{m!
    {mMeta is {y%s{m. {n
    {mYour skill tree is {y%s{m. {n
    
    {mYour skills are:
    {mNow we choose some skill based on your skill tree. {n

    """ % (caller.db.faction, caller.db.Meta, caller.db.skilltree))
    
    for k,v in caller.db.skills.items():
            caller.msg("{W" + k + "{n:{m " +v+ " ")
   
    

          
    options = ({"key": ("{r1)-{y B{nack (default)", "_default", "1"),
               "desc": "Back to main menu",
               "goto": "test_start_node"})
    return text, options



def test_view_node(caller):
    text = ("""
    {mYour faction is {y%s{m!
    {mMeta is {y%s{m. {n
    {m%s, %s, %s, %s, %s, %s 
    """ % (caller.db.faction, caller.db.Meta, caller.db.skills))
    options = {"desc": "back to main",
               "goto": "test_start_node"}
    return text, options

def  test_displayinput_node(caller, raw_string):
    text = """
    You entered the text:

        "%s"

    """ % raw_string
    options = {"key": "_default",
              "goto": "test_start_node"}
    return text, options


def test_end_node(caller):
    text = """
    This is the end of the menu and since it has no options the menu
    will exit here, followed by a call of the "look" command.
    """
    return text, None
