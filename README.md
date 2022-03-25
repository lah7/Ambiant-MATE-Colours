
![Colourful Ubuntu MATE Logo](.github/readme/logo-small.png)

# Ubuntu MATE Colours

[![Test Build](https://github.com/lah7/ubuntu-mate-colours/workflows/Test%20Build/badge.svg?event=push)](https://github.com/lah7/ubuntu-mate-colours/actions?query=workflow%3A%22Test+Build%22)
[![Release](https://img.shields.io/github/release/lah7/ubuntu-mate-colours.svg)](https://github.com/lah7/ubuntu-mate-colours/releases)
[![Snapcraft](https://snapcraft.io/ubuntu-mate-colours/badge.svg)](https://snapcraft.io/ubuntu-mate-colours)

![Screenshot of the 3 themes using custom colours](.github/readme/screenshot@2x.jpg)

This project provides Ubuntu MATE with colour variants for these themes:

* Ambiant-MATE
* Ambiant-MATE-Dark
* Radiant-MATE

In addition to themes and icons, these wallpapers and applications themes
are recoloured too:

| Jazz                  | Wall (Logo and Text)              | Wall (Logo)     |
| :-------------------: | :-------------------------------: | :-------------: |
| ![](.github/readme/wall-jazz.jpg) | ![](.github/readme/wall-logo-text.jpg) | ![](.github/readme/wall-logo.jpg)

| Wall                  | Splash                            | Plank
| :-------------------: | :-------------------------------: | :-------------: |
| ![](.github/readme/wall.jpg) | ![](.github/readme/wall-splash.jpg) | ![](.github/readme/plank.jpg)


## Colours

Packages are made for the following pre-defined colours:

| Aqua                  | Blue                  | Brown                  | Orange                  | Pink                  | Purple                  | Red                  | Teal                  | Yellow                  |
| :-------------------: | :-------------------: | :--------------------: | :---------------------: | :-------------------: | :---------------------: | :------------------: | :-------------------: | :---------------------: |
| ![](.github/readme/aqua.png) | ![](.github/readme/blue.png) | ![](.github/readme/brown.png) | ![](.github/readme/orange.png) | ![](.github/readme/pink.png) | ![](.github/readme/purple.png) | ![](.github/readme/red.png) | ![](.github/readme/teal.png) | ![](.github/readme/yellow.png) |
| `#2DACD4`             | `#5489CF`             | `#965024`              | `#E95420`               | `#E231A3`             | `#7E5BC5`               | `#CE3A3A`            | `#1CB39F`             | `#DFCA25`               |

Packages are split by colour, so installing `ubuntu-mate-colours-blue` will
give you the blue variants of the GTK and icon themes.

    sudo apt install ubuntu-mate-colours-blue

Want them all? That's roughly 35 MB download, 550 MB unpacked!

    sudo apt install ubuntu-mate-colours-all

After installing, themes/icons will be available from **Appearance** (Look & Feel).


## Ubuntu MATE Welcome (18.04 to 21.10)

Users of Ubuntu MATE between releases 18.04 and 21.10 can conveniently access
this feature via the **Welcome** application:

![Screenshot of Colour Selection in Ubuntu MATE Welcome](.github/readme/welcome.png)

This adds the older [lah7/ubuntu-mate-colours PPA](https://launchpad.net/~lah7/+archive/ubuntu/ubuntu-mate-colours/),
which is now discontinued.


### Snap Compatibility

In order for the theme to work in snapped applications, you will need to
install the snap in addition:

    sudo snap install ubuntu-mate-colours

Then, "plug" this snap to all the other snaps:

    for PLUG in $(snap connections | grep gtk-common-themes:gtk-3-themes | awk '{print $2}'); do sudo snap connect ${PLUG} ubuntu-mate-colours:gtk-3-themes; done
    for PLUG in $(snap connections | grep gtk-common-themes:gtk-2-themes | awk '{print $2}'); do sudo snap connect ${PLUG} ubuntu-mate-colours:gtk-2-themes; done
    for PLUG in $(snap connections | grep gtk-common-themes:icon-themes | awk '{print $2}'); do sudo snap connect ${PLUG} ubuntu-mate-colours:icon-themes; done

To snap an individual application, such as Firefox:

    sudo snap connect firefox:gtk-3-themes ubuntu-mate-colours:gtk-3-themes

This step may need to be repeated when installing new snaps to the system.

Please note that the snap only provides compatibility for snapped applications. It cannot
be selected as the theme in MATE's **Appearance** settings.


## Building

1. To begin, make sure you have a clone of this repository.

       git clone https://github.com/lah7/ubuntu-mate-colours

1. Install the dependencies:

       sudo apt install librsvg2-bin imagemagick

1. (Optional) Download a copy of Ambiant-MATE.

    Skip this step if you have the theme already installed on your system.

       git clone https://github.com/lah7/Ambiant-MATE

1. Use the [generate-ambiant-mate-colour.py](generate-ambiant-mate-colour.py)
script, which will create a copy and rewrites known colours to new colour
values. Some image assets will be recoloured using Imagemagick.

    By default, the theme is created in `~/.themes` and `~/.icons`, making it
available only to the local user.

    The tool is entirely command line and parameter based. For usage:

       ./generate-ambiant-mate-colour.py --help


#### Tweaks

Ambiant-MATE/Radiant-MATE themes can optionally apply 'tweaks' to modify the
themes even further:

| Tweak Name             | Theme                | Description                  |
| ---------------------- | -------------------- | ---------------------------- |
| `mono-osd-icons`       | Ambiant/Radiant-MATE | [Use monochrome icons for OSD volume pop up (#14)](https://github.com/lah7/ubuntu-mate-colours/issues/14)
| `black-selected-text`  | Ambiant/Radiant-MATE | [The selected text colour is black instead of white (#21)](https://github.com/lah7/ubuntu-mate-colours/issues/21)
| `gtk3-classic`         | Ambiant/Radiant-MATE | [Append treeview alternating styling](https://github.com/lah7/gtk3-classic/wiki/Treeview:-Alternating-Colours-CSS) for use with the [gtk3-classic](https://github.com/lah7/gtk3-classic) project.

These are passed as a comma separated parameter to `--tweaks`.


## Packaging

A local package can be produced by running:

    debuild -b

Note that this runs through the entire `scripts/build.sh` script, which takes a
long time to process. A RAM disk is strongly recommended.

Alternately, to produce a complete colour collection:

    scripts/build.sh
    tar -cv usr/ | xz -z -9 > ubuntu-mate-colours-VERSION.tar.xz


## Development Tips

### Inspect GTK+3 Themes

The inspector allows you to figure out the classes and properties used to make
up the theme. First, make sure you have the development files installed:

    sudo apt install libgtk-3-dev

Set this environment variable and launch the application:

    export GTK_DEBUG=interactive
    pluma

[More information on the Ubuntu MATE Community.](https://ubuntu-mate.community/t/20150)


### Test with the Widget Factory

The Widget Factory is a basic application with generic controls, useful for testing
the theme and icons. This is provided in the GTK+3 examples package:

    sudo apt install gtk-3-examples

To launch:

    gtk3-widget-factory

(You can edit your MATE menu to show this application, it's under "Programming")


## License

This program is licensed under the GPLv3.

[`Ambiant-MATE`] is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License].


[`Ambiant-MATE`]: https://github.com/lah7/Ambiant-MATE
[Creative Commons Attribution-ShareAlike 4.0 License]: https://creativecommons.org/licenses/by-sa/4.0/
