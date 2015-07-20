# Menu nodes 

def test_start_node(caller):
    text = """
    This is an example menu.

    If you enter anything except the valid options, your input will be
    recorded and you will be brought to a menu entry showing your
    input.

    Select options or use 'quit' to exit the menu.
    """
    options = ({"key": ("Set", "s"),
                "desc": "**** TEST ****Set an attribute on yourself.",
                "exec": lambda caller: caller.attributes.add("menuattrtest", "Test value"),
                "goto": "test_set_node"},
               {"key": ("View", "v"),
                "desc": "*** TEST ***View your own name",
                "goto": "test_view_node"},
               {"key": ("Quit", "quit", "q", "Q"),
                "desc": "** Quit ** this menu example.",
                "goto": "test_end_node"},
               {"key": "_default",
                "goto": "test_displayinput_node"})
    return text, options


def test_set_node(caller):
    text = ("""
    The attribute 'menuattrtest' was set to

            %s

    (check it with examine after quitting the menu).

    This node's has only one option, and one of its key aliases is the
    string "_default", meaning it will catch any input, in this case
    to return to the main menu.  So you can e.g. press <return> to go
    back now.
    """ % caller.db.menuattrtest,

    # optional help text for this node
    """
    This is the help entry for this node. It is created by returning
    the node text as a tuple - the second string in that tuple will be
    used as the help text.
    """)
    options = {"key": ("back (default)", "_default"),
               "desc": "back to main",
               "goto": "test_start_node"}
    return text, options


def test_view_node(caller):
    text = """
    Your name is %s!

    This node's option has no explicit key (nor the "_default" key
    set), and so gets assigned a number automatically. You can infact
    -always- use numbers (1...N) to refer to listed options also if you
    don't see a string option key (try it!).
    """ % caller.key
    options = {"desc": "back to main",
               "goto": "test_start_node"}
    return text, options

def  test_displayinput_node(caller, raw_string):
    text = """
    You entered the text:

        "%s"

    ... which could now be handled or stored here in some way if this
    was not just an example.

    This node has an option with a single alias "_default", which
    makes it hidden from view. It catches all input (except the
    in-menu help/quit commands) and will, in this case, bring you back
    to the start node.
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
