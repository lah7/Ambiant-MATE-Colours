#
# Functions for manipulating SVGs and PNGs
#

from modules.common import status_print

import os


def export_svg(prop, svg, png):
    """
    Exports an SVG to a PNG file.
    """
    # Determine the size of the PNG file in the source theme
    png_path = os.path.join(prop.src_path, "usr/share/themes/", prop.base_theme, png)

    if not os.path.exists(png_path):
        return

    size = os.popen("identify -format '%w' {0}".format(png_path)).readlines()[0]
    status_print(prop, png, size)
    os.system("rsvg-convert -w {2} -h {2} -f png -o {1} {0}".format(svg, png, size))


def colourize_raster(new_hex, path):
    """
    Uses Imagemagick to recolour a PNG or JPG file. The resulting file will
    replace the specified path.
    """
    if not os.path.exists(path):
        return

    tmp_path = "./tmp." + path.split(".")[-1]

    # Convert to greyscale (-> tmp)
    os.system("convert {0} -colorspace gray {1}".format(path, tmp_path))

    # Convert to new tined colour (-> path)
    os.remove(path)
    os.system("convert {0} -background white -fill '{2}' -tint 100 {1}".format(tmp_path, path, new_hex))
    os.remove(tmp_path)
