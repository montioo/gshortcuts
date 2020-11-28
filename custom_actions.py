#!/usr/bin/env python3

#
# custom_actions.py
# gshortcuts
#
# Created: November 2020
# Author: Marius Montebaur
# montebaur.tech, github.com/montioo
#

import subprocess
from typing import List


settings_key = "org.gnome.settings-daemon.plugins.media-keys custom-keybindings"

def query_all_shortcuts() -> List[str]:
    """Returns a string of currently installed custom shortcut identifiers.

    Returns a list of installed shortcut identifiers, each represented as a string like
    `/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/SHORTCUT_NAME/`.
    """

    cmd = "gsettings get " + settings_key
    entry_str = subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8")
    entry_str = entry_str.lstrip("@as")  # an empty list entry looks like: `@as []`

    # entry_str looks like a list and can be converted
    return eval(entry_str)


def overwrite_shortcut_list(shortcuts: List[str]):
    """Overwrites the complete list of custom shortcuts.

    Removes all installed custom shortcuts. Instead activates the shortcuts
    whose identifiers are given in the list `shortcuts`. Shortcuts are are
    not supposed to be removed but should be kept also have to be in the list
    that this function receives. Every identifier needs to have the format
    `/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/SHORTCUT_NAME/`.
    The `SHORTCUT_NAME` is later used to refer to this shortcut and edit its
    properties (like keybinding and command).

    Parameters
    ----------
    shortcuts: List[str]
        A list of shortcut identifiers to install / keep.
    """
    cmd = "gsettings set " + settings_key + f' "{shortcuts}"'
    subprocess.call(["/bin/bash", "-c", cmd])


def remove_shortcuts_with_domain(domain: str):
    """Removes all shortcuts with a name starting with domain.

    All custom shortcuts are stored with the identifier
    `/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/SHORTCUT_NAME/`.
    This function will remove every shortcut from Gnome's settings that has
    a SHORTCUT_NAME starting with `domain`. If `domain` is an empty string
    (i.e. `""`), all custom shortcuts will be removed.

    Parameters
    ----------
    domain : str
        prefix string of a keybinding.
    """

    current = query_all_shortcuts()

    # expects shortcut identifier to end with '/'
    # keeps only shortcuts that have a name that doesn't start with domain
    to_keep = list(filter(lambda p: not p.split('/')[-2].startswith(domain), current))

    overwrite_shortcut_list(to_keep)

def remove_shortcut(domain: str, title: str):
    """Removes a shortcut that is given by its domain and title."""
    current = query_all_shortcuts()

    name = f"{domain}_{title}"
    to_keep = list(filter(lambda p: p.split('/')[-2] != name, current))

    overwrite_shortcut_list(to_keep)


def set_new_shortcut(domain, title, command, binding):
    """Creates a new shortcuts.

    Creates a new custom shortcut in Gnome's settings. The new identifier of this shortcut looks
    `/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/<domain>_<title>/`.
    The domain is like a group of functionalities this shortcut belongs to. For example
    `/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/windowcontrols_maximize/`.

    Parameters
    ----------
    domain: str
        Prefix for the name of a shortcut used in its identifier.
    title: str
        Postfix for the name referring to the shortcuts functionality.
    command: str
        Shell command to execute when this shortcut is triggered.
    binding: str
        Key presses to react to, e.g. `<Ctrl><Alt>f`. To learn more about
        possible bindings and their format, look into the module's `README.md`.
    """

    current = query_all_shortcuts()

    shortcut_base = "/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"
    new_shortcut = f"{shortcut_base}/{domain}_{title}/"

    current.append(new_shortcut)

    overwrite_shortcut_list(current)

    # Attention: This one is different. Accessing only one keybinding, thus singular.
    # and space replaced with dot.
    skd = "org.gnome.settings-daemon.plugins.media-keys.custom-keybinding"
    set_name = f"gsettings set {skd}:{new_shortcut} name '{title}'"
    set_cmd  = f"gsettings set {skd}:{new_shortcut} command '{command}'"
    set_key  = f"gsettings set {skd}:{new_shortcut} binding '{binding}'"

    for cmd in [set_name, set_cmd, set_key]:
        subprocess.call(["/bin/bash", "-c", cmd])

