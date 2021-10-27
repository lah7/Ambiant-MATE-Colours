
![Colourful Ubuntu MATE Logo](.github/readme/logo-small.png)

# Ubuntu MATE Colours

[![Test Build](https://github.com/lah7/ubuntu-mate-colours/workflows/Test%20Build/badge.svg?event=push)](https://github.com/lah7/ubuntu-mate-colours/actions?query=workflow%3A%22Test+Build%22)
[![Release](https://img.shields.io/github/release/lah7/ubuntu-mate-colours.svg)](https://github.com/lah7/ubuntu-mate-colours/releases)
[![Upstream](https://img.shields.io/github/release/ubuntu-mate/ubuntu-mate-artwork.svg?label=upstream)](https://github.com/ubuntu-mate/ubuntu-mate-artwork/releases)
[![Snapcraft](https://snapcraft.io/ubuntu-mate-colours/badge.svg)](https://snapcraft.io/ubuntu-mate-colours)

![Screenshot of the 3 themes using custom colours](.github/readme/screenshot@2x.jpg)

This project provides Ubuntu MATE with colour variants for these themes:

* Ambiant-MATE
* Ambiant-MATE-Dark
* Radiant-MATE
* Yaru-MATE-Light (21.04 onwards)
* Yaru-MATE-Dark (21.04 onwards)

In addition to themes and icons, these wallpapers and applications themes
are recoloured too:

| Jazz                  | Wall (Logo and Text)              | Wall (Logo)     |
| :-------------------: | :-------------------------------: | :-------------: |
| ![](.github/readme/wall-jazz.jpg) | ![](.github/readme/wall-logo-text.jpg) | ![](.github/readme/wall-logo.jpg)

| Wall                  | Splash                            | Plank
| :-------------------: | :-------------------------------: | :-------------: |
| ![](.github/readme/wall.jpg) | ![](.github/readme/wall-splash.jpg) | ![](.github/readme/plank.jpg)


## Supported Releases

| Release   | Codename | Ambiant*-MATE | Yaru-MATE |
| --------- | -------- | ------------- | --------- |
| 21.10     | Impish   | ✔️            | ✔️
| 21.04     | Hirsute  | ✔️            | ✔️
| 20.04 LTS | Focal    | ✔️            | ❌
| 18.04 LTS | Bionic   | ✔️            | ❌


## Installation

If you're running Ubuntu MATE 18.04 or later, you can conveniently access this
feature via the **Welcome** application:

![Screenshot of Colour Selection in Ubuntu MATE Welcome](.github/readme/welcome.png)

This adds the [lah7/ubuntu-mate-colours PPA](https://launchpad.net/~lah7/+archive/ubuntu/ubuntu-mate-colours/)

    sudo add-apt-repository ppa:lah7/ubuntu-mate-colours

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


### Snap Compatibility

In order for the theme to work in snapped applications, you will need to
install the snap in addition:

    sudo snap install ubuntu-mate-colours

Then, "plug" this snap to all the other snaps, [as indicated on Yaru-MATE's README](https://github.com/ubuntu-mate/gtk-theme-yaru-mate-snap#readme):

    for PLUG in $(snap connections | grep gtk-common-themes:gtk-3-themes | awk '{print $2}'); do sudo snap connect ${PLUG} ubuntu-mate-colours:gtk-3-themes; done
    for PLUG in $(snap connections | grep gtk-common-themes:gtk-2-themes | awk '{print $2}'); do sudo snap connect ${PLUG} ubuntu-mate-colours:gtk-2-themes; done
    for PLUG in $(snap connections | grep gtk-common-themes:icon-themes | awk '{print $2}'); do sudo snap connect ${PLUG} ubuntu-mate-colours:icon-themes; done

To snap an individual application, such as Firefox:

    sudo snap connect firefox:gtk-3-themes ubuntu-mate-colours:gtk-3-themes

This step may need to be repeated when installing new snaps to the system.

Please note that the snap only provides compatibility for snapped applications. It cannot
be selected as the theme in MATE's **Appearance** settings.


## Building Ambiant-MATE and Radiant-MATE

1. To begin, make sure you have a clone of this repository.

       git clone https://github.com/lah7/ubuntu-mate-colours

1. Acquire the source code for [`ubuntu-mate-artwork`]:

       git clone https://github.com/ubuntu-mate/ubuntu-mate-artwork

1. Install the dependencies:

       sudo apt install librsvg2-bin imagemagick

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

These are passed as a comma separated parameter to `--tweaks`.


## Building Yaru-MATE

1. To begin, make sure you have a clone of this repository.

       git clone https://github.com/lah7/ubuntu-mate-colours

1. Acquire the source code for [Yaru-MATE](https://github.com/ubuntu/yaru/tree/hirsute/mate):

       git clone https://github.com/ubuntu/yaru.git -b hirsute/mate

1. Install the dependencies:

       sudo apt install meson sassc libglib2.0-bin libgtk-3-dev imagemagick inkscape optipng ruby

1. Use the [generate-yaru-mate-colour.py](generate-yaru-mate-colour.py) script,
which creates a temporary copy of the source code to patch, build and optimise
to your specified colour.

The output (`--usr-dir`) can then be placed into `~/.themes` and `~/.icons`.
This script does not generate wallpapers or Plank themes.

This theme uses Yaru's build system. If `Yaru-MATE-light` and `Yaru-MATE-dark`
is already installed in `/usr/share/icons`, then uncoloured icons will be
removed to save disk space.

For usage:

    ./generate-yaru-mate-colour.py --help


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

[`ubuntu-mate-artwork`] is licensed under the GPLv3 or
[Creative Commons Attribution-ShareAlike 4.0 License].

Yaru-MATE is a branch of the [Yaru] project and its assets are licensed under
the [Creative Commons Attribution-ShareAlike 4.0 License].


[`ubuntu-mate-artwork`]: https://github.com/ubuntu-mate/ubuntu-mate-artwork
[Creative Commons Attribution-ShareAlike 4.0 License]: https://creativecommons.org/licenses/by-sa/4.0/
[Yaru]: https://github.com/ubuntu/yaru
