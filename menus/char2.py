# Menu nodes 

def test_start_node(caller):
    text = """
    {mThis is a {yTEST{m faction selection menu.

    Select options or use {y'quit'{m to exit the menu.

    Choose your faction below.{n
    """
    options = ({"key": ("{ya) {nAnarchist", "a"),
                "desc": "Choose the Anarchist faction",
                "exec": lambda caller: caller.attributes.add("faction", "Anarchist"),
            #    "exec": lambda callerm: caller.attributes.add("Meta", "Idealogical"),
                "goto": "test_set_node"},
               {"key": ("{yr) {nReligious", "r"),
                "desc": "Choose the Religious faction",
                "exec": lambda caller: caller.attributes.add("faction", "Religious"),
            #    "exec": lambda callerm: caller.attributes.add("Meta", "Spiritual"),
                "goto": "test_set_node"},
               {"key": ("{yl) {nLaw Enforcement", "l"),
                "desc": "Choose the Law Enforcement faction",
                "exec": lambda caller: caller.attributes.add("faction", "Law Enforcement"),
             #   "exec": lambda callerm: caller.attributes.add("Meta", "Judicial"),
                "goto": "test_set_node"},
               {"key": ("{yv) {nView", "v"),
                "desc": "View your currently chosen faction.",
                "goto": "test_view_node"},
               {"key": ("{yq) {nQuit", "quit", "q", "Q"),
                "desc": "Quit this menu.",
                "goto": "test_end_node"},
               {"key": "_default",
                "goto": "test_displayinput_node"})
    return text, options


def test_set_node(caller):

    if caller.db.faction == 'Anarchist':
        caller.attributes.add("Meta", "Idealogical")
    elif caller.db.faction == 'Religious':
        caller.attributes.add("Meta", "Spiritual")
    elif caller.db.faction == 'Law Enforcement':
        caller.attributes.add("Meta", "Judicial"),
    text = ("""
    The characters faction was set to

            %s
    Meta was set to 

            
    (check it with examine after quitting the menu).

    """ % caller.db.faction)

    # optional help text for this node
    options = ({"key": ("back (default)", "_default"),
               "desc": "back to main",
               "goto": "test_start_node"},
               {"key": ("Skills", "s"), 
               "desc": "to skill menu",
               "goto": "test_set_skills"})
    return text, options


def test_set_skills(caller):
    text = """
    {mThis is a {yTEST{m skills selection menu.

    Nothing much happening here until it gets fleshed out.

    Choose your skills below.{n
    """
    options = ({"key": ("{yt) {nTechnological", "t"),
                "desc": "Choose the Technological skill tree",
                "exec": lambda caller: caller.attributes.add("skilltree", "Technological"),
                "goto": "test_set_node"},
               {"key": ("{yn) {nNatural", "n"),
                "desc": "Choose the Natural skill tree",
                "exec": lambda caller: caller.attributes.add("skilltree", "Natural"),
                "goto": "test_set_node"},
               {"key": ("{yp) {nPhysical", "p"),
                "desc": "Choose the Physical skill tree",
                "exec": lambda caller: caller.attributes.add("skilltree", "Physical"),
                "goto": "test_set_node"})
    return text, options




def test_view_node(caller):
    text = """
    Your faction is %s!

    """ % caller.db.faction
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
