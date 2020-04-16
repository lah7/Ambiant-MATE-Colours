#!/bin/bash

# Simple shell script to generate XML wallpaper file

if [ "$#" -ne 3 ]; then
    echo "$0 basedir color outputfile"
    exit 1
fi

base=$1
col=$2
output=$3

generate() {
    name=$1
    filename=$2
    artist=$3
    lout=$4

    echo "    <wallpaper>" >> $lout
    echo "        <name>$name</name>" >> $lout
    echo "        <filename>$filename</filename>" >> $lout
    echo "        <options>zoom</options>" >> $lout
    echo "        <artist>$artist</artist>" >> $lout
    echo "    </wallpaper>" >> $lout
}

generate_color() {
    color=$1
    basedir=$2
    fout=$3

    generate "Ubuntu MATE $color Splash" "$base/Ubuntu-MATE-Colours-$color-Ubuntu-MATE-Splash.jpg" "Martin Wimpress" $fout
    generate "Ubuntu MATE $color Jazz" "$base/Ubuntu-MATE-Colours-$color-Green-Jazz.jpg" "Martin Wimpress" $fout
    generate "$color Wall" "$base/Ubuntu-MATE-Colours-$color-Green-Wall.png" "Roberto Perico" $fout
    generate "$color Wall (Logo)" "$base/Ubuntu-MATE-Colours-$color-Green-Wall-Logo.png" "Roberto Perico" $fout
    generate "$color Wall (Logo and Text)" "$base/Ubuntu-MATE-Colours-$color-Green-Wall-Logo-Text.png" "Roberto Perico" $fout
}


echo '<?xml version="1.0" encoding="UTF-8"?>' > $output
echo '<!DOCTYPE wallpapers SYSTEM "mate-wp-list.dtd">' >> $output
echo '<wallpapers>' >> $output

generate_color $col $base $output

echo '</wallpapers>' >> $output
