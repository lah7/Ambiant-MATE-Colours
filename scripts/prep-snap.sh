#!/bin/bash
#
# Performs additional preparations for the snap package.
#
# Parameters:
# <$SNAPCRAFT_PART_INSTALL>
#
# =======================
# For packaging use only!
# =======================
#
OUTPUT_DIR="$1"

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
