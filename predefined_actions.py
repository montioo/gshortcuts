#!/usr/bin/env python3

#
# predefined_actions.py
# gshortcuts
#
# Created: November 2020
# Author: Marius Montebaur
# montebaur.tech, github.com/montioo
#

"""
Disables predefined keybindings and various other functions.

Take those as examples to define your own commands.
Find commands you are looking for with
$ gsettings list-recursively | grep "show-desktop"
"""

import subprocess
from .custom_actions import set_gsetting


### Disabling predefined shortcuts

def disable_show_desktop():
    """Unbinds <Super><Alt>d from hiding all windows."""
    sp, key, value = 'org.gnome.desktop.wm.keybindings', 'show-desktop', '"[]"'
    set_gsetting(sp, key, value)

def disable_launch_terminal():
    """Unbinds <Ctrl><Alt>t from launching a terminal window."""
    sp, key, value = 'org.gnome.settings-daemon.plugins.media-keys', 'terminal', '"[]"'
    set_gsetting(sp, key, value)

def disable_switch_workspace_left_right():
    """Disables left/right workspace shortcut to free Ctrl Alt Left/Right."""
    cmds = [
        ("org.gnome.desktop.wm.keybindings", "switch-to-workspace-left", "[]"),
        ("org.gnome.desktop.wm.keybindings", "switch-to-workspace-right", "[]")
    ]
    for cmd in cmds:
        set_gsetting(*cmd)


### Various other Gnome settings

def enable_dock_autohide():
    """Hides the dock automatically to make more room for windows."""
    cmds = [
        ("org.gnome.shell.extensions.dash-to-dock", "dock-fixed", "false"),
        ("org.gnome.shell.extensions.dash-to-dock", "autohide", "true")
    ]
    for cmd in cmds:
        set_gsetting(*cmd)

def disable_edge_tiling():
    """Disabling gnome's standard functionality where dragging a window to
    the screen's edge will allign it with a part of the screen."""
    cmd = "org.gnome.mutter", "edge-tiling", "false"
    set_gsetting(*cmd)
