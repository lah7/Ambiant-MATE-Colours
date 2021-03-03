#
# Functions for manipulating hex and RGB values
#

import colorsys
import math


def get_hex_variant(string, offset, rgb_only=False):
    """
    Converts hex input #RRGGBB to RGB and HLS to increase lightness independently
    """
    string = string.lstrip("#")
    rgb = list(int(string[i:i+2], 16) for i in (0, 2 ,4))

    # colorsys module converts to HLS to brighten/darken
    hls = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    newbright = hls[1] + offset
    newbright = min([255, max([0, newbright])])
    hls = (hls[0], newbright, hls[2])

    # reconvert to rgb and hex
    newrgb = colorsys.hls_to_rgb(hls[0], hls[1], hls[2])

    def _validate(value):
        value = int(value)
        if value > 255:
            return 255
        elif value < 0:
            return 0
        return value

    newrgb = [_validate(newrgb[0]), _validate(newrgb[1]), _validate(newrgb[2])]
    newhex = '#%02x%02x%02x' % (newrgb[0], newrgb[1], newrgb[2])

    if rgb_only:
        return newrgb
    return newhex


def get_rgb_variant_of_hex(string, offset):
    """
    Same as get_hex_variant() but returns a string of 3 comma separated integers.

    For example, to replace "168, 191, 132" with "48, 184, 226"
    """
    rgb = get_hex_variant(string, offset, rgb_only=True)
    return "{0}, {1}, {2}".format(rgb[0], rgb[1], rgb[2])


def hex_to_rgb(hex_string):
    """
    Converts "#RRGGBB" string to rgb() CSS string.
    """
    hex_string = hex_string.lstrip("#")
    rgb = list(int(hex_string[i:i+2], 16) for i in (0, 2 ,4))
    return "rgb({0}, {1}, {2})".format(rgb[0], rgb[1], rgb[2])


def hex_to_rgba(hex_string):
    """
    Converts "#RRGGBB" string to rgba() CSS string.
    """
    hex_string = hex_string.lstrip("#")
    rgb = list(int(hex_string[i:i+2], 16) for i in (0, 2 ,4))
    return "rgba({0}, {1}, {2})".format(rgb[0], rgb[1], rgb[2])


def hex_to_rgb_list(hex_string):
    """
    Converts "#RRGGBB" string to RGB value list
    """
    hex_string = hex_string.lstrip("#")
    rgb = list(int(hex_string[i:i+2], 16) for i in (0, 2 ,4))
    return [rgb[0], rgb[1], rgb[2]]


def is_dark_colour(hex_string):
    """
    Returns a boolean on whether the specified colour is dark or light.
    """
    [r,g,b] = hex_to_rgb_list(hex_string)
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    if (hsp > 127.5):
        return False
    return True
