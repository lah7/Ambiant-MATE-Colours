# Ubuntu MATE Colours

![Screenshot of thte 3 themes using custom colours](.github/screenshot.jpg)

A small program that takes `ubuntu-mate-artwork` (theme & icons)
and swaps out the green to a colour of your choice.

Only these themes are supported:

- Ambiant-MATE
- Ambiant-MATE-Dark
- Radiant-MATE


> :warning: This is a work in progress!


## Installation

Packages are avaliable for both the generator and pre-defined colours.
On Ubuntu, simply add the PPA and install the packages as desired.

    sudo add-apt-repository ppa:lah7/ubuntu-mate-colours

The following colours are avaliable:

| Hex                               | Colour          |
| --------------------------------- | --------------- |
| ![](.github/aqua.png) `#2DACD4`   | Aqua
| ![](.github/blue.png) `#5489CF`   | Blue
| ![](.github/brown.png) `#7F441F`  | Brown
| ![](.github/green.png) `#679816`  | Green (alternate)
| ![](.github/orange.png) `#E66C1E` | Orange
| ![](.github/pink.png) `#E231A3`   | Pink
| ![](.github/purple.png) `#7E5BC5` | Purple
| ![](.github/red.png) `#CE3A3A`    | Red
| ![](.github/teal.png) `#1CB39F`   | Teal
| ![](.github/yellow.png) `#D8A200` | Yellow

Packages are split by colour, so installing `ubuntu-mate-colours-blue` will
give you the blue variants of Ambiant-MATE, Ambiant-MATE-Dark and Radiant-MATE.

    sudo apt install ubuntu-mate-colours-blue

After installing, the themes/icons will be avaliable to choose from **Appearance** (Look & Feel).

If your desired colour isn't listed, you can create your own using the generator:

    sudo apt install ubuntu-mate-colours-generator

There's also the option to install them all, but this may take up a lot of disk space!

    sudo apt install ubuntu-mate-colours-all


## Usage

First, make sure you have an up-to-date copy of the [`ubuntu-mate-artwork` repository](https://github.com/ubuntu-mate/ubuntu-mate-artwork).
If you have `git` installed, you can make a clone using this command:

    git clone https://github.com/ubuntu-mate/ubuntu-mate-artwork.git --depth=1

To update this copy without re-downloading everything in future:

    cd ubuntu-mate-artwork
    git pull --rebase origin master


#### Required arguments

```
--theme <THEME>       Ubuntu MATE theme to use, e.g. 'Ambiant-MATE'
--hex <HEX>           Colour value to use, e.g. '#3cabe4'
--name <NAME>         Human readable suffix to identify variant, e.g. 'blue'.
--src-dir             Path to ubuntu-mate-artwork repository
```

For **hex**, you can use colour picker applications to choose the colour.

    mate-color-selection
    zenity --color-selection

For example:

    generate-ubuntu-mate-colours --theme="Ambiant-MATE" --hex="#5489CF" --name="Blue"

The script by default will create the theme in `~/.local/share/themes` and
`~/.local/share/icons` using the `ubuntu-mate-artwork` repository as a source.


#### Optional arguments

```
--install-icon-dir    Path to install coloured icons
--install-theme-dir   Path to install coloured theme
-v, --verbose         Show details of each file being processed
-y, --yes             Assume yes to replace existing target directory
```


## Generated your own?

Don't forget to update your copy as time passes. To keep it up-to-date, pull the
latest changes from `ubuntu-mate-artwork` and run this program again. If
forgotten for too long, you may miss out on bug fixes and improvements
present in the `ubuntu-mate-themes` package.


## License

Both this program and [`ubuntu-mate-artwork`](https://github.com/ubuntu-mate/ubuntu-mate-artwork)
are licensed under the GPLv3.
