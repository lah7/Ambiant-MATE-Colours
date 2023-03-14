# Ambiant MATE Colours

[![CI](https://github.com/lah7/Ambiant-MATE-Colours/workflows/CI/badge.svg?event=push)](https://github.com/lah7/Ambiant-MATE-Colours/actions?query=workflow%3A%22CI%22)
[![Release](https://img.shields.io/github/release/lah7/Ambiant-MATE-Colours.svg)](https://github.com/lah7/Ambiant-MATE-Colours/releases)
[![Snapcraft](https://snapcraft.io/ubuntu-mate-colours/badge.svg)](https://snapcraft.io/ubuntu-mate-colours)

![Screenshot of the 3 themes using custom colours](.github/readme/screenshot@2x.jpg)

This project generates colour variants for the [Ambiant-MATE] family, including:

* Ambiant-MATE-Dark
* Radiant-MATE


## Status

Like [Ambiant-MATE], this theme is not actively maintained and relies on
community contributions.

The theme will be continued to be packaged for new Ubuntu releases.


## Colours

Packages are made with the following pre-defined colours:

| Aqua                  | Blue                  | Brown                  | Orange                  | Pink                  | Purple                  | Red                  | Teal                  | Yellow                  |
| :-------------------: | :-------------------: | :--------------------: | :---------------------: | :-------------------: | :---------------------: | :------------------: | :-------------------: | :---------------------: |
| ![](.github/readme/aqua.png) | ![](.github/readme/blue.png) | ![](.github/readme/brown.png) | ![](.github/readme/orange.png) | ![](.github/readme/pink.png) | ![](.github/readme/purple.png) | ![](.github/readme/red.png) | ![](.github/readme/teal.png) | ![](.github/readme/yellow.png) |
| `#2DACD4`             | `#5489CF`             | `#965024`              | `#E95420`               | `#E231A3`             | `#7E5BC5`               | `#CE3A3A`            | `#1CB39F`             | `#DFCA25`               |


## Installation

Coloured themes can be obtained in a few ways:

* Ubuntu users can add the `lah7/ambiant-mate` PPA.
* Download a copy from the [Releases](https://github.com/lah7/Ambiant-MATE-Colours/releases) page.
* [Build one yourself](#building)

Ubuntu users can conveniently add the PPA like so:

    sudo add-apt-repository ppa:lah7/ambiant-mate

Packages are split by colour, so installing `ambiant-mate-colours-blue` will
give you the blue variants of the GTK and icon themes.

    sudo apt install ambiant-mate-colours-blue

Want them all? That's roughly 35 MB download, 550 MB unpacked!

    sudo apt install ambiant-mate-colours-all

After installing, themes/icons will be available from **Appearance** (Look & Feel).

To keep the size of the colour themes down, these colours depend on the original
theme packages: `ambiant-mate-gtk-themes` and `ambiant-mate-icon-themes`
(included in the PPA)


## Via Ubuntu MATE Welcome

Previously, this project was [known as `ubuntu-mate-colours`](https://github.com/lah7/Ambiant-MATE-Colours/tree/49199e9b07d172608bfef83b70e242ff3657109f),
which included recoloured wallpapers and a Plank theme.

Users running a release of Ubuntu MATE between 18.04 and 21.10 can conveniently
access this feature via the **Welcome** application:

![Screenshot of Colour Selection in Ubuntu MATE Welcome](.github/readme/welcome.png)

This adds the older [lah7/ubuntu-mate-colours PPA](https://launchpad.net/~lah7/+archive/ubuntu/ubuntu-mate-colours/),
which is now discontinued. This feature is no longer accessible in 22.04 as Yaru-MATE
now includes colour variants out of the box, and superceded this theme.


### Snap Compatibility

In order for the theme to work in snapped applications, you will need to
install the snap in addition:

    sudo snap install ubuntu-mate-colours

**Please note: The snap is no longer updated.**

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

       git clone https://github.com/lah7/Ambiant-MATE-Colours

1. Install the dependencies:

       sudo apt install librsvg2-bin imagemagick

1. (Optional) Download a copy of [Ambiant-MATE].

    Skip this step if you have the theme already installed on your system.

       git clone https://github.com/lah7/Ambiant-MATE

1. Use the script to generate your theme.

    The tool is entirely command line and parameter based. For usage:

       ./generate-ambiant-mate-colour.py --help

    By default, the new theme will be created in `~/.themes` and `~/.icons`.
    If you use Compiz, this needs to be copied (as root) to `/usr/share/`
    in order for window borders to work.


#### Tweaks

Ambiant-MATE/Radiant-MATE themes can optionally apply 'tweaks' to modify the
themes even further:

| Tweak Name             | Theme                | Description                  |
| ---------------------- | -------------------- | ---------------------------- |
| `mono-osd-icons`       | Ambiant/Radiant-MATE | [Use monochrome icons for OSD volume pop up (#14)](https://github.com/lah7/Ambiant-MATE-Colours/issues/14)
| `black-selected-text`  | Ambiant/Radiant-MATE | [The selected text colour is black instead of white (#21)](https://github.com/lah7/Ambiant-MATE-Colours/issues/21)
| `gtk3-classic`         | Ambiant/Radiant-MATE | [Append treeview alternating styling](https://github.com/lah7/gtk3-classic/wiki/Treeview:-Alternating-Colours-CSS) for use with the [gtk3-classic](https://github.com/lah7/gtk3-classic) project.

These are passed as a comma separated parameter to `--tweaks`.


## Packaging

A local package can be produced by running:

    debuild -b

Note that this runs through the entire `scripts/build.sh` script, which takes a
long time to process. A RAM disk is strongly recommended.

Packaging is not strictly required, a complete colour collection can be created like this:

    scripts/build.sh
    tar -cv usr/ | xz -z -9 > ubuntu-mate-colours-VERSION.tar.xz


## Bonus: Wallpapers

Take your favourite [Ubuntu MATE wallpaper](https://github.com/ubuntu-mate/ubuntu-mate-artwork/tree/master/usr/share/backgrounds) and recolour it:

    convert input.jpg -colorspace gray temp.jpg
    convert temp.jpg -background white -fill 'YOUR_HEX_HERE' -tint 100 output.jpg

Users upgrading to 22.04 can re-download coloured wallpapers [from this release (18.8 MB)](https://github.com/lah7/Ambiant-MATE-Colours/releases/download/21.04.6.4/ubuntu-mate-colours-21.04.6.4.tar.xz).

More tips can be found in [CONTRIBUTING.md](CONTRIBUTING.md)


## License

This program is licensed under the GPLv3.

[Ambiant-MATE] is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License].


[Ambiant-MATE]: https://github.com/lah7/Ambiant-MATE
[Creative Commons Attribution-ShareAlike 4.0 License]: https://creativecommons.org/licenses/by-sa/4.0/
