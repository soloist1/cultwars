# -*- coding: utf-8 -*-
"""
Connection screen

Texts in this module will be shown to the user at login-time.

Evennia will look at global string variables (variables defined
at the "outermost" scope of this module and use it as the
connection screen. If there are more than one, Evennia will
randomize which one it displays.

The commands available to the user when the connection screen is shown
are defined in commands.default_cmdsets.UnloggedinCmdSet and the
screen is read and displayed by the unlogged-in "look" command.

"""

from django.conf import settings
from evennia import utils

CONNECTION_SCREEN = \
"""{b=============================================================={n
 Welcome to {g%s{n, Version 0.01!

 If you have an existing account, connect to it by typing:
      {wconnect <username> <password>{n
 If you need to create an account, type (without the <>s):
      {wcreate <username> <password>{n

 If you have spaces in your username, enclose it in quotes.
 Enter {whelp{n for more info. {wlook{n will re-show this screen.

           {r**** {mNew Commands{r ****{n

 {ytarget -{n echoes target string
 {yabilities -{n shows some initial generic abilities
 {y+genstats -{r ONLY IN CREATION ROOM{n generates some base stats
 {yscore -{n (alias - sc) shows your base stats
 {y+createnpc {rNPC NAME {n will spawn a new npc 
    initial stats will be rolled for the npc when created
 {y+npc {rNPC NAME{n = {rACTION (ex. say Hello.){n
    makes NPC perform action
 {ygetsessionid -{n (alias - sid) Uhm, returns session id
 {ytestmenu {rMENU NAME{n runs the new menu system, the first menu
    is 'fmenu', for selecting a faction.

          {r**** {mNew Locations{r ****{n

 {yCharacter Creation Room {Wdbref #91 -{n north of Infirmary
 
 {yEquipment Room {Wdbref #95 -{n west of Character Creation


         {r**** {mFixes/Changes{r ****{n 

 Prompt now displays your true stats
 Workaround for capitalize() for npc generation, see comments
{b=============================================================={n"""\
 % (settings.SERVERNAME)
