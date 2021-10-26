#!/bin/bash
#
# Build the Snap package, usually performed by Launchpad.
#
# Parameters:
# <$SNAPCRAFT_PART_INSTALL>
#
# =======================
# For packaging use only!
# =======================
#
OUTPUT_DIR="$1"

function generate_ambiant() {
    theme="$1"
    hex="$2"
    name="$3"
    tweaks="$4"

    echo -e "\nBuilding $theme-$name ($hex)..."
    echo -e "=================================================="
    ./generate-ambiant-mate-colour.py \
        --overwrite \
        --ignore-existing \
        --install-icon-dir="$OUTPUT_DIR/share/icons" \
        --install-theme-dir="$OUTPUT_DIR/share/themes" \
        --src-dir=/root/parts/ubuntu-mate-artwork/src/ \
        --theme="$theme" \
        --hex="$hex" \
        --name="$name" \
        --tweaks=$tweaks

    if [ $? != 0 ]; then
        echo "Build failed!"
        exit 1
    fi
}

function build_yaru() {
    hex="$1"
    name="$2"
    echo -e "\nBuilding $name ($hex)..."
    echo -e "=================================================="

    ./generate-yaru-mate-colour.py \
        --hex "$hex" \
        --name "$name" \
        --src-dir /root/parts/yaru-mate/src/ \
        --usr-dir "$OUTPUT_DIR/"

    if [ $? != 0 ]; then
        echo "Build failed!"
        exit 1
    fi
}

for theme in "Ambiant-MATE" "Ambiant-MATE-Dark" "Radiant-MATE"; do
    #                 Hex #     Name     Tweaks
    #                 --------- -------- -------------------------------------
    generate_ambiant "$theme" "#2DACD4" "Aqua"   "mono-osd-icons"
    #generate_ambiant "$theme" "#5489CF" "Blue"   "mono-osd-icons"
    #generate_ambiant "$theme" "#965024" "Brown"  "mono-osd-icons"
    #generate_ambiant "$theme" "#E95420" "Orange" "mono-osd-icons"
    #generate_ambiant "$theme" "#E231A3" "Pink"   "mono-osd-icons"
    #generate_ambiant "$theme" "#7E5BC5" "Purple" "mono-osd-icons"
    #generate_ambiant "$theme" "#CE3A3A" "Red"    "mono-osd-icons"
    #generate_ambiant "$theme" "#1CB39F" "Teal"   "mono-osd-icons"
    #generate_ambiant "$theme" "#DFCA25" "Yellow" "mono-osd-icons,black-selected-text"
done

# Build Yaru-MATE variants
build_yaru "#2DACD4" "Aqua"
#build_yaru "#5489CF" "Blue"
#build_yaru "#965024" "Brown"
#build_yaru "#E95420" "Orange"
#build_yaru "#E231A3" "Pink"
#build_yaru "#7E5BC5" "Purple"
#build_yaru "#CE3A3A" "Red"
#build_yaru "#1CB39F" "Teal"
#build_yaru "#DFCA25" "Yellow"

# Prepare snap: Move GTK2 themes to a different location
cd "$OUTPUT_DIR"
mkdir -p share/gtk2
cd share/themes/
for theme in $(ls); do
    mkdir ../gtk2/$theme
    mv "$theme/gtk-2.0" ../gtk2/$theme/
done

# Prepare snap: Update caches
for theme in $(ls); do
    gtk-update-icon-cache -f "$theme"
done
