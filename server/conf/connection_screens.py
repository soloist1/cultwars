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
 {ymystats -{n (alias - mstat) shows your base stats
 {y+createnpc {rNPC NAME{n-{r ONLY IN NPC ROOM{n will spawn a new npc 
    initial stats will be rolled for the npc when created

          {r**** {mNew Locations{r ****{n

 {yCharacter Creation Room {Wdbref #91 -{n north of Infirmary
 {yNPC Room {Wdbref #99 -{n east of Character Creation
 {yEquipment Room {Wdbref #95 -{n west of Character Creation
{b=============================================================={n"""\
 % (settings.SERVERNAME)
