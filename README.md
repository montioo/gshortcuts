# gshortcuts

*Brief:* Wrapper for Gnome settings (default desktop environment in Ubuntu and Fedora) to set and unset keyboard shortcuts. Interface is idempotent (i.e. it won't cause problems if executed multiple times) and can thus be used with tools for installing dotfiles.

License: MIT

Author: Marius Montebaur ([website](https://www.montebaur.tech))

---

gshortcuts uses the gsettings command line interface to access and change the
keyboard shortcuts in Gnome. When a new shortcut is created, it is associated
with a name gshortcuts is idempotent, i.e. it is able to run multiple times
without causing any problems.


## Usage examples:

A very simple example that makes `<Ctrl><Alt>m` move a window to the upper left corner of the screen is given below:

(xdotool needs to be installed)

```python
from gshortcuts.custom_actions import set_new_shortcut

set_new_shortcut(
    "window_layout_move_to_top_left",  # name
    "xdotool getactivewindow windowmove 0 0",  # shell command to execute
    "<Ctrl><Alt>m"  # shortcut to listen to
)
```

Using gshortcuts becomes really handy when custom scripts are triggered by a shortcut. A script that uses gshortcuts can be executed after setting up a new computer to immediately have all keybindings available.


```python
from gshortcuts.custom_actions import remove_shortcuts_with_prefix, remove_shortcut

# removes all shortcuts with this prefix
remove_shortcuts_with_prefix("window_layout")

# removes only this exact shortcut
remove_shortcut("window_layout_move_to_top_left")
```

## Keybinding Structure

Some characters have special representations when setting them as a keybinding, e.g.
`'` is stored as `apostrophe` and `]` as `bracketleft`.

To find out stuff like this, create a keybinding manually in Ubuntu's settings and then run:
```
gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ binding
```
to get the keybinding. If you have already created multiple custom shortcuts using the GUI, the identifier of the one you just created by hand might be >0, e.g. `/custom1/`


## Altering existing shortcuts:

Existing shortcuts that are predefined by the system can be listed with

```bash
gsettings list-keys org.gnome.desktop.wm.keybindings
```

Those can be disabled to use the key binding for a different purpose with
```bash
gsettings set   org.gnome.desktop.wm.keybindings   show-desktop    "[]"
                --------------------------------   ------------    ----
                           schema                      key         value
```
which is already defined in `gshortcuts.predefined_actions`.

gshortcuts provides a function that, given a schema, key and value (the latter without the double quotes), will adjust the settings for you:
```python
from gshortcuts.custom_actions import set_gsetting

schema, key, value = 'org.gnome.desktop.wm.keybindings', 'show-desktop', '[]'
set_gsetting(schema, key, value)
```


## Search all settings:

To search all keys of Gnome's settings for a specific entry, use the command below:

```bash
gsettings list-recursively | grep terminal
```

This will give you the schema, key and value as an output. You can then use this information to adjust this setting with gshortcuts.

Since a schema and a key might not be very informative to understand what influence a setting has on your system, you can use
```bash
gsettings describe <schema> <key>
```
to get more a description on what a setting changes. For example:

```bash
gsettings describe org.gnome.shell.extensions.dash-to-dock dock-fixed
```
