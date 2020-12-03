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


# Settings in gsettings are identified by a schema and a key
shortcut_schema = "org.gnome.settings-daemon.plugins.media-keys"
shortcut_key = "custom-keybindings"


def set_gsetting(schema_path, key, value):
    cmd = f'gsettings set {schema_path} {key} "{value}"'
    subprocess.call(["/bin/bash", "-c", cmd])

def get_gsetting(schema_path, key):
    cmd = f"gsettings get {schema_path} {key}"
    return subprocess.check_output(["/bin/bash", "-c", cmd]).decode("utf-8")

def query_all_shortcuts() -> List[str]:
    """Returns a string of currently installed custom shortcut identifiers.

    Returns a list of installed shortcut identifiers, each represented as a string like
    `/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/SHORTCUT_NAME/`.
    """

    entry_str = get_gsetting(shortcut_schema, shortcut_key)
    entry_str = entry_str.lstrip("@as")  # an empty list entry starts with: `@as []`

    # entry_str looks like a list and can be converted to a python object
    return eval(entry_str)


def overwrite_shortcut_list(shortcuts: List[str]):
    """Overwrites the complete list of custom shortcuts.

    Removes all installed custom shortcuts. Instead activates the shortcuts
    whose identifiers are given in the list `shortcuts`. Shortcuts that are
    not supposed to be removed but should be kept, have to be in the list
    that this function receives. Every identifier needs to have the format
    `/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/SHORTCUT_NAME/`.
    The `SHORTCUT_NAME` is later used to refer to this shortcut and edit its
    properties (like keybinding and command).

    Parameters
    ----------
    shortcuts: List[str]
        A list of shortcut identifiers to install / keep.
    """
    set_gsetting(shortcut_schema, shortcut_key, shortcuts)


def remove_shortcuts_with_prefix(name_prefix: str):
    """Removes all shortcuts with a name starting with the given prefix.

    All custom shortcuts are stored with the identifier
    `/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/SHORTCUT_NAME/`.
    This function will remove every shortcut from Gnome's settings that has a
    SHORTCUT_NAME starting with `name_prefix`. If `name_prefix` is an empty
    string (i.e. `""`), all custom shortcuts will be removed.

    Parameters
    ----------
    name_prefix : str
        prefix string of a keybinding.
    """

    current = query_all_shortcuts()

    # expects shortcut identifier to end with '/'
    # keeps only shortcuts that have a name that doesn't start with name_prefix
    to_keep = list(filter(lambda p: not p.split('/')[-2].startswith(name_prefix), current))

    overwrite_shortcut_list(to_keep)

def remove_shortcut(name: str):
    """Removes a shortcut that is given by its name."""
    current = query_all_shortcuts()

    to_keep = list(filter(lambda p: p.split('/')[-2] != name, current))

    overwrite_shortcut_list(to_keep)


def set_new_shortcut(name, command, binding):
    """Creates a new shortcuts.

    Creates a new custom shortcut in Gnome's settings. The new identifier of this shortcut is
    `/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/<name>/`.

    Parameters
    ----------
    name: str
        Name referring to the shortcut's functionality.
    command: str
        Shell command to execute when this shortcut is triggered.
    binding: str
        Key presses to react to, e.g. `<Ctrl><Alt>f`. To learn more about
        possible bindings and their format, look into the module's `README.md`.
    """

    current = query_all_shortcuts()

    shortcut_id_base = "/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"
    new_shortcut_identifier = f"{shortcut_id_base}/{name}/"

    current.append(new_shortcut_identifier)
    overwrite_shortcut_list(current)

    # schema for setting a key is followed by the identifier
    schema = f"{shortcut_schema}.custom-keybinding:{new_shortcut_identifier}"
    key_value_pairs = [
        ("name", name),
        ("command", command),
        ("binding", binding)
    ]

    for k, v in key_value_pairs:
        set_gsetting(schema, k, v)


