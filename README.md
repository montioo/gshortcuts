# gshortcuts

*Brief:* Wrapper for Gnome settings (default desktop environment in Ubuntu and Fedora) to set and unset keyboard shortcuts. Interface is idempotent (i.e. it won't cause problems if executed multiple times) and can thus be used with tools for installing dotfiles.

License: MIT

Author: Marius Montebaur ([website](www.montebaur.tech))

---

gshortcuts uses the gsettings command line interface to access and change the keyboard shortcuts
in Gnome. When a new shortcut is created, it is associated with a domain
which groups the use of this shortcut. This is not something that is
established by gsettings or Gnome but by this gshortcuts. gshortcuts should be
idempotent, i.e. it should be able to run multiple times without causing any
problems. A script that sets commands from one domain can thus delete all
commands from this before setting them again.


## Usage examples:

A very simple example that makes `<Ctrl><Alt>m` move a window to the upper left corner of the screen is given below:

(xdotool needs to be installed)

```python
from gshortcuts.custom_actions import set_new_shortcut

set_new_shortcut(
    "window_layout",  # domain (groups commands)
    "move_to_top_left",  # name
    "xdotool getactivewindow windowmove 0 0",  # shell command to execute
    "<Ctrl><Alt>m"  # shortcut to listen to
)
```

Using gshortcuts becomes really hands when custom scripts are triggered by a shortcut. A script that uses gsettings can be executed after setting up a new computer to immediately have all keybindings available.

Removing a group (i.e. domain) of shortcuts is shown below:

```python
from gshortcuts.custom_actions import remove_shortcuts_with_domain, remove_shortcut

# removes all shortcuts with this domain
remove_shortcuts_with_domain("window_layout")

# removes only this exact shortcut
remove_shortcut("window_layout", "move_to_top_left")
```

## Keybinding Structure

Some characters have special representations when setting them as a keybinding, e.g.
`'` is stored as `apostrophe` and `]` as `bracketleft`.

To find out stuff like this, create a keybinding manually in Ubuntu's settings and then run:
```
gsettings get org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ binding
```
to get the keybinding. Replace custom0 with whatever the number of the shortcut is.


## Altering existing shortcuts:

Existing shortcuts that are predefined by the system can be listed with

```bash
gsettings list-keys org.gnome.desktop.wm.keybindings
```

Those can be disabled to use the key binding for a different purpose with
```bash
gsettings set org.gnome.desktop.wm.keybindings show-desktop "[]"
```
which is already defined in `gshortcuts.predefined_actions`.


## Search all settings:

To search all keys of Gnome's settings for a specific entry, use the command below:

```bash
gsettings list-recursively | grep terminal
```
