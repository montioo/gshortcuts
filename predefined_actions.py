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
Disables predefined keybindings.
"""

import subprocess


def disable_show_desktop():
    """Unbinds <Super><Alt>d from hiding all windows."""
    cmd = 'gsettings set org.gnome.desktop.wm.keybindings show-desktop "[]"'
    subprocess.call(["/bin/bash", "-c", cmd])

def disable_launch_terminal():
    """Unbinds <Ctrl><Alt>t from launching a terminal window."""
    cmd = 'gsettings set org.gnome.settings-daemon.plugins.media-keys terminal "[]"'
    subprocess.call(["/bin/bash", "-c", cmd])