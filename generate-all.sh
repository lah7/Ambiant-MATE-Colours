#!/bin/bash
#
# Generates all the themes - for packaging use only!
#

CMD="./ubuntu-mate-colours-generator --yes --install-icon-dir=usr/share/icons --install-theme-dir=usr/share/themes --src-dir=/"

for theme in "Ambiant-MATE" "Ambiant-MATE-Dark" "Radiant-MATE"; do
    $CMD --theme="$theme" --hex="#2DACD4" --name="Aqua"
    $CMD --theme="$theme" --hex="#5489CF" --name="Blue"
    $CMD --theme="$theme" --hex="#7F441F" --name="Brown"
    $CMD --theme="$theme" --hex="#679816" --name="Green"
    $CMD --theme="$theme" --hex="#E66C1E" --name="Orange"
    $CMD --theme="$theme" --hex="#E231A3" --name="Pink"
    $CMD --theme="$theme" --hex="#7E5BC5" --name="Purple"
    $CMD --theme="$theme" --hex="#CE3A3A" --name="Red"
    $CMD --theme="$theme" --hex="#1CB39F" --name="Teal"
    $CMD --theme="$theme" --hex="#D8A200" --name="Yellow"
done
